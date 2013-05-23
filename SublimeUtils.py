import sublime, sublime_plugin
import sys, os

if (os.path.join(os.path.dirname(__file__), "lib") in sys.path) == False :
	sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))


class HelloworldCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, self.view.sel()[0].begin(), "Hello, World! ")


class PasteWithSshCommand(sublime_plugin.TextCommand):
	textToSend=None
	router=None
	user=None
	password=None

	def run(self,edit):
		self.textToSend=self.view.substr(self.view.sel()[0])
		sublime.active_window().show_input_panel("Router IP or hostname", "", self.on_router_done, None, None)

	def on_router_done(self,text):
		self.router=text
		sublime.active_window().show_input_panel("Username", "", self.on_user_done, None, None)		

	def on_user_done(self,text):
		self.user=text
		sublime.active_window().show_input_panel("Password", "", self.on_pass_done, None, None)		


	def on_pass_done(self,text):
		self.password=text
		sublime.message_dialog("host: %s user: %s pass: %s text %s"%(self.router,self.user,self.password,self.textToSend))


class CopyForRouterPasteCommand(sublime_plugin.TextCommand):
	textToSend=None

	def run(self,edit):
		self.textToSend=self.view.substr(self.view.sel()[0])
		sublime.active_window().show_input_panel("filename", "", self.on_filename_done, None, None)

	def on_filename_done(self,filename):
		if filename.find(":/") == -1 : 
			filename="flash://"+filename

		sublime.set_clipboard("tclsh\nputs [ open \"%s\" w+ ] {%s}\ntclquit\n"%(filename,self.textToSend))
		sublime.message_dialog("TCL commands to write to file %s have been copied to your clipboard.\nPaste to your telnet/SSH session to write the file."%(filename))
