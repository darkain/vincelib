

################################################################################
# EXTERNAL DEPENDENCIES
################################################################################
from	pathlib			import	Path
from	os.path			import	expanduser
from	urllib.request	import	urlopen
from	urllib.parse	import	urlparse
from	subprocess		import	Popen, PIPE, DEVNULL
import	json
import	sys
import	shlex
import	yaml




################################################################################
# LOCAL DEPENDENCIES
################################################################################
from	.				import	text




################################################################################
# GET THE HOME DIRECTORY PATH FOR THE CURRENT USER
################################################################################
def home():
	return Path(expanduser('~'))




################################################################################
# GET THE FILE SYSTEM DIRECTORY PATH OF THE CALLER
################################################################################
def source():
	return Path(sys.path[0])




################################################################################
# GET THE CONTENTS OF A FILE ON THE LOCAL FILE SYSTEM
################################################################################
def read_local(path, mode='r'):
	with open(str(path), mode) as handle:
		return handle.read()




################################################################################
# READ CONTENT OF URL AND RETURN IT AS A STRING
################################################################################
def read_url(url):
	data = urlopen(str(url).replace(' ', '+'))
	return text.from_bytes(data.read())




################################################################################
# RUN A CLI COMMAND AND RETURN ITS STDOUT TEXT
################################################################################
def read_cli(command):
	data = Popen(
		[str(item) for item in command],
		stdout	= PIPE,
		stderr	= DEVNULL,
	)

	return ''.join([text.from_bytes(line) for line in data.stdout])




################################################################################
# GET THE CONTENTS OF A FILE REMOTELY VS SSH
################################################################################
def read_ssh(path):
	parsed = urlparse(str(path))

	return read_cli([
		'ssh', str(parsed.netloc.strip(':')),
		'-oStrictHostKeyChecking=no',
		'cat', str(parsed.path)
	])




################################################################################
# RUN A CLI COMMAND REMOTELY VIA SSH AND RETURN ITS STDOUT TEXT
################################################################################
def read_sshcli(path):
	parsed = urlparse(str(path))

	return read_cli([
		'ssh', str(parsed.netloc.strip(':')),
		'-oStrictHostKeyChecking=no',
		str(parsed.path)
	])




################################################################################
# OPEN A FILE (LOCALLY, REMOTELY, OR VIRTUALLY) AND RETURN ITS CONTENTS
################################################################################
def read(path, mode='r', safe=None):
	try:
		# ESSENTIALLY /dev/null
		if path is None:
			return safe

		# CONVERT TO STRING - USEFUL FOR PATHLIB COMPATIBILITY
		path = str(path)

		# THIS IS A LOCAL FILE, NOT A URL/URI RESOURCE
		if '://' not in path:
			return read_local(path, mode)

		# THIS IS A LOCAL FILE, SPECIFIED BY URL/URI RESOURCE
		if path.startswith('file://'):
			return read_local(path, mode)

		# RUN A COMMAND LOCALLY AND RETURN ITS STDOUT
		if path.startswith('cli://'):
			return read_cli( shlex.split(path[6:]) )

		# SSH REMOTE FILE PATH
		if path.startswith('ssh://'):
			return read_ssh(path)

		# RUN A COMMAND REMOTELY VIA SSH AND RETURN ITS STDOUT
		if path.startswith('ssh+cli://'):
			return read_sshcli(path)

		# ALL OTHER URL/URI SCHEMAS
		return read_url(path)


	except:
		if safe is not None:
			return safe

		# RE-RAISE EXCEPTION, WE'RE NOT IN A DECLARED "SAFE" STATE
		raise




################################################################################
# READ CONTENTS OF A FILE, RETURNING AN EMPTY STRING WHEN EXCEPTIONS HAPPEN
################################################################################
def read_safe(path, mode='r'):
	return str(read(path, mode, ''))




################################################################################
# READ CONTENTS OF A JSON FILE, PARSING JSON AND RETURNING A NATIVE OBJECT
################################################################################
def read_json(path, mode='r', safe=None):
	return json.loads(str(read(path, mode, safe)))




################################################################################
# READ CONTENTS OF A YAML FILE, PARSING YAML AND RETURNING A NATIVE OBJECT
################################################################################
def read_yaml(path, mode='r', safe=None):
	return yaml.safe_load(str(read(path, mode, safe)))
