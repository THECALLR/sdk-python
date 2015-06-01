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
api = thecallr.Api("login", "password")

# 1. "call" method: each parameter of the method as an argument
api.call("sms.send", "THECALLR", "+33123456789", "Hello, world", {
	"flash_message": False
})

# 2. "send" method: parameter of the method is an array
my_array = ["THECALLR", "+33123456789", "Hello, world", {
	"flash_message": False
}]
api.send("sms.send", my_array)
```

## Exception Management

```python
try:
	# Set your credentials
	api = thecallr.Api("login", "password")

	# This will raise an exception
	api.call("sms.send", "THECALLR")

# Exceptions handler
except (thecallr.ThecallrException, thecallr.ThecallrLocalException) as e:
	print "ERROR: %s" % e.code
	print "MESSAGE: %s" % e.msg
	print "DATA: ", e.data
```



## Usage
**Send an SMS**

* Without options

```python
result = api.call('sms.send', 'CALLR', '+33123456789', 'Hello world!')
```

* Personalized sender

Your sender must have been authorized and respect the [sms_sender](http://thecallr.com/docs/formats/#sms_sender) format
```python
result = api.call('sms.send', 'Your Brand', '+33123456789', 'Hello world!')
```

* If you want to receive replies, do not set a sender, we will automatically use a shortcode

```python
result = api.call('sms.send', '', '+33123456789', 'Hello world!')
```

* Force GSM encoding

```python
optionSMS = {
	:force_encoding => 'GSM'
}
result = api.call('sms.send', '', '+33123456789', 'Hello world!', optionSMS)
```

* Long SMS (availability depends on carrier)

```python
text = 'Some super mega ultra long text to test message longer than 160 characters ',
       'Some super mega ultra long text to test message longer than 160 characters ',
       'Some super mega ultra long text to test message longer than 160 characters'
result = api.call('sms.send', 'CALLR', '+33123456789', text);
```

* Specify your SMS type

```python
optionSMS = {
	'nature': 'ALERTING'
}
result = api.call('sms.send', 'CALLR', '+33123456789', 'Hello world!', optionSMS)
```

* Custom data

```python
optionSMS = {
	'user_data': '42'
}
result = api.call('sms.send', 'CALLR', '+33123456789', 'Hello world!', optionSMS);
```

* Delivery Notification

```python
optionSMS = {
	'push_dlr_enabled': true,
	'push_dlr_url': 'http://yourdomain.com/push_delivery_path',
	# 'push_dlr_url_auth': 'login:password' # needed if you use Basic HTTP Authentication
}
result = api.call('sms.send', 'CALLR', '+33123456789', 'Hello world!', optionSMS)
```

**Get an SMS**
```python
result = api.call('sms.get', 'SMSHASH')
```

**Get SMS global options**
```python
result = api.call('sms.get_settings')
```
Return an [SMS.settings](http://thecallr.com/docs/objects/#SMS.Settings) object

**Set SMS global options**

Add options that you want to change in the object
```python
options = {
	'push_dlr_enabled': true,
	'push_dlr_url': 'http://yourdomain.com/push_delivery_path'
}
result = api.call('sms.set_settings', options)
```
Return the updated [SMS.settings](http://thecallr.com/docs/objects/#SMS.Settings) object

***

**Realtime**

* Create REALTIME app with callback URL

```python
options = {
	'url': 'http://yourdomain.com/realtime_callback_url'
}
result = api.call('app.create', 'REALTIME10', 'Your app name', options)
```

* Start a Real-time outbound call

```python
target = {
	'number': '+33132456789',
	'timeout': 30
}

callOptions = {
	'cdr_field': '42',
	'cli': 'BLOCKED'
}

result = api.call('dialr/call.realtime', 'appHash', target, callOptions)
```

***

**List available countries with DID availability**
```python
result = api.call('did/areacode.countries')
```

**Get area codes available for a specific country and DID type**

Check [did/areacode.get_list](http://thecallr.com/docs/api/services/did/areacode/#did/areacode.get_list) for DID type
```python
result = api.call('did/areacode.get_list', 'US', None)
```

**Get DID types available for a specific country**
```python
result = api.call('did/areacode.types', 'US')
```

***

**Create a conference**

Check [conference/10.create_room](http://thecallr.com/docs/api/services/conference/10/#conference/10.create_room) for details
[params](http://thecallr.com/docs/objects/#CONFERENCE10)
[access](http://thecallr.com/docs/objects/#CONFERENCE10.Room.Access)
```python
params = {
	'open': true
}
access = []

result = api.call('conference/10.create_room', 'room name', params, access)
```

* Assign a DID to a room

```python
result = api.call('conference/10.assign_did', 'Room ID', 'DID ID')
```

* Create a PIN protected conference

```python
params = {
	'open': true
}
access = [
	{ 'pin' => '1234', 'level' => 'GUEST' },
	{ 'pin' => '4321', 'level' => 'ADMIN', 'phone_number' => '+33123456789' }
];

result = api.call('conference/10.create_room', 'room name', params, access)
```

* Call a room access

```python
result = api.call('conference/10.call_room_access', 'Room Access ID', 'BLOCKED', true)
```
