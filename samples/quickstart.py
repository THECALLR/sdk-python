import thecallr

try:
	## initialize instance Thecallr
	# set your credentials or an Exception will raise
	tc = thecallr.Api("login", "password")

	## an optional third parameter let you add options like proxy support
	# proxy must be in url standard format
	# http[s]://user:password@host:port
	# http[s]://host:port
	# http[s]://host

	# options = {
	# 	"proxy": "https://foo:bar@example.com:8080"
	# }
	# tc = thecallr.Api("login", "password", options)


	## Basic example
	# Example to send a SMS
	# 1. "call" method: each parameter of the method as an argument
	tc.call("sms.send", "THECALLR", "+33123456789", "Hello, world", {
		"flash_message": False
	})

	# 2. "send" method: parameter of the method is an array
	my_array = ["THECALLR", "+33123456789", "Hello, world", {
		"flash_message": False
	}]
	tc.send("sms.send", my_array)


	# If you don't pass the correct number of parameter for a method an Exception will raise
	tc.call("sms.send", "THECALLR")

	# Exception will also raise if there is any HTTP error

# Exceptions handler
except (thecallr.ThecallrException, thecallr.ThecallrLocalException) as e:
	print "ERROR: %s" % e.code
	print "MESSAGE: %s" % e.msg
	print "DATA: ", e.data
