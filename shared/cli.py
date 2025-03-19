

################################################################################
# EXTERNAL DEPENDENCIES
################################################################################
import	inspect
import	sys




################################################################################
# LOCAL DEPENDENCIES
################################################################################
from	.	import	color
from	.	import	echo




################################################################################
# EXIT CLI INTERFACE
################################################################################
def end(code=None):
	# DO ALL NEEDED CLEANUP
	cleanup.clean_all()

	if code is None:
		code = 0

	sys.exit(int(code))




################################################################################
# EXIT CLI INTERFACE WITH A SUCCESS STATUS CODE
################################################################################
def success():
	end(0)




################################################################################
# EXIT CLI INTERFACE WITH A GENERIC ERROR STATUS CODE
################################################################################
def error():
	end(1)




################################################################################
# GET THE CALLING MODULE
################################################################################
def caller():
	# GET OUR CURRENT FILENAME
	filename = inspect.stack()[0].filename

	# CHECK IF STACK FRAME IS NOT IN THE CURRENT FILE
	for frame in inspect.stack():
		if frame.filename != filename:
			return inspect.getmodule(frame[0])

	# THIS SHOULD NEVER HAPPEN !?
	raise Exception('Python is broken!?')




################################################################################
# GET A LIST OF CALLABLE CLI COMMANDS FROM THE GIVEN MODULE
################################################################################
def commands(module=None, debug=False):
	# DETERMINE CALLING MODULE AUTOMATICALLY
	if module is None:
		module = caller()

	items = []

	for command in dir(module):

		# ONLY INCLUDE INTENDED COMMANDS
		if not command.startswith('cli_'):
			continue

		# OPTIONALLY IGNORE DEBUG RELATED COMMANDS
		if (not debug)  and  (command.endswith('_debug')):
			continue

		# ADD COMMAND TO OUR LIST, STRIPPING cli_ PREFIX
		items.append(command[4:])

	# RETURN THE LIST SORTED, LOOKS CLEANER FOR THE USER!
	return sorted(items)




################################################################################
# DISPLAY HELP TEXT FOR THE CLI COMMAND
################################################################################
def help(module=None, debug=False):
	# DETERMINE CALLING MODULE AUTOMATICALLY
	if module is None:
		module	= caller()

	# PRINT OUT EACH COMMAND FROM MODULE
	for command in commands(module, debug):
		attr	= getattr(module, 'cli_'+command)
		docs	= attr.__doc__ or ''
		echo.line(command.replace('_', '-'), docs.strip())




################################################################################
# EXECUTE THE GIVEN COMMAND
################################################################################
def run(command=None, args=None, module=None):
	if (command is None)  and  (args is None):
		command	= sys.argv[1] if (len(sys.argv) > 1) else 'help'
		args	= sys.argv[2:]

	# DETERMINE CALLING MODULE AUTOMATICALLY
	if module is None:
		module	= caller()

	if command in ('help', '-help', '--help', '---help'):
		return help()


	# GET THE REQUESTED CLASS OR FUNCTION
	try:
		method	= 'cli_' + command.replace('-', '_')
		attr	= getattr(module, method)

	# NOT FOUND, BAIL!
	except:
		echo.error('Unknown Command!', command)
		return error()


	# EXECUTE FUNCTION
	if inspect.isfunction(attr):
		if len(inspect.getfullargspec(attr).args) == 0:
			return attr()
		return attr(args)

	# EXECUTE CLASS METHOD
	if inspect.isclass(attr):
		instance	= _parse(attr(), args)
		validate	= instance.validate()
		if validate is not True:
			print(color.red(color.bold(validate)))
			error()
		return instance.run()

	# THIS SHOULD NEVER HAPPEN !?
	echo.error('Unknown Command!?', command)
	return error()




################################################################################
# PARSE OUT AND ASSIGN ARGUMENT LIST
################################################################################
def _parse(command, args):

	# GET LIST OF EXPECTED COMMAND LINE ARGUMENTS
	members = command.args(flag)

	# STEP THROUGH PROVIDED ARGUMENTS, MATCHING THEM TO EXPECTED ARGUMENTS
	for item in args:
		# FLAGS / PARAMS
		if item.startswith('-'):
			parts		= item.split('=', 1)
			argument	= getattr(command, parts[0].lstrip('-'))
			argument.set(parts[1] if len(parts) > 1 else True)
			continue

		# MAKE SURE WE HAVE ENOUGH ARGS LEFT
		if len(members) < 1:
			raise Exception('Too many arguments!')

		# ARGUMENTS
		argument	= getattr(command, members.pop(0))
		argument.set(item)

	return command




################################################################################
# CLEANUP INSTANCES WHEN CLI IS EXITING
################################################################################
class cleanup():
	instances = []

	def __init__(self):
		cleanup.instances.append(self)

	def __del__(self):
		cleanup.instances.remove(self)

	def clean_all():
		for item in cleanup.instances:
			item.clean()

	def clean(self):
		pass




################################################################################
# BASE CLASS USED FOR CLI COMMANDS
################################################################################
class base():
	class unused:
		pass


	# RECURSIVELY FIND ALL ARGS IN CLASS HIERARCHY
	def _args(item):
		args = []
		for parent in item.__bases__:
			if parent != object:
				args += base._args(parent)
		return args + list(item.__dict__.keys())


	# GET ALL ARGS FOR THIS CLASS
	def args(self, exclude=unused):
		return [
			item for item
			in base._args(type(self))
			if isinstance(getattr(self, item), arg)
			and not isinstance(getattr(self, item), exclude)
		]


	# VALIDATE THAT ARGS HAVE EXPECTED VALUES
	def validate(self):
		for item in self.args():
			valid		= getattr(self, item)
			valid.name	= item
			validate	= valid.validate()
			if validate is not True:
				return item + ': ' + validate
		return True


	# OVERRIDE THIS METHOD, CALLED WHEN RUNNING THIS COMMAND
	def run(self):
		pass




################################################################################
# A SINGLE ARGUMENT ON THE COMMAND LINE
################################################################################
class arg():
	value	= None
	name	= None

	def __str__(self):
		return str(self.value)

	def set(self, value):
		self.value = value

	def get(self):
		return self.value

	def int(self):
		return int(self.value)

	def validate(self):
		return True




################################################################################
# A SINGLE ARGUMENT ON THE COMMAND LINE - THAT IS REQUIRED TO HAVE A VALUE
################################################################################
class arg_required(arg):
	def validate(self):
		return "Missing argument" if self.get() is None else True




################################################################################
# A SINGLE CLI PARAMETER
# example: --recurse
################################################################################
class flag(arg):
	def valuable(self):
		return False




################################################################################
# A SINGLE CLI PARAMETER THAT TAKES A VALUE
# example: --x=1
################################################################################
class param(flag):
	dtype	= None

	def __init__(self, datatype=str):
		self.dtype = datatype

	def set(self, value):
		self.value = self.dtype(value)

	def valuable(self):
		return True
