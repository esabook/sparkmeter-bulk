from .console import console
from utils.readJson import rJ

from pathlib import Path

import json

class menu_customFilter(console):
	intro = '''
	Custom filter,
	filter usage as Json "name_?operator":"value". e.g: 4 "relay_state_?==":"on", "credit_balance_?<=":-2000 
	but you must input to this console like as "name":"operator":"value", type 'help set' for more action
	
	(left : right) is as (current_meter_value : your_filter_value)
	operator:
	'<'  : left  <    	  right
	'<=' : left  <=   	  right
	'> ' : left  >    	  right
	'>=' : left  >=   	  right
	'!=' : left  !=   	  right	
	'===': left	 ==   	  right	
	'%-' : left  in   	  right	
	'-%' : right in   	  left
	'%!' : left  not in   right	
	'!%' : right not in   left
	'''
	prompt='(customFilter):'
	filterFileName=''
	tempFilterJson=''
	FILTER=''

	def do_fn(self, name=''):
		'''
		
		change current filter file to other exist file, 
		e.g. fn filters.json

		'''
		defName = 'filters.json'
		name = defName if name=='' or name is None  else name
		if not Path(name).exists() : name = defName

		self.filterFileName = name
		self.FILTER = rJ(self.filterFileName).read()
		return self

	def do_show(self, arg) :
		'Print current saved filter,  if not show your filter use \'f filename.json\' command to load filter'
		print(json.dumps(self.FILTER, indent=4))
		return self
	

	def do_set(self, args=''):
		'''

		Create a custom filter with these format (modified json format):
		"name_of_element":"operator":int, "name_of_element":"operator":"str", "name_of_element":"operator":bool
		e.g "meter_credit":"<=":23, "meter_serial":"%-":"SM-0076"

		'''
		try:

			self.tempFilterJson = self.filterFromStr(args)

			print('''
			0	show
			1	add more filter
			2	merge to current filter
			3	save as current filter

			h	show help
			x	exit
			''')

			a = ''
			while a not in  ['2','3','x']:
				
				if a=='0':
					print(self.tempFilterJson)

				if a=='1':
					print(
					"""
            		References:
            		"address_city": "Sentani",
            		"address_coords": "",
            		"address_state": "Papua",
            		"address_street1": "Jl. Pos 7",
            		"address_street2": "",
            		"customer_code": "Aryanto",
            		"customer_name": "Aryanto",
            		"customer_phone_number": null,
            		"customer_phone_number_verified": false,
            		"ground_name": "EVI-DevSite-Sentani",
            		"ground_serial": "bTSq1_jS0dOGrnA_xyK9",
            		"meter_active": true,
            		"meter_credit_value": 103000,
            		"meter_debt_value": 0,
            		"meter_is_running_plan": false,
            		"meter_plan_value": 0,
            		"meter_serial": "SM5R-02-0000293A",
            		"meter_state": 1,
            		"meter_tags": "",
            		"tariff_name": "Sumba - BUMDes",
            		"tariff_plan_enabled": true

					Example:
					"address_city":"%!":"Sentani"
					""")
					filterReAdd = input('Input filter: ')
					filterReAdd = self.filterFromStr(filterReAdd)
					if hasattr(filterReAdd, '__getitem__'):
						for efra in filterReAdd:
							self.tempFilterJson[efra] = filterReAdd[efra]
				if a=='h':
					print(self.intro)
					self.do_help('set')
				a =  input(self.chooselabel)
				
			else:
				
				if a=='2':
					currentFilter = self.FILTER
					for fj in  self.tempFilterJson: 
						currentFilter[fj] = self.tempFilterJson[fj]
					
					rJ(self.filterFileName).createFromObject(currentFilter).save()
				
				if a=='3':
					while True:
						filename = input('Enter valid file name: ')
						if Path(filename).exists():
							y = input('File with \'%s\' name exist, type `yes` to replace:'%(filename))
							if y =='yes': break
						elif '.json' in filename:
							break

					rJ(filename).createFromObject(self.tempFilterJson).save()	
		
		except Exception as a:
			print(a)
		return self

	def filterFromStr(self, args=''):
		newFilter= ''
		delim = '":'
		for arg in args.split(','):
			if len(arg.split(delim)) != 3 : 
				print('format invalid => %s' % (arg))
				continue
			arg = arg.split(delim)
			keyValue = '%s_?%s":%s ' % (arg[0], arg[1].replace('"',''), arg[2])
			newFilter += ',' if newFilter != '' else '' + keyValue
		return json.loads('{'+newFilter+'}')

	def do_del(self, arg):
		'''
		
		Delete the element on current saved filter
		
		'''

		fls=self.FILTER
		self.tempFilterJson=self.FILTER
		print('''
		0	show
		1	remove
		x	exit
		''')
		a=''
		while a != 'x':
			for k in fls :
				print('%s : %s' % (k, fls[k]))
				a = input(self.chooselabel)
				if a =='0':
					print(self.tempFilterJson)

				if a == '1':
					del self.tempFilterJson[k]

				if a == 'x':
					break
		if fls == self.tempFilterJson: return
		if input('type \'s\' to save: ') =='s':
			rJ(self.filterFileName).createFromObject(self.tempFilterJson).save()		
		return self

	def precmd(self, line):
		self.do_fn()
		return self
	