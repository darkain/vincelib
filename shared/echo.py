

################################################################################
# LOCAL DEPENDENCIES
################################################################################
from	.	import	color




################################################################################
# PRINT OUT A SINGLE LINE WITH TWO COLUMNS AND COLORS
################################################################################
def line(left, right='', size=19):
	if left  is None: left  = ''
	if right is None: right = ''

	print(
		color.bold(color.green(str(left).ljust(size, ' ')))
		+ " " +
		color.bold(color.blue(str(right)))
	)




################################################################################
# PRINT OUT A SINGLE LINE WITH TWO COLUMNS AND COLORS
################################################################################
def error(left, right='', size=19):
	if left  is None: left  = ''
	if right is None: right = ''

	print(
		color.bold(color.yellow(str(left).ljust(size, ' ')))
		+ " " +
		color.bold(color.red(str(right)))
	)




################################################################################
# PIVOT A ROW TO PRINT IT VERTICALLY
################################################################################
def pivot(data):
	if data is None:
		return

	maxlen = 0

	for item in data:
		maxlen = max(maxlen, len(item))

	for item in data:
		value = data[item]
		if value == '':
			line(item, color.yellow("''"), maxlen)
		elif value is None:
			line(item, color.yellow('None'), maxlen)
		else:
			line(item, value, maxlen)




################################################################################
# PIVOT A BUNCH OF ROWS
################################################################################
def pivotrow(data):
	first	= True
	rownum	= 0

	for row in data:
		if not first: print()
		first = False

		rownum = rownum + 1
		print(color.yellow(color.bold('----- Row: ' + str(rownum) + ' -----')))

		pivot(row)




################################################################################
# PIVOT A SINGLE ROW
################################################################################
def pivotline(data):
	for row in data:
		pivot(row)
		return




################################################################################
# PRINT OUT THE FIRST CELL IN A RESULT SET
################################################################################
def cell(data):
	for row in data:
		for col in row:
			print(color.yellow(row[col]))
			return




################################################################################
# PRINT OUT DATA AS A TABLE
################################################################################
def table(data):
	if len(data) < 1:
		return

	keys	= data[0].keys()
	cols	= {}


	# GET THE LENGTH OF EACH OF THE HEADERS
	for key in keys:
		cols[key] = len(key)


	# GET MAX LENGTH OF EACH COLUMN
	for row in data:
		for key in keys:
			cols[key] = max(cols[key], len(str(row[key])))


	# DISPLAY HEADER ROW
	first = True
	for key in keys:
		if not first: print(color.red(' | '), end='')
		print(color.green(key.ljust(cols[key])), end='')
		first = False
	print()


	# DISPLAY SEPARATOR LINE
	first = True
	for key in keys:
		if not first: print(color.red('-+-'), end='')
		print(color.red('-'.ljust(cols[key], '-')), end='')
		first = False
	print()


	# DISPLAY THE ROW DATA
	for row in data:
		first = True
		for key in keys:
			if not first: print(color.red(' | '), end='')
			print(str(row[key]).ljust(cols[key]), end='')
			first = False
		print()
