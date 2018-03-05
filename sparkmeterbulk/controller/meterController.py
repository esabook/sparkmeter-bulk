from .loginController import login

from enum import Enum

import json
import http.client, urllib


class meterState(Enum):
    off= 0
    on = 1
    auto=2


class meterController():

    def __init__(self, loginSession: login):
        'Initializer with RoboBrowser object, to scapping meters from available login session'
        self.LOGIN_iNFO = loginSession
        self.BROWSER = loginSession.BROWSER
        self.METER_JSONCOLLECTION = {'meters':[]}
        self.METER_FILTER = {}

    def read(self):
        'Read current `METER_JSONCOLLECTION`'
        return self.METER_JSONCOLLECTION

    def getAllMeterInfo(self):
        'Get all available meters on sparkmeter server, return object of myself'
        # 1 
        br = self.BROWSER
        if  br._cursor == -1 : return self

        main_url = br.url
        grab_meter_url = main_url + 'meters.json'

        # 2 
        br.open(grab_meter_url)
        content = json.loads(br.response.text)

        # 3
        content['main_url'] = main_url

        self.METER_JSONCOLLECTION = content
        return self

    def getMeterInfo(self,  filterJson=None, useFilter: bool=False):
        'Return `getAllMeterInfo()` but selected meters is based on filter'
        self.getAllMeterInfo()
        meters = self.METER_JSONCOLLECTION
        tempFilteredMeter=[]

        #4
        if not useFilter or filterJson is None:
            self.METER_JSONCOLLECTION = meters
        else:

            for meter in meters['meters']:
                if self.__compareMeterWithFilter(meter, filterJson):
                    tempFilteredMeter.append(meter)
                else:
                    pass

        meters['meters']=tempFilteredMeter
        self.METER_JSONCOLLECTION = meters
        return self

    def changeAllMeterCredit(self, amountTarget:float, currentMaximumAmount:float):
        '''
        
        Change credit for all meters on current `METER_JSONCOLLECTION` to `amountTarget` and `currentMaximumAmount` filter.
        You can selects meter target with `getMeterInfo` and set filter 
        
        '''
        
        meterInfo = self.METER_JSONCOLLECTION
        if not hasattr(meterInfo,"__getitem__") : return
            
        # 1 iterate all available meter
        for meter in meterInfo['meters']:
            credit = meter['meter_credit_value']
            serial = meter['meter_serial']		
			
            if credit < currentMaximumAmount and credit < amountTarget :
			
				# 2  set meter credit
                print('Meter: %-45s from %-30s => add %-20s' % (serial, credit, abs(amountTarget-credit)),end = "")			

                br = self.changeMeterCredit(serial, abs( amountTarget - credit)) 
                print('http response: %s' % (br.response.status_code))
				
            else:
                print('Meter: %-45s from  %-56s PASS' % (serial, credit))

    def changeAllMeterState(self, newMeterState:str):
        '''
        
        Change meter state for all meters on current `METER_JSONCOLLECTION` to `newMeterState`.
        You can selects meter target with `getMeterInfo` and set filter 
        
        '''
        
        meterInfo = self.METER_JSONCOLLECTION
        if not hasattr(meterInfo,"__getitem__") : return
            
        # 1 iterate all available meter
        for meter in meterInfo['meters']:
            currentState = meter['meter_state']
            serial = meter['meter_serial']		
			
            # 2  set meter state
            print('Meter: %-45s from %-30s => add %-20s' % (serial, currentState, newMeterState), end = "")			

            br = self.changeMeterState(serial, newMeterState) 
            print('http response: %s' % (br.response.status_code))
        
    def changeAllMeterTariff(self, TarifID:str):
        '''Change meter state for all meters on current `METER_JSONCOLLECTION` to `newMeterState`.
        You can selects meter target with `getMeterInfo` and set filter '''
        
        meterInfo = self.METER_JSONCOLLECTION
        if not hasattr(meterInfo,"__getitem__") : return
            
        # 1 iterate all available meter
        for meter in meterInfo['meters']:
            currentTariff = meter['tariff_name']
            serial = meter['meter_serial']		
			
            # 2  set meter credit
            print('Meter: %-45s from %-30s => add %-20s' % (serial, currentTariff, TarifID), end = "")			

            br = self.changeMeterState(serial, TarifID) 
            print('http response: %s' % (br.response.status_code))
				
        

    def changeMeterCredit(self, meter_serial:str, amount:float):
        'Change `amount` meter credit to `meter_serial` (as meter), return RoboBrowser object after sending request'
        br = self.BROWSER
        if  br._cursor == -1 : return br
        
        mainUrl=self.read()['main_url']
        set_meter_url = mainUrl + meter_serial +'/transaction'
        br.open(set_meter_url)
		
        form = br.get_form(id='transaction_form')
        # form['vendor'].value = form['vendor'].options[0].value,				#first customer id, semi-hardcoded
        form['acct_type'].value = 'credit'
        form['source'].value = form['source'].options[2]						#
        form['amount'].value = amount

        br.submit_form(form)
        return br

    def changeMeterState(self, meter_serial:str, relayState:str):
        br = self.BROWSER
        if  br._cursor == -1 : return br
        
        mainUrl=self.read()['main_url']
        url = mainUrl + meter_serial +'/set-state'
        bodyParams = urllib.parse.urlencode({'state': relayState})

        response =br.session.post(url,None,json=bodyParams)
        br._update_state(response)

        return br
    
    def changeMeterTarif(self, meter_serial:str, tarif:str):
        br = self.BROWSER
        if  br._cursor == -1 : return br
        
        mainUrl=self.read()['main_url']
        set_meter_url = mainUrl + meter_serial +'/edit'
        br.open(set_meter_url)
		
        kwargs = {'class':'form form-horizontal'}
        form = br.get_form(None,None,kwargs)
        form['config-tariff'].value = tarif

        print(form['config-state'])
        br.submit_form(form)
        return br












    def __compareMeterWithFilter(self, meterInfo, filterJson:json):
        '''Return true if given `meterInfo` is matches of `filterJson`'''		
        condition = True

        try:
            for met in filterJson.keys():
               
                try:
                    op =  met.split('_?') if '_?' in met else [met,None]
                    
                    if op[0] not in meterInfo: continue

                    mval = meterInfo[op[0]]
                    fval = filterJson[met]
                    condition = self.__compare(mval, op[1], fval) and condition
                    
                except :
                    pass
        except:
            pass
		
        return condition

    def __compare(self,left, operator, right):
        'comparator method to compare given value of `left` and `right` by string of `operator`. Return true/false'
        if	operator == '<'  : return left <    right
        if	operator == '<=' : return left <=   right
        if	operator == '> ' : return left >    right
        if	operator == '>=' : return left >=   right
        if	operator == '!=' : return left !=   right	
        if	operator == '===' : return left ==   right	
        if	operator == '%-' : return left in  right	
        if	operator == '-%' : return right in left
        if	operator == '%!' : return left not in  right	
        if	operator == '!%' : return right not in left

        return right == left
