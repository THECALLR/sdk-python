sdk-python
==========

SDK in Python for THECALLR API

## Quick start
Install via PyPI

    pip install thecallr

Or get sources from Github

## Initialize your code

Pip

```python
import thecallr
```

Source

```python
import sys
sys.path.append("/path/to/thecallr_folder")
import thecallr
```

## Basic Example (Send SMS)
See full example in [samples/quickstart.py](samples/quickstart.py)

```python
# Set your credentials
tc = thecallr.Api("login", "password")

# 1. "call" method: each parameter of the method as an argument
tc.call("sms.send", "THECALLR", "+33123456789", "Hello, world", {
	"flash_message": False
})

# 2. "send" method: parameter of the method is an array
my_array = ["THECALLR", "+33123456789", "Hello, world", {
	"flash_message": False
}]
tc.send("sms.send", my_array)
```

## Exception Management

```python
try:
	# Set your credentials
	tc = thecallr.Api("login", "password")

	# This will raise an exception
	tc.call("sms.send", "THECALLR")

# Exceptions handler
except (thecallr.ThecallrException, thecallr.ThecallrLocalException) as e:
	print "ERROR: %s" % e.code
	print "MESSAGE: %s" % e.msg
	print "DATA: ", e.data
```
