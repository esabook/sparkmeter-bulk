from model.website import sparkWebsite
from utils.readJson import rJ

from sub_console.console import console
from sub_console.menu_customFilter import menu_customFilter
from sub_console.menu_login import menu_login
from controller.meterController import meterController
from controller.meterController import meterState


from pathlib import Path

import json, csv

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
	7	Bulk edit meter by file of `c` (new temp meter info)
	8	Bulk menu

	==========================================================================
	l	Login
	f	Set custom filter
	g	Get meter based on custom filter (f) for current login session (l)
	c	Compare current taken meters by (g) with csv (semicolon delimiters) file 
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
		
		Show current setting file where will be use for bulk operation, default is what inside `settings.json`.
		
		'''
		print(json.dumps( self.settingJson, indent=4))

	def do_2(self, arg):
		'''
		
		Bulk Zeroing credit balance, this program just zeroing credit if current credit value is under zero (0).
		this method is use `current setting to iterate all credentials` availabe on it to access all meters on it.
		important action: 
		1	validate your setting by showing it, `s` command
		s	switch to other file setting, `s some_relatif_file_path.json`

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
		related command: `f`, `g`

		'''
	
		if arg =='':
			state = self.myInput('Input new meter state with `off`/`on`/`auto` or key else to abort: ','auto') 
			if state in ['off','on','auto']:				
				self.currentWebsiteSession.METER.changeAllMeterState(state)
						

		else:
			metersLocal =  rJ(arg).read()
			a=1
			z=len(metersLocal)
			
			for m in metersLocal:
				print('\n\nMeter no %s from %s ; SN = %s ; url = %s' %(a,z, m['meter_serial'], self.currentWebsiteSession.LOGIN_iNFO.URL))
				a += 1
				intState = m['meter_state']

				state = 'off' if intState == 0 else 'on' if intState == 1 else 'auto'
				self.currentWebsiteSession.METER.changeAllMeterState(m['meter_serial'], state)
						
				
	
	def do_5(self, arg):
		'''

		Change meter tarif to other tariff profile,
		related command: `f`, `g`

		Note		: you need valid `tariff profile id` to use this method
		e.g 		: https://web.com/tariff/48b0ee32-cf87-4df4-8ea4-757233a14825/
		tarif id	: 48b0ee32-cf87-4df4-8ea4-757233a14825

		'''

		self.do_help('5')
		
		if arg =='':
			url = self.currentWebsiteSession.LOGIN_iNFO.URL
			if len(url)>0 :
				url += '/tariff'
				import webbrowser
				webbrowser.open(url, new=2)

			tarifId = self.myInput('input valid tarif id and recheck, `enter` or `x` to abort: ', 'x')
			if tarifId !='x':
				self.currentWebsiteSession.METER.changeAllMeterTariff( tarifId )
						
				
		

	def do_6(self, arg):
		'''

		Change meter credit for all meter in current filtered meters
		related command: `f`, `g`

		'''
		tamount 	= input( '%-45s: ' % "Input amount target")
		tmaxmount 	= input( '%-45s: ' % "Input current maximum amount")

		if not tamount.isdigit() or not tmaxmount.isdigit() :
			print("Input is invalid number")
			return
		
		self.currentWebsiteSession.METER.changeAllMeterCredit(float(tamount), float(tmaxmount))
	

	def do_7(self, arg):
		'''
		Push new meter information on temporary file (end result/output) of `c` command,
		e.g: c "d:/myDir/temp_new_meter_info-sparkcloud.json"


		'''

		self.currentWebsiteSession.METER.getMeterInfo(filterJson=self.currentFilter, useFilter=True)
		metersLocal =  rJ(arg).read()
		a=1
		z=len(metersLocal)
			
		for m in metersLocal:
			print('\n\nMeter no %s from %s ; SN = %s ; url = %s' %(a,z, m['meter_serial'], self.currentWebsiteSession.LOGIN_iNFO.URL))
			a += 1
			self.editMeter(m, False)


	def do_8(self, arg):
		'''
		Bulk menu to access bulk script
		hard typed available argument: `reset-protect`, `zero-credit`,  `set-credit` 

		related command: `1`, `2`, `3`

		'''
		if arg == '': 
			print(self.do_help('8'))
		if str(arg) == 'reset-protect':
			self.do_resetprotectall('')
		if str(arg) == 'zero-credit':
			self.do_2('')
		if str(arg) == 'set-credit':
			self.do_3('')
		

	def do_resetprotectall(self, arg):
		'''
		reset all protected meter (meter is in protect state)

		'''
		settings = []
		retries = True
		
		print('Site selection. Type `x` to excluding site.')
		while retries:
			settings = []
			for data in self.settingJson:
				#0 skip disabled config
				if data.get('disabled', False):
					continue
				if str(self.myInput('%-50s: ' % (data['baseurl']),'')).lower() !='x':
					settings.append(data)
			retries = str(input('Type `r` to Retry: ')).lower() == 'r'
		
		if len(settings) == 0 : 
			print('No more action needed.')
			return

		infinite_mode 		= self.myInput('Type `i` to runs in infinite mode for every 30 minutes [or] else to run just once: ', '').lower() == 'i'
		admin_name			= self.myInput('Kindly you must type your long name for your work log? ','')
		
		runs 				= True
		delayed_second	 	= 1800 # int( self.myInput('Type how countdown delay in seconds for infinite mode, default=900 : ', 900))
		import datetime, time
		
		start_time = datetime.datetime.now()
		while runs:
			try:
				if infinite_mode:
					while datetime.datetime.now() < start_time:
						time.sleep(60)

				for data in settings:

					#1 flag for current base url from setting
					print('\n%-50s -----> ' % (data['baseurl']))

					#2 get meter status
					retriesCount = 3
					while retriesCount > 0:
						try:
							self.currentWebsiteSession = sparkWebsite(data['baseurl'], data['username'], data['password'])
							meterStates = self.currentWebsiteSession.METER.getReadLatestState()['readings']
							retriesCount = 0
						except Exception as e:
							print(e)
							retriesCount -=1

					ground_nm = 'ground_name'
					state = 'state'
					sn = 'serial'
					addr ='address'
					for meterstate in meterStates:
						if str(meterstate[state]).lower() == "protect":
							meterstate['access_user'] = admin_name
							meterstate['reset_datetime'] =  datetime.datetime.utcnow()
							gb = meterstate[ground_nm]

							print('Reset for SN: %-25s ADDR: %-50s on GB: %-50s ' % (meterstate[sn], meterstate[addr], gb ))
							self.do_resetprotect(meterstate[sn])
							
							
							header = []
							for key in meterstate.keys():
								header.append(key)

							p = '%s_reset_log.csv' % (gb)
							mode = 'a' if Path(p).exists() else 'w'
							with open( p, mode , newline='') as mFile:
								out = csv.DictWriter(mFile, dialect='excel', fieldnames=header, delimiter=';', quoting=csv.QUOTE_MINIMAL)
								if mode=='w':
									out.writeheader()
								out.writerow(meterstate)

					print('Finish check at %s' % (datetime.datetime.now()))

				start_time = datetime.datetime.now() + datetime.timedelta(seconds=delayed_second)
				runs = infinite_mode
			except Exception as e:
				print(e)
				if self.myInput('Type (Y/N) to terminate current circle? ', 'N').lower() == 'y':
					runs = False
					
	def do_resetprotect(self, arg):
		'''
		non verbose to reset protect of single meter serial on current login session,
		
		note: 	to use this single command, current `login session` must be defined first by `l` command
				and set meter_serial as argumen.
				ex. l login ------> resetprotect SM5R-002-0000000 

		'''
		retries = True
		while retries:
			try:
				self.currentWebsiteSession.METER.resetMeter(arg)
				retries = False
			except Exception as e:
				print(e)
					
			


	def do_d(self, arg):
		'''
		only check customer_code duplication on current meter-list,
		related command: `g`

		'''

		meters = self.meterJsonArray
		duplicate = []
		skipCustName = []
		
		field = 'customer_code'
		savedField = 'meter_serial'
		for m in meters:
			selfCustName = m[field]
			
			if selfCustName not in skipCustName:
				newDup = []
				skipCustName.append(selfCustName)
				for n in meters:
					if n[field] not in skipCustName:
						if n[field] == selfCustName:
							newDup.append(n[savedField])

				if len(newDup) > 0:
					newDuplicateInfo = {}
					newDuplicateInfo[field] 		= selfCustName
					newDuplicateInfo[savedField] 	= newDup
					duplicate.append(newDuplicateInfo)
			
			
		
		Path('duplicated_meter_info-'+self.currentWebsiteSession.LOGIN_iNFO.URL.split('/')[2]+'.json').write_text(str(json.dumps(duplicate, indent=4)))
		

	def do_f(self, arg):
		'''
		
		Manage meter filter. Type `f help` for more help.
		
		'''
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
		-d		Get MeterInfo including customer code, meter coordinate
		-s		Save to Json and CSV

		related command: `l`

		'''
		if arg=='show':
			print(json.dumps(self.meterJsonArray, indent=4))
			print('Total : %i' % (len( self.meterJsonArray)))

		elif arg == '-s':
			self.saveJson(self.currentWebsiteSession.LOGIN_iNFO.URL)	
		else:
			pFilt = self.currentFilter
			if arg == "-d":
				meters = self.currentWebsiteSession.METER.getMeterInfo(pFilt,True).getDetailOfAllMeterlInfo()
			
			else:
				meters = self.currentWebsiteSession.METER.getMeterInfo(filterJson=pFilt, useFilter=True)
			
			self.meterJsonArray = meters.METER_JSONCOLLECTION['meters']
			if input('type `yes` to show ') =='yes':
				self.do_g('show')
			self.do_g('-s')
			
	def do_c(self, arg):
		'''
		!!!!!!!!!!!!!!!!!!!!!! CASE SENSITIVE MODE REQUIRED !!!!!!!!!!!!!!!!!!!!!!!!!
		Compare meter info on current grabbed meter to specific csv (semicolon delimiter)
		required column name: `site_url`, `add?` see comprarison.csv for example

		ex:	l login
			g
			c mycomparisondata.csv

		related command: `g`

		'''
		if not Path(arg.replace('"','')).exists() or arg =='':
			return
		with open(arg.replace('"','')) as csvFile:
			csvReader = csv.DictReader(csvFile, dialect='excel', delimiter=';')
			newMeterInfos =[]
			dik =[]
			for b in csvReader:
				d ={}
				for key, value in b.items():
					d[key]=value
				dik.append(d)
			
			##### iterate all grabbed meters
			a=1
			z=len(self.meterJsonArray)
			
			for m in self.meterJsonArray:
				
				##### print meter index
				print('\n\nMeter no %s from %s ; SN = %s ; url = %s' %(a,z, m['meter_serial'], self.currentWebsiteSession.LOGIN_iNFO.URL))
				a += 1

				##### print header
				print('%-134s????????????  Type `a new value`/ c / l / ~:null / ENTER:skip  ??????????????' % '')
				print('%-32s %-50s %s' % ('', '(c) Cloud Version', '(l) Local version'))
		

				##### finding matches meter serial on csv
				newMeterInfo = {}

				for cm in dik:
					##### compare if found
					if cm.get('meter_serial') == m.get('meter_serial') and cm.get('site_url') in (self.currentWebsiteSession.LOGIN_iNFO.URL) and cm.get('add?', '')=='' :
					
						tempNewMetetInfo = {}
						for key in m:
							value = m.get(key,'')
							cmvalue =cm.get(key,value) 
							if key == 'meter_state':
								try:
									cmvalue = int(cmvalue)
								except:
									pass	
								
							if cmvalue != value:
								inp = input('%-30s : %-50s %-50s <<<<<<<<< ' % (key, value, cmvalue))
								if inp == 'c' or inp == '':
									tempNewMetetInfo[key] = value
								elif inp == 'l':
									tempNewMetetInfo[key] = cmvalue
								else:
									tempNewMetetInfo[key] = inp

						newMeterInfo = tempNewMetetInfo
						print('\n↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓\n')
					
				
				newMeterInfo = {**m, **newMeterInfo}

				for key in m:
					print('%-30s : %-50s %s' % (key, m[key], newMeterInfo.get(key,'')))

				
				if m != newMeterInfo:
					newMeterInfos.append(newMeterInfo)
					if input('Type `s` to send or else to skip anymore : ').lower() == 's':
						self.editMeter(newMeterInfo)
							

			Path('temp_new_meter_info-'+self.currentWebsiteSession.LOGIN_iNFO.URL.split('/')[2]+'.json').write_text(str(json.dumps(newMeterInfos, indent=4)))

	def editMeter(self, meterInfo, verboseMode:bool=True, maxRetry:int=-1):
		retries = True
		retriesElapsed = 0
		while retries:
			if retriesElapsed == maxRetry:
				retries = False
			try:
				self.currentWebsiteSession.METER.editMeterInfo(
								    meterInfo['meter_serial'], **meterInfo)

				retries = False
			except Exception as e:
				print(e)
				if verboseMode:
					if self.myInput("\nType `s` to Skip or else to Retry : ", "").lower() == "s":
						retries = False
			finally:
				if maxRetry > -1:
					retriesElapsed +=1
				

				

	def saveJson(self, url):
		url = str(url)
		if url =='' or len(url.split('/')) <= 2 or self.meterJsonArray == '':
			return
		
		outputFileName = url.split('/')[2]
		inp = input("type `sv` to save to %s -- json and csv file: " % (outputFileName)) 
		if inp =='sv':
			header = []
			for key in self.meterJsonArray[0]:
				header.append(key)

			with open(outputFileName+'.csv', 'w', newline='') as mFile:
				out = csv.DictWriter(mFile, dialect='excel', fieldnames=header, delimiter=';', quoting=csv.QUOTE_MINIMAL)
				out.writeheader()
				out.writerows(self.meterJsonArray)
						

		
			rJ( outputFileName +'.json').createFromObject(self.meterJsonArray).save()
	
	def do_l(self, arg):
		'''

		Login to sparkmeter website, use current settings or enter new characters
		
		'''

		if type(self.__myLogin) != type(menu_login()):
			self.__myLogin = menu_login()

		args = '%s %s' % (arg , str(self.settingJson).replace("'",'"').replace('True', 'true').replace('False', 'false'))
		#TODO support select login from current settings
		self.__myLogin =  self.openChild(self.__myLogin, args)

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
	# retries = True
	# while retries:
	# 	try:
			main().cmdloop()
		# except Exception as e:
		# 	print(e)
		# 	retries = str(input('Type (Q/N) to quit: ')).lower() == 'n'
			
			
	
