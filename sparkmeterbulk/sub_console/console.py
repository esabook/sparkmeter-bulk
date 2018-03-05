import cmd
import pip

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])    

class console(cmd.Cmd):
	chooselabel='input your choose:'

	def precmd(self, line):
		import_or_install('robobrowser')
		import_or_install('lxml')
		import_or_install('beautifulsoup4')

	def do_x(self, arg):
		'Close | Exit | Quit | End | Escape'
		return True

	def default(self, line):
		if line != '':
			print('Command for this is not available : %s' % (line))
	
	def openChild(self, childName:cmd.Cmd, arg):
		if arg == '' :
			a = childName.onecmd('help')
		else:
			a = childName.onecmd(arg)
		return a
	def myInput(self, text, defaultRet):
		a = input(text)
		return defaultRet if a == '' else a

