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
Ubivar](https://my.ubivar.com). Set `ubivar.api_key` to its value or for apps
that need to use multiple keys during the lifetime of a process, set a key
per-request. 

```python
import ubivar 

ubivar.api_key = "9spB-ChM6J8NwMEEG ... WsJShd6lVQH7f6xz=".

# Create event 
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

# Retrieve, Update, Delete, or List Events 
ubivar.Event.retrieve("123")
ubivar.Event.update("123", parameters={"extra_is_verified": "true", "extra_is_graylisted": "false"}})
ubivar.Event.delete("123")
ubivar.Event.list()

# Create, Retrieve, Update, Delete or List Whiteslits
ubivar.FilterWhitelist.create(description="Test", feature="email_domain", is_active="true", value="gmail.com")
ubivar.FilterWhitelist.retrieve("0")
ubivar.FilterWhitelist.update("0", description="Test", feature="email_domain", is_active="true", value="yahoo.com")
ubivar.FilterWhitelist.delete("123")
ubivar.FilterWhitelist.list()

# Specify a different API key for each request
ubivar.Event.list(api_key="9spB-ChM6J8NwMEEG ... WsJShd6lVQH7f6xz=")
```
## Resources, actions, and arguments 
Every resource is accessed via your `ubivar`. The following matrix list the
resources (rows), the CRUD actions (columns) and the arguments (cells). The cell links
point to the full documentation at [https://ubivar.com/docs/python](https://ubivar.com/docs/python). 

|               | Resource                | C | R | U | D | L     | Test Specs |
|--------------:| ----------------------- |:-:|:-:|:-:|:-:|:-----:|:-------:|
| **Event data**| Events                  | [`{}`](https://ubivar.com/docs/python#create_event)| [`123`](https://ubivar.com/docs/python#retrieve_event) | [`123, {}`](https://ubivar.com/docs/python#update_event) | [`123`](https://ubivar.com/docs/python#delete_event) | [`{}`](https://ubivar.com/docs/python#list_events) | | 
|               | EventNotifications      |  | [`123`](https://ubivar.com/docs/python#retrieve_eventnotification) |  |  | [`{}`](https://ubivar.com/docs/python#list_eventnotifications) | | 
|               | EventLastId             |  | [`123`](https://ubivar.com/docs/python#retrieve_eventlastid) |  |  | [`{}`](https://ubivar.com/docs/python#list_eventlastids) | | 
|               | EventFeatures           |  | [`123`](https://ubivar.com/docs/python#retrieve_eventfeature) |  |  | [`{}`](https://ubivar.com/docs/python#list_eventfeatures) | | 
|               | EventLabels             | [`{}`](https://ubivar.com/docs/python#create_eventlabel)| [`123`](https://ubivar.com/docs/python#retrieve_eventlabel) | [`123, {}`](https://ubivar.com/docs/python#update_eventlabel) | [`123`](https://ubivar.com/docs/python#delete_eventlabel) | [`{}`](https://ubivar.com/docs/python#list_eventlabels) | | 
|               | EventQueues             | [`{}`](https://ubivar.com/docs/python#create_eventqueue)| [`123`](https://ubivar.com/docs/python#retrieve_eventqueue) | [`123, {}`](https://ubivar.com/docs/python#update_eventqueue) | [`123`](https://ubivar.com/docs/python#delete_eventqueue) | [`{}`](https://ubivar.com/docs/python#list_eventqueues) | | 
|               | EventReviews            | [`{}`](https://ubivar.com/docs/python#create_eventreview)| [`123`](https://ubivar.com/docs/python#retrieve_eventreview) | [`123, {}`](https://ubivar.com/docs/python#update_eventreview) | [`123`](https://ubivar.com/docs/python#delete_eventreview) | [`{}`](https://ubivar.com/docs/python#list_eventreviews) | | 
|               | Last id                 |   |  |  |  | [`{}`](https://ubivar.com/docs/python#list_last_id) | | 
| **Filters** | FilterWhitelists        | [`{}`](https://ubivar.com/docs/python#create_filterwhitelist)| [`123`](https://ubivar.com/docs/python#retrieve_filterwhitelist) | [`123, {}`](https://ubivar.com/docs/python#update_filterwhitelist) | [`123`](https://ubivar.com/docs/python#delete_filterwhitelist) | [`{}`](https://ubivar.com/docs/python#list_filterwhitelists) | | 
|               | FilterBlacklists        |   | [`123`](https://ubivar.com/docs/python#retrieve_filterblacklist) | [`123, {}`](https://ubivar.com/docs/python#update_filterblacklist) |  | [`{}`](https://ubivar.com/docs/python#list_filterblacklists) | | 
|               | FilterRulesCustoms      | [`{}`](https://ubivar.com/docs/python#create_filterrulescustom)| [`123`](https://ubivar.com/docs/python#retrieve_filterrulescustom) | [`123, {}`](https://ubivar.com/docs/python#update_filterrulescustom) | [`123`](https://ubivar.com/docs/python#delete_filterrulescustom) | [`{}`](https://ubivar.com/docs/python#list_filterrulescustoms) | | 
|               | FilterRulesBase         |   | [`123`](https://ubivar.com/docs/python#retrieve_filterrulesbase) | [`123, {}`](https://ubivar.com/docs/python#update_filterrulesbase) |  | [`{}`](https://ubivar.com/docs/python#list_filterrulesbases) | | 
|               | FilterRulesAI           |   | [`123`](https://ubivar.com/docs/python#retrieve_filterrulesai) | [`123, {}`](https://ubivar.com/docs/python#update_filterrulesai) |  | [`{}`](https://ubivar.com/docs/python#list_filterrulesais) | | 
|               | FilterScoringsDedicated |   | [`123`](https://ubivar.com/docs/python#retrieve_filterscoringsdedicated) | [`123, {}`](https://ubivar.com/docs/python#update_filterscoringsdedicated) |  | [`{}`](https://ubivar.com/docs/python#list_filterscoringsdedicated) | | 
| **Notifications** | NotifierEmails      | [`{}`](https://ubivar.com/docs/python#create_notifieremail)| [`123`](https://ubivar.com/docs/python#retrieve_notifieremail) | [`123, {}`](https://ubivar.com/docs/python#update_notifieremail) | [`123`](https://ubivar.com/docs/python#delete_notifieremail) | [`{}`](https://ubivar.com/docs/python#list_notifieremails) | | 
|               | NotifierSms             | [`{}`](https://ubivar.com/docs/python#create_notifiersms)| [`123`](https://ubivar.com/docs/python#retrieve_notifiersms) | [`123, {}`](https://ubivar.com/docs/python#update_notifiersms) | [`123`](https://ubivar.com/docs/python#delete_notifiersms) | [`{}`](https://ubivar.com/docs/python#list_notifiersms) | | 
|               | NotifierWebhook         | [`{}`](https://ubivar.com/docs/python#create_notifierwebhook)| [`123`](https://ubivar.com/docs/python#retrieve_notifierwebhook) | [`123, {}`](https://ubivar.com/docs/python#update_notifierwebhook) | [`123`](https://ubivar.com/docs/python#delete_notifierwebhook) | [`{}`](https://ubivar.com/docs/python#list_notifierwebhooks) | | 
|               | NotifierECommerce       |   | [`123`](https://ubivar.com/docs/python#retrieve_notifierecommerce) | [`123, {}`](https://ubivar.com/docs/python#update_notifierecommerce) |  |  | | 
|               | NotifierSlack           | [`{}`](https://ubivar.com/docs/python#create_notifierslack)| [`123`](https://ubivar.com/docs/python#retrieve_notifierslack) | [`123, {}`](https://ubivar.com/docs/python#update_notifierslack) | [`123`](https://ubivar.com/docs/python#delete_notifierslack) | [`{}`](https://ubivar.com/docs/python#list_notifierslacks) | | 


+ *C*: Create
+ *R*: Retrieve
+ *U*: Update
+ *D*: Delete
+ *L*: List
+ `123`: resource id 
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
