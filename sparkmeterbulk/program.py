from model.website import sparkWebsite
from utils.readJson import rJ

from sub_console.console import console
from sub_console.menu_customFilter import menu_customFilter
from sub_console.menu_login import menu_login

from pathlib import Path

import json

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

class main(console):
	intro = """
	Welcome to 'SparkBulk' for set sparkmeter credit or else
	type 'Help <topic>' for more help

	1	Show setting (sparkmeter credentials)
	2	Bulk Zeroing credit balance 	!!!for all meter on current setting!!!
	3	Bulk Set custom credit balance	!!!for all meter on current setting!!!
	4	Change meter state
	5	Change meter tariff
	6	Create payment to change meter credit

	==========================================================================
	f	Set custom filter
	g	Get meter based on custom filter (f) for current login session (l)
	l	Login
	s	Setting
	x	Exit
	
	"""
	prompt = '(SparkBulk): '
	settingJson = ''
	meterJsonArray	=	[]

	__myLogin	=	menu_login()
	currentWebsiteSession = sparkWebsite()
	
	__myCustomFilter = menu_customFilter()
	currentFilter=''

	def do_1(self, arg):
		'''
		
		Show current setting file
		
		'''
		print(json.dumps( self.settingJson, indent=4))

	def do_2(self, arg):
		'''
		
		Bulk Zeroing credit balance, this program just zeroing credit if current credit value is under zero (0).
		this method is use current setting to iterate all credentials availabe on it to access all meters on it.
		important action: 
		1	validate your setting by showing it
		s	switch to other file setting

		'''
		for data in self.settingJson:
			#0 skip disabled config
			if data.get('disabled', False):
				continue
		
			#1 flag for current base url from setting
			print('\n' + data['baseurl']+'\t:')
		
			#2 get meter 
			loginSession = sparkWebsite(data['baseurl'], data['username'], data['password'])
			loginSession.METER.getAllMeterInfo().changeAllMeterCredit(0,0)
			
	def do_3(self, arg):
		'''

		Bulk to change meter's credit balance relative to their current credit.
		Example: set the `amount target` to 20000 for all meter if the current credit is under 1000 (`current maximum amount`).
		important action: 
		1	validate your setting by showing it
		s	switch to other file setting

		'''
		tamount 	= input( '%-45s: ' % "Input amount target")
		tmaxmount 	= input( '%-45s: ' % "Input current maximum amount")

		if not tamount.isdigit() or not tmaxmount.isdigit() :
			print("Input is invalid number")
			return
		
		for data in self.settingJson:
			#0 skip disabled config
			if data.get('disabled', False):
				continue
		
			#1 flag for current base url from setting
			print('\n' + data['baseurl']+'\t:')
		
			#2 get meter info
			loginSession = sparkWebsite(data['baseurl'], data['username'], data['password'])
			loginSession.METER.getAllMeterInfo().changeAllMeterCredit(float( tamount), float(tmaxmount))
	def do_4(self, arg):
		'''
		
		Change meter state to `off`/`on`/`auto` for all meter in current filtered meters
		see: help f | help g

		'''
		state = self.myInput('Input new meter state with `off`/`on`/`auto` or key else to abort: ','auto') 
		if state in ['off','on','auto']:
			self.currentWebsiteSession.METER.changeAllMeterState(state)
	
	def do_5(self, arg):
		'''

		Change meter tarif to other tariff profile,
		Note		: you need valid `tariff profile id` to use this method
		e.g 		: https://web.com/tariff/48b0ee32-cf87-4df4-8ea4-757233a14825/
		tarif id	: 48b0ee32-cf87-4df4-8ea4-757233a14825

		'''

		self.do_help('5')
		tarifId = self.myInput('input valid tarif id and recheck, `enter` or `x` to abort: ', 'x')
		if tarifId !='x':
			self.currentWebsiteSession.METER.changeAllMeterTariff(tarifId)

	def do_6(self, arg):
		'''

		Change meter credit for all meter in current filtered meters

		'''
		tamount 	= input( '%-45s: ' % "Input amount target")
		tmaxmount 	= input( '%-45s: ' % "Input current maximum amount")

		if not tamount.isdigit() or not tmaxmount.isdigit() :
			print("Input is invalid number")
			return
		
		self.currentWebsiteSession.METER.changeAllMeterCredit(float(tamount), float(tmaxmount))
	
	def do_f(self, arg):
		'Manage meter filter. Type \'f help\' for more help.'
		if type(self.__myCustomFilter) != type(menu_customFilter()):
			self.__myCustomFilter = menu_customFilter()

		self.__myCustomFilter = self.openChild(self.__myCustomFilter,arg)
		if self.__myCustomFilter is not None : 
			self.currentFilter = self.__myCustomFilter.FILTER

	def do_g(self, arg):
		'''
		
		Get filtered meters, this method will get all 
		filtered meters from current login session
		
		show	Showing current filtered meters 
		'''
		if arg=='show':
			print(json.dumps(self.meterJsonArray, indent=4))
		else:
			pFilt = self.currentFilter
			meters = self.currentWebsiteSession.METER.getMeterInfo(filterJson=pFilt, useFilter=True)
			self.meterJsonArray = meters.METER_JSONCOLLECTION['meters']

			if input('type `yes` to show: ') =='yes':
				self.do_g('show')


	def do_l(self, arg):
		'''

		Login to sparkmeter website
		
		'''

		if type(self.__myLogin) != type(menu_login()):
			self.__myLogin = menu_login()

		self.__myLogin =  self.openChild(self.__myLogin,arg)

		if self.__myLogin is not None :
			self.currentWebsiteSession = self.__myLogin.BROWSER_SESSION
		
	def do_s(self, name=''):
		'''
		
		change current setting file to other exist file, 
		e.g. s settings.json

		'''
		defName = 'settings.json'
		name = defName if name=='' or name is None  else name
		if not Path(name).exists() : 
			name = defName

		a=rJ(name).read()
		self.settingJson = a['credentials']

	def precmd(self, line):
		self.do_s()
		return line
	


if __name__ == '__main__':
	main().cmdloop()