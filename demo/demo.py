

################################################################################
# LOCAL DEPENDENCIES
################################################################################
import shared
from shared import cli
from shared import color




################################################################################
# SOME BASIC TEST FUNCTIONS
################################################################################
def cli_test(args):
	print("Some Stuff")


def cli_color(args):
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


def cli_blink(args):
	print("===" + color.blink("BLINKING") + "===")
	print("===" + color.blink_fast("BLINKING") + "===")


def cli_rgb(args):
	print("===" + color.rgb("COLOR", 50, 100, 255) + "===")
	print("===" + color.bgrgb("COLOR", 255, 100, 50) + "===")

def cli_style(args):
	print("===" + color.italic("Italic") + "===")
	print("===" + color.underline("Underline") + "===")
	print("===" + color.strike("Strike") + "===")
	print("===" + color.overline("Overline") + "===")
	print("===" + color.invert("Invert") + "===")
	print("===" + color.hide("Hidden") + "===")


################################################################################
# RUN THE COMMAND LINE INTERFACE PARSER, AND CALL THE DESIRED FUNCTION/CLASS
################################################################################
cli.run()
cli.success()
