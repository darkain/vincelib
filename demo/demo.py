

################################################################################
# GLOBAL DEPENDENCIES
################################################################################
import json




################################################################################
# LOCAL DEPENDENCIES
################################################################################
import shared
from shared import cli
from shared import color
from shared import file
from shared import html




################################################################################
# SOME BASIC TEST FUNCTIONS
################################################################################
def cli_test():
	print("Some Stuff")


def cli_color():
	print("===" + color.red("RED") + "===")
	print("===" + color.green("GREEN") + "===")
	print("===" + color.blue("BLUE") + "===")
	print("===" + color.cyan("CYAN") + "===")
	print("===" + color.magenta("MAGENTA") + "===")
	print("===" + color.yellow("YELLOW") + "===")

	print("===" + color.bgred(color.black("RED")) + "===")
	print("===" + color.bggreen(color.black("GREEN")) + "===")
	print("===" + color.bgblue(color.black("BLUE")) + "===")
	print("===" + color.bgcyan(color.black("CYAN")) + "===")
	print("===" + color.bgmagenta(color.black("MAGENTA")) + "===")
	print("===" + color.bgyellow(color.black("YELLOW")) + "===")


def cli_blink():
	print("===" + color.blink("BLINKING") + "===")
	print("===" + color.blink_fast("BLINKING") + "===")


def cli_rgb():
	print("===" + color.rgb("COLOR", 50, 100, 255) + "===")
	print("===" + color.bgrgb("COLOR", 255, 100, 50) + "===")

def cli_style():
	print("===" + color.italic("Italic") + "===")
	print("===" + color.underline("Underline") + "===")
	print("===" + color.strike("Strike") + "===")
	print("===" + color.overline("Overline") + "===")
	print("===" + color.invert("Invert") + "===")
	print("===" + color.hide("Hidden") + "===")


def cli_menu():
	data = file.read_json("menu.json")
	print(json.dumps(data, indent=4))



def cli_webdir(args):
	for arg in args:
		print(html.webdir(arg))



################################################################################
# RUN THE COMMAND LINE INTERFACE PARSER, AND CALL THE DESIRED FUNCTION/CLASS
################################################################################
cli.run()
cli.success()
