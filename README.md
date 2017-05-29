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

* Python 2.6+ or Python 3.3+ (PyPy supported)

## Usage

The library needs to be configured with your API key which is available in [My
Ubivar][https://my.ubivar.com]. Set `ubivar.api_key` to its value:

```python
import ubivar 
ubivar.api_key = "9spB-ChM6J8NwMEEG ... WsJShd6lVQH7f6xz=".

# list events 
ubivar.Event.list()

# retrieve single event 
ubivar.Event.retrieve("123")
```

### Per-request Configuration

For apps that need to use multiple keys during the lifetime of a process, it's
also possible to set a per-request key and/or account:

``` python
import ubivar 

# list events 
ubivar.Event.list(
api_key="9spB-ChM6J8NwMEEG ... WsJShd6lVQH7f6xz=",
ubivar_account="acct_..."
)

# retrieve single charge
ubivar.Event.retrieve(
"123",
api_key="9spB-ChM6J8NwMEEG ... WsJShd6lVQH7f6xz=",
ubivar_account="acct_..."
)
```

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
