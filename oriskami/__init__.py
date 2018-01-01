# Oriskami Python bindings
# API docs at https://oriskami.com/docs
# Authors:
# Fabrice Colas <fcolas@oriskami.com>
# Patrick Collison <patrick@stripe.com>
# Greg Brockman <gdb@stripe.com>
# Andrew Metcalf <andrew@stripe.com>

# Configuration variables

api_key = None
client_id = None
api_base = 'https://api.oriskami.com'
api_version = 'v1.0.0'
verify_ssl_certs = True
default_http_client = None
app_info = None

# Set to either 'debug' or 'info', controls console logging
log = None

# Resource
from oriskami.resource import (  # noqa
  Router,
  RouterParameter,
  RouterData,
  RouterFlow,
  RouterFlowBackup,
  RouterTest,
  Event,
  EventNotification,
  EventLastId,
  EventLabel,
  EventQueue,
  EventReview,
  Filters,
  FilterWhitelist,
  FilterBlacklist,
  FilterRulesCustom,
  FilterRulesAI,
  FilterRulesBase,
  FilterScoringsDedicated,
  Notifiers,
  NotifierEmail,
  NotifierSms,
  NotifierWebhook,
  NotifierECommerce,
  NotifierSlack)

# Error imports.  Note that we may want to move these out of the root
# namespace in the future and you should prefer to access them via
# the fully qualified `oriskami.error` module.

from oriskami.error import (  # noqa
    APIConnectionError,
    APIError,
    AuthenticationError,
    PermissionError,
    RateLimitError,
    InvalidRequestError,
    SignatureVerificationError,
    OriskamiError)

# DEPRECATED: These imports will be moved out of the root oriskami namespace
# in version 2.0

from oriskami.version import VERSION  # noqa
from oriskami.api_requestor import APIRequestor  # noqa
from oriskami.resource import (  # noqa
    APIResource,
    CreatableAPIResource,
    DeletableAPIResource,
    ListObject,
    ListableAPIResource,
    SingletonAPIResource,
    OriskamiObject,
    UpdatableAPIResource,
    convert_to_oriskami_object)
from oriskami.util import json, logger  # noqa


# Sets some basic information about the running application that's sent along
# with API requests. Useful for plugin authors to identify their plugin when
# communicating with Oriskami.
#
# Takes a name and optional version and plugin URL.
def set_app_info(name, version=None, url=None):
    global app_info
    app_info = {
        'name': name,
        'version': version,
        'url': url
    }
