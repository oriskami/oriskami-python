# Ubivar Python bindings
# API docs at https://ubivar.com/docs
# Authors:
# Fabrice Colas <fcolas@ubivar.com>
# Patrick Collison <patrick@stripe.com>
# Greg Brockman <gdb@stripe.com>
# Andrew Metcalf <andrew@stripe.com>

# Configuration variables

api_key = None
client_id = None
api_base = 'https://api.ubivar.com'
api_version = 'v1.0.0' 
verify_ssl_certs = True
default_http_client = None
app_info = None

# Set to either 'debug' or 'info', controls console logging
log = None

# Resource
from ubivar.resource import (  # noqa
    Event
  , Label
  , Feature
  , LastId
  , Whitelist
  , Blacklist
  , RulesCustom
  , RulesAI
  , RulesBase
  , DedicatedScorings
  , Email
  , Sms
  , Webhook
  , ECommerce
  , Slack)

# Webhooks
from ubivar.webhook import Webhook, WebhookSignature  # noqa

# Error imports.  Note that we may want to move these out of the root
# namespace in the future and you should prefer to access them via
# the fully qualified `ubivar.error` module.

from ubivar.error import (  # noqa
    APIConnectionError,
    APIError,
    AuthenticationError,
    PermissionError,
    RateLimitError,
    InvalidRequestError,
    SignatureVerificationError,
    UbivarError)

# DEPRECATED: These imports will be moved out of the root ubivar namespace
# in version 2.0

from ubivar.version import VERSION  # noqa
from ubivar.api_requestor import APIRequestor  # noqa
from ubivar.resource import (  # noqa
    APIResource,
    CreateableAPIResource,
    DeletableAPIResource,
    ListObject,
    ListableAPIResource,
    SingletonAPIResource,
    UbivarObject,
    UpdateableAPIResource,
    convert_to_ubivar_object)
from ubivar.util import json, logger  # noqa


# Sets some basic information about the running application that's sent along
# with API requests. Useful for plugin authors to identify their plugin when
# communicating with Ubivar.
#
# Takes a name and optional version and plugin URL.
def set_app_info(name, version=None, url=None):
    global app_info
    app_info = {
        'name': name,
        'version': version,
        'url': url,
    }
