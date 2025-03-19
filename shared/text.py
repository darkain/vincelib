

################################################################################
# EXTERNAL DEPENDENCIES
################################################################################
import secrets
import string




################################################################################
# CONVERT A BYTE ARRAY TO A UTF8 STRING
################################################################################
def from_bytes(data):
	return data.decode('utf8')




################################################################################
# CONVERT A UTF8 STRING TO A BYTE ARRAY
################################################################################
def to_bytes(data):
	return bytes(data, encoding='utf8')




################################################################################
# CHECK IF A VARIABLE IS A STRING
################################################################################
def is_str(data):
	return isinstance(data, str)




################################################################################
# CREATE A CRYPTOGRAPHICALLY SECURE RANDOMLY GENERATED PASSWORD
# https://docs.python.org/3/library/secrets.html#recipes-and-best-practices
################################################################################
def password(count=20, alphabet=None):
	if alphabet is None:
		alphabet = string.ascii_letters + string.digits

	return ''.join(secrets.choice(alphabet) for i in range(count))




################################################################################
# CONVERT NUMBER OF SECONDS INTO HUMAN READABLE DAYS/HOURS/MINUTES/SECONDS
################################################################################
def duration(seconds):
	if seconds is None:
		return 'None'

	seconds			= int(seconds)
	items			= {}

	if seconds == 0:
		return '0 seconds'

	items['day']	= seconds // (60*60*24)
	seconds %= (60*60*24)

	items['hour']	= seconds // (60*60)
	seconds %= (60*60)

	items['minute']	= seconds // 60

	items['second']	= seconds % 60

	return ' '.join(
		(str(value) + ' ' + key + ('s' if value > 1 else ''))
		for key, value
		in items.items()
		if value
	)
