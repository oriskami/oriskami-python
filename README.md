# Ubivar python bindings 
[![PyPI version](https://badge.fury.io/py/ubivar.svg)](https://badge.fury.io/py/ubivar)
[![Build Status](https://travis-ci.org/ubivar/ubivar-python.png?branch=master)](https://travis-ci.org/ubivar/ubivar-python)
[![Inline docs](http://inch-ci.org/github/ubivar/ubivar-python.svg?branch=master)](http://inch-ci.org/github/ubivar/ubivar-python)
 
The Ubivar Python library provides convenient access to the Ubivar API from
applications written in the Python language. It includes a pre-defined set of
classes for API resources. 

## Documentation

See the [Ubivar API docs](https://www.ubivar.com/docs/python).


## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

```python
pip install --upgrade ubivar 
```

or

```python
easy_install --upgrade ubivar 
```

Install from source with:

```python
python setup.py install
```

### Requirements

* Python Python 3.6+ (PyPy supported)

## Usage

The library needs to be configured with your API key which is available in [My
Ubivar](https://my.ubivar.com). Set `ubivar.api_key` to its value:

```python
import ubivar 

ubivar.api_key = "9spB-ChM6J8NwMEEG ... WsJShd6lVQH7f6xz=".

# create event 
ubivar.Event.create(parameters = {
    "id"                          : "123"           # a unique id 
  , "email"                       : "abc@gmail.com"
  , "names"                       : "M Abc"
  , "account_creation_time"       : "2017-05-17 21:50:00"
  , "account_id"                  : "10000"
  , "account_n_fulfilled"         : "1"
  , "account_total_since_created" : "49.40"
  , "account_total_cur"           : "EUR"
  , "invoice_time"                : "2017-05-17 21:55:00"
  , "invoice_address_country"     : "France"
  , "invoice_address_place"       : "75008 Paris"
  , "invoice_address_street1"     : "1 Av. des Champs-Élysées"
  , "invoice_name"                : "M ABC"
  , "invoice_phone1"              : "0123456789"
  , "invoice_phone2"              : null
  , "transport_date"              : "2017-05-18 08:00:00"
  , "transport_type"              : "Delivery"
  , "transport_mode"              : "TNT"
  , "transport_weight"            : "9.000"
  , "transport_unit"              : "kg"
  , "transport_cur"               : "EUR"
  , "delivery_address_country"    : "France"
  , "delivery_address_place"      : "75008 Paris"
  , "delivery_address_street1"    : "1 Av. des Champs-Élysées"
  , "delivery_name"               : "M ABC"
  , "delivery_phone1"             : "0123450689"
  , "customer_ip_address"         : "1.2.3.4"
  , "pmeth_origin"                : "FRA"
  , "pmeth_validity"              : "0121"
  , "pmeth_brand"                 : "MC"
  , "pmeth_bin"                   : "510000"
  , "pmeth_3ds"                   : "-1"
  , "cart_products"               : [ "Product ref #12345" ]
  , "cart_details"                : [{
      "name"                      : "Product ref #12345"
    , "pu"                        : "10.00"
    , "n"                         : "1"
    , "amount"                    : "10.00"
    , "cur"                       : "EUR" 
    }]
  , "cart_n"                      : "15000"
  , "order_payment_accepted"      : "2017-05-17 22:00:00"
  , "amount_pmeth"                : "ABC Payment Service Provider"
  , "amount_discounts"            :  "0.00"
  , "amount_products"             : "20.00"
  , "amount_transport"            : "10.00"
  , "amount_total"                : "30.00"
  , "amount_cur"                  : "EUR"
})

# retrieve single event 
ubivar.Event.retrieve("123")

# list events 
ubivar.Event.list()
```

### Per-request Configuration

For apps that need to use multiple keys during the lifetime of a process, it's
also possible to set a per-request key and/or account:

``` python
import ubivar 

# list events 
ubivar.Event.list(api_key="9spB-ChM6J8NwMEEG ... WsJShd6lVQH7f6xz=")

# retrieve single event 
ubivar.Event.retrieve("123", api_key="9spB-ChM6J8NwMEEG ... WsJShd6lVQH7f6xz=")
```

## Resources, actions, and arguments 
Every resource is accessed via your `ubivar` instance and accepts an optional
callback as the last argument. In the matrix below we list the resources
(rows), the actions (columns) and the arguments (cells). The full documentation
is available at [https://ubivar.com/docs/python](https://ubivar.com/docs/python). 

|               | Resource                | C | R | U | D | L     | Test Specs |
|--------------:| ----------------------- |:-:|:-:|:-:|:-:|:-----:|:-------:|
| **Data**      | Events                  | [`{}`](https://ubivar.com/docs/python#create_event)| [123](https://ubivar.com/docs/python#retrieve_event) | [`{}`](https://ubivar.com/docs/python#update_event) | [123](https://ubivar.com/docs/python#delete_event) | [`{}`](https://ubivar.com/docs/python#list_events) | | 
|               | Labels                  | [`{}`](https://ubivar.com/docs/python#create_label)| [123](https://ubivar.com/docs/python#retrieve_label) | [`{}`](https://ubivar.com/docs/python#update_label) | [123](https://ubivar.com/docs/python#delete_label) | [`{}`](https://ubivar.com/docs/python#list_labels) | | 
|               | Features                |   | [123](https://ubivar.com/docs/python#retrieve_feature) |  |  | [`{}`](https://ubivar.com/docs/python#list_features) | | 
|               | Last id                 |   |  |  |  | [`{}`](https://ubivar.com/docs/python#list_last_id) | | 
| **Filtering** | Whitelists              | [`{}`](https://ubivar.com/docs/python#create_whitelist)| [123](https://ubivar.com/docs/python#retrieve_whitelist) | [`{}`](https://ubivar.com/docs/python#update_whitelist) | [123](https://ubivar.com/docs/python#delete_whitelist) | [`{}`](https://ubivar.com/docs/python#list_whitelists) | | 
|               | Blacklists              |   | [123](https://ubivar.com/docs/python#retrieve_blacklist) | [`{}`](https://ubivar.com/docs/python#update_blacklist) |  | [`{}`](https://ubivar.com/docs/python#list_blacklists) | | 
|               | Custom rules            | [`{}`](https://ubivar.com/docs/python#create_custom_rule)| [123](https://ubivar.com/docs/python#retrieve_custom_rule) | [`{}`](https://ubivar.com/docs/python#update_custom_rule) | [123](https://ubivar.com/docs/python#delete_custom_rule) | [`{}`](https://ubivar.com/docs/python#list_custom_rules) | | 
|               | Base rules              |   | [123](https://ubivar.com/docs/python#retrieve_base_rule) | [`{}`](https://ubivar.com/docs/python#update_base_rule) |  | [`{}`](https://ubivar.com/docs/python#list_base_rules) | | 
|               | AI rules                |   | [123](https://ubivar.com/docs/python#retrieve_ai_rule) | [`{}`](https://ubivar.com/docs/python#update_ai_rule) |  | [`{}`](https://ubivar.com/docs/python#list_ai_rules) | | 
|               | Dedicated scoring       | [`{}`](https://ubivar.com/docs/python#create_dedicated_scorings)| [123](https://ubivar.com/docs/python#retrieve_dedicated_scorings) | [`{}`](https://ubivar.com/docs/python#update_dedicated_scorings) | [123](https://ubivar.com/docs/python#delete_dedicated_scorings) | [`{}`](https://ubivar.com/docs/python#list_dedicated_scorings) | | 
| **Notifications** | Email | [`{}`](https://ubivar.com/docs/python#create_email)| [123](https://ubivar.com/docs/python#retrieve_email) | [`{}`](https://ubivar.com/docs/python#update_email) | [123](https://ubivar.com/docs/python#delete_email) | [`{}`](https://ubivar.com/docs/python#list_emails) | | 
|                   | Sms   | [`{}`](https://ubivar.com/docs/python#create_sms)| [123](https://ubivar.com/docs/python#retrieve_sms) | [`{}`](https://ubivar.com/docs/python#update_sms) | [123](https://ubivar.com/docs/python#delete_sms) | [`{}`](https://ubivar.com/docs/python#list_sms) | | 
|                   | Webhook | [`{}`](https://ubivar.com/docs/python#create_webhook)| [123](https://ubivar.com/docs/python#retrieve_webhook) | [`{}`](https://ubivar.com/docs/python#update_webhook) | [123](https://ubivar.com/docs/python#delete_webhook) | [`{}`](https://ubivar.com/docs/python#list_webhooks) | | 
|                   | E-commerce |   | [123](https://ubivar.com/docs/python#retrieve_e-commerce) | [`{}`](https://ubivar.com/docs/python#update_e-commerce) |  |  | | 
|                   | Slack | [`{}`](https://ubivar.com/docs/python#create_slack)| [123](https://ubivar.com/docs/python#retrieve_slack) | [`{}`](https://ubivar.com/docs/python#update_slack) | [123](https://ubivar.com/docs/python#delete_slack) | [`{}`](https://ubivar.com/docs/python#list_slacks) | | 


+ *C*: Create
+ *R*: Retrieve
+ *U*: Update
+ *D*: Delete
+ *L*: List
+ `{}`: JSON with query parameters

## Filter parameters

| Filter        | Default | Example             | Description                   |
| ------------- |:-------:|:--------------------|:------------------------------|
| `start_after` |         | `{"start_after":10}`| `id` after the one specified  |
| `end_before`  |         | `{"end_before":10}` | `id` before the one specified |
| `limit`       | `10`    | `{"limit":10}`      | At most `10` returned results |
| `gt`          |         | `{"id":{"gt":10}}`  | `id` greater than 10          |
| `gte`         |         | `{"id":{"gte":10}}` | `id` greater than or equal    |
| `lt`          |         | `{"id":{"lt":10}}`  | `id` less than                |
| `lte`         |         | `{"id":{"lte":10}}` | `id` less than or equal       |


### Configuring a Client

The library can be configured to use `urlfetch`, `requests`, `pycurl`, or
`urllib2` with `ubivar.default_http_client`:

``` python
client = ubivar.http_client.UrlFetchClient()
client = ubivar.http_client.RequestsClient()
client = ubivar.http_client.PycurlClient()
client = ubivar.http_client.Urllib2Client()
ubivar.default_http_client = client
```

Without a configured client, by default the library will attempt to load
libraries in the order above (i.e. `urlfetch` is preferred with `urllib2` used
as a last resort). We usually recommend that people use `requests`.


### Logging

The library can be configured to emit logging that will give you better insight
into what it's doing. The `info` logging level is usually most appropriate for
production use, but `debug` is also available for more verbosity.

There are a few options for enabling it:

1. Set the environment variable `UBIVAR_LOG` to the value `debug` or `info`
```
$ export UBIVAR_LOG=debug
```

2. Set `ubivar.log`:
```py
import ubivar
ubivar.log = 'debug'
```

3. Enable it through Python's logging module:
```py
import logging
logging.basicConfig()
logging.getLogger('ubivar').setLevel(logging.DEBUG)
```

### [Issues and feature requests](https://github.com/ubivar/ubivar-python/issues)

## Author

Originally inspired from [stripe-python](https://github.com/stripe/stripe-python). Developed and maintained by [Fabrice Colas](https://fabricecolas.me) ([fabrice.colas@gmail.com](mailto:fabrice.colas@gmail.com)) for [Ubivar](https://ubivar.com). 
