import urllib
import sys
from copy import deepcopy
from ubivar import api_requestor, error, util


def convert_to_ubivar_object(resp, api_key):
    types = {
            'events': Event,
            'event_labels': EventLabel,
            'event_notifications': EventNotification,
            'event_queues': EventQueue,
            'event_reviews': EventReview,
            'event_last_id': EventLastId,
            'filter_whitelists': FilterWhitelist,
            'filter_blacklists': FilterBlacklist,
            'filter_rules_custom': FilterRulesCustom,
            'filter_rules_base': FilterRulesBase,
            'filter_rules_ai': FilterRulesAI,
            'filter_scorings_dedicated': FilterScoringsDedicated,
            'notifier_emails': NotifierEmail,
            'notifier_sms': NotifierSms,
            'notifier_ecommerce': NotifierECommerce,
            'notifier_slack': NotifierSlack,
            'notifier_webhooks': NotifierWebhook
            }

    if isinstance(resp, list):
        return [convert_to_ubivar_object(i, api_key) for i in resp]
    elif isinstance(resp, dict) and not isinstance(resp, UbivarObject):
        resp = resp.copy()
        klass_name = resp.get('object')
        if isinstance(klass_name, str):
            klass = types.get(klass_name, UbivarObject)
        else:
            klass = UbivarObject
        return klass.construct_from(resp, api_key)
    else:
        return resp


def convert_array_to_dict(arr):
    if isinstance(arr, list):
        d = {}
        for i, value in enumerate(arr):
            d[str(i)] = value
        return d
    else:
        return arr


def _compute_diff(current, previous):
    if isinstance(current, dict):
        previous = previous or {}
        diff = current.copy()
        for key in set(previous.keys()) - set(diff.keys()):
            diff[key] = ""
        return diff
    return current if current is not None else ""


def _serialize_list(array, previous):
    array = array or []
    previous = previous or []
    params = {}

    for i, v in enumerate(array):
        previous_item = previous[i] if len(previous) > i else None
        if hasattr(v, 'serialize'):
            params[str(i)] = v.serialize(previous_item)
        else:
            params[str(i)] = _compute_diff(v, previous_item)

    return params


class UbivarObject(dict):
    def __init__(self, id=None, api_key=None, **params):
        super(UbivarObject, self).__init__()

        self._unsaved_values = set()
        self._transient_values = set()
        self._retrieve_params = params
        self._previous = None

        object.__setattr__(self, 'api_key', api_key)

        if id:
            self['id'] = id

    def update(self, update_dict):
        for k in update_dict:
            self._unsaved_values.add(k)

        return super(UbivarObject, self).update(update_dict)

    def __setattr__(self, k, v):
        if k[0] == '_' or k in self.__dict__:
            return super(UbivarObject, self).__setattr__(k, v)

        self[k] = v
        return None

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)

        try:
            return self[k]
        except KeyError as err:
            raise AttributeError(*err.args)

    def __delattr__(self, k):
        if k[0] == '_' or k in self.__dict__:
            return super(UbivarObject, self).__delattr__(k)
        else:
            del self[k]

    def __setitem__(self, k, v):
        if v == "":
            raise ValueError("You cannot set %s to an empty string. We "
                             "interpret empty strings as None in requests. You"
                             "may set %s.%s = None to delete the property" %
                             (k, str(self), k))

        super(UbivarObject, self).__setitem__(k, v)

        # Allows for unpickling in Python 3.x
        if not hasattr(self, '_unsaved_values'):
            self._unsaved_values = set()

        self._unsaved_values.add(k)

    def __getitem__(self, k):
        try:
            return super(UbivarObject, self).__getitem__(k)
        except KeyError as err:
            if k in self._transient_values:
                raise KeyError(
                    "%r.  HINT: The %r attribute was set in the past."
                    "It was then wiped when refreshing the object with "
                    "the result returned by Ubivar's API, probably as a "
                    "result of a save().  The attributes currently "
                    "available on this object are: %s" %
                    (k, k, ', '.join(self.keys())))
            else:
                raise err

    def __delitem__(self, k):
        super(UbivarObject, self).__delitem__(k)

        # Allows for unpickling in Python 3.x
        if hasattr(self, '_unsaved_values'):
            self._unsaved_values.remove(k)

    @classmethod
    def construct_from(cls, values, key):
        instance = cls(values.get('id'), api_key=key)
        instance.refresh_from(values, api_key=key)
        return instance

    def refresh_from(self, values, api_key=None, partial=False):
        self.api_key = api_key or getattr(values, 'api_key', None)

        # Wipe old state before setting new.  This is useful for e.g.
        # updating a customer, where there is no persistent card
        # parameter.  Mark those values which don't persist as transient
        if partial:
            self._unsaved_values = (self._unsaved_values - set(values))
        else:
            removed = set(self.keys()) - set(values)
            self._transient_values = self._transient_values | removed
            self._unsaved_values = set()
            self.clear()

        self._transient_values = self._transient_values - set(values)

        for k, v in values.items():
            super(UbivarObject, self).__setitem__(
                k, convert_to_ubivar_object(v, api_key))

        self._previous = values

    @classmethod
    def api_base(cls):
        return None

    def request(self, method, url, params=None, headers=None):
        if params is None:
            params = self._retrieve_params
        requestor = api_requestor.APIRequestor(
            key=self.api_key, api_base=self.api_base())
        response, api_key = requestor.request(method, url, params, headers)

        return convert_to_ubivar_object(response, api_key)

    def __repr__(self):
        ident_parts = [type(self).__name__]

        if isinstance(self.get('object'), str):
            ident_parts.append(self.get('object'))

        if isinstance(self.get('id'), str):
            ident_parts.append('id=%s' % (self.get('id'),))

        unicode_repr = '<%s at %s> JSON: %s' % (
            ' '.join(ident_parts), hex(id(self)), str(self))

        if sys.version_info[0] < 3:
            return unicode_repr.encode('utf-8')
        else:
            return unicode_repr

    def __str__(self):
        return util.json.dumps(self, sort_keys=True, indent=2)

    @property
    def ubivar_id(self):
        return self.id

    def serialize(self, previous):
        params = {}
        unsaved_keys = self._unsaved_values or set()
        previous = previous or self._previous or {}

        for k, v in self.items():
            if k == 'id' or (isinstance(k, str) and k.startswith('_')):
                continue
            elif isinstance(v, APIResource):
                continue
            elif hasattr(v, 'serialize'):
                params[k] = v.serialize(previous.get(k, None))
            elif k in unsaved_keys:
                params[k] = _compute_diff(v, previous.get(k, None))
            elif k == 'additional_owners' and v is not None:
                params[k] = _serialize_list(v, previous.get(k, None))

        return params

    # This class overrides __setitem__ to throw exceptions on inputs that it
    # doesn't like. This can cause problems when we try to copy an object
    # wholesale because some data that's returned from the API may not be valid
    # if it was set to be set manually. Here we override the class' copy
    # arguments so that we can bypass these possible exceptions on __setitem__.
    def __copy__(self):
        copied = UbivarObject(self.get('id'), self.api_key)

        copied._retrieve_params = self._retrieve_params

        for k, v in self.items():
            # Call parent's __setitem__ to avoid checks that we've added in the
            # overridden version that can throw exceptions.
            super(UbivarObject, copied).__setitem__(k, v)

        return copied

    # This class overrides __setitem__ to throw exceptions on inputs that it
    # doesn't like. This can cause problems when we try to copy an object
    # wholesale because some data that's returned from the API may not be valid
    # if it was set to be set manually. Here we override the class' copy
    # arguments so that we can bypass these possible exceptions on __setitem__.
    def __deepcopy__(self, memo):
        copied = self.__copy__()
        memo[id(self)] = copied

        for k, v in self.items():
            # Call parent's __setitem__ to avoid checks that we've added in the
            # overridden version that can throw exceptions.
            super(UbivarObject, copied).__setitem__(k, deepcopy(v, memo))

        return copied


class APIResource(UbivarObject):

    @classmethod
    def retrieve(cls, id, api_key=None, **params):
        instance = cls(id, api_key, **params)
        instance.refresh()
        return instance

    def refresh(self):
        self.refresh_from(self.request('get', self.instance_url()))
        return self

    @classmethod
    def class_name(cls):
        if cls == APIResource:
            raise NotImplementedError(
                'APIResource is an abstract class.  You should perform '
                'actions on its subclasses (e.g. Charge, Customer)')
        return str(urllib.parse.quote_plus(cls.__name__.lower()))

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return "/%s" % (cls_name,)

    def instance_url(self):
        id = self.get('id')
        if not id:
            raise error.InvalidRequestError(
                'Could not determine which URL to request: %s instance '
                'has invalid ID: %r' % (type(self).__name__, id), 'id')
        id = util.utf8(id)
        base = self.class_url()
        extn = urllib.parse.quote_plus(id)
        return "%s/%s" % (base, extn)


class ListObject(UbivarObject):

    def list(self, **params):
        return self.request('get', self['url'], params)

    def auto_paging_iter(self):
        page = self
        params = dict(self._retrieve_params)

        while True:
            item_id = None
            for item in page:
                item_id = item.get('id', None)
                yield item

            if not getattr(page, 'has_more', False) or item_id is None:
                return

            params['starting_after'] = item_id
            page = self.list(**params)

    def create(self, **params):
        return self.request('post', self['url'], params)

    def retrieve(self, id, **params):
        base = self.get('url')
        id = util.utf8(id)
        extn = urllib.parse.quote_plus(id)
        url = "%s/%s" % (base, extn)

        return self.request('get', url, params)

    def __iter__(self):
        return getattr(self, 'data', []).__iter__()


class SingletonAPIResource(APIResource):

    @classmethod
    def retrieve(cls, **params):
        return super(SingletonAPIResource, cls).retrieve(None, **params)

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return "/%s" % (cls_name,)

    def instance_url(self):
        return self.class_url()


#######################################################
# CLASSES OF API OPERATIONS                           #
#######################################################


class ListableAPIResource(APIResource):

    @classmethod
    def auto_paging_iter(cls, *args, **params):
        return cls.list(*args, **params).auto_paging_iter()

    @classmethod
    def list(cls, api_key=None, **params):
        requestor = api_requestor.APIRequestor(api_key,
                                               api_base=cls.api_base())
        url = cls.class_url()
        response, api_key = requestor.request('get', url, params)
        ubivar_object = convert_to_ubivar_object(response, api_key)
        ubivar_object._retrieve_params = params
        return ubivar_object


class CreatableAPIResource(APIResource):

    @classmethod
    def create(cls, api_key=None, **params):
        requestor = api_requestor.APIRequestor(api_key)
        url = cls.class_url()
        response, api_key = requestor.request('post', url, params)
        return convert_to_ubivar_object(response, api_key)


class UpdatableAPIResource(APIResource):

    @classmethod
    def update(cls, resource_id, api_key=None, **params):
        requestor = api_requestor.APIRequestor(api_key)
        url = cls.class_url() + "/" + resource_id
        response, api_key = requestor.request('post', url, params)
        return convert_to_ubivar_object(response, api_key)


class DeletableAPIResource(APIResource):

    @classmethod
    def delete(cls, resource_id, api_key=None, **params):
        requestor = api_requestor.APIRequestor(api_key)
        url = cls.class_url() + "/" + resource_id
        response, api_key = requestor.request('delete', url, params)
        return convert_to_ubivar_object(response, api_key)

#####################################################
#
# API OBJECTS
#
#


class Event(CreatableAPIResource, UpdatableAPIResource,
            DeletableAPIResource, ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'events'


class EventLabel(UpdatableAPIResource, DeletableAPIResource, 
                 ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'event_labels'


class EventNotification(ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'event_notifications'


class EventQueue(UpdatableAPIResource, DeletableAPIResource, 
                 ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'event_queues'


class EventReview(UpdatableAPIResource, DeletableAPIResource, 
                  ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'event_reviews'


class EventLastId(ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'event_last_id'


class FilterWhitelist(CreatableAPIResource, UpdatableAPIResource,
                      DeletableAPIResource, ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'filter_whitelists'


class FilterBlacklist(UpdatableAPIResource, ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'filter_blacklists'


class FilterRulesCustom(CreatableAPIResource, UpdatableAPIResource,
                        DeletableAPIResource, ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'filter_rules_custom'


class FilterRulesBase(UpdatableAPIResource, ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'filter_rules_base'


class FilterRulesAI(UpdatableAPIResource, ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'filter_rules_ai'


class FilterScoringsDedicated(UpdatableAPIResource,
                              ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'filter_scorings_dedicated'


class NotifierEmail(CreatableAPIResource, UpdatableAPIResource,
                    DeletableAPIResource, ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'notifier_emails'


class NotifierECommerce(UpdatableAPIResource, ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'notifier_ecommerce'


class NotifierWebhook(CreatableAPIResource, UpdatableAPIResource,
                      DeletableAPIResource, ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'notifier_webhooks'


class NotifierSlack(CreatableAPIResource, UpdatableAPIResource,
                    DeletableAPIResource, ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'notifier_slack'


class NotifierSms(CreatableAPIResource, UpdatableAPIResource,
                  DeletableAPIResource, ListableAPIResource):

    @classmethod
    def class_name(cls):
        return 'notifier_sms'
