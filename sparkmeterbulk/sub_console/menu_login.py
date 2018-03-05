from .console import console
from model.website import sparkWebsite
from utils.readJson import rJ


class menu_login(console):
    '''
    Login function
    '''
    __URL         ='kmeter.cloud'
    __USERNAME       ='m.com'
    __PASSWORD    ='zRh3GVr' 

    BROWSER_SESSION = sparkWebsite()


    def do_show(self, arg) :
        '''

        Show current login info
        
        '''
        try:
            print(self.BROWSER_SESSION.LOGIN_iNFO.BROWSER.url)
        except Exception as a:
            print(a.args)
        return self
        
    
    def do_login(self, arg):
        '''
        
        Login to sparkmeter website with username and password

        '''



        while True:
    	    url = self.myInput('Url      : ', self.__URL )
    	    em  = self.myInput('Username : ', self.__USERNAME)
    	    pwd = self.myInput('Password : ', self.__PASSWORD)


    	    br = sparkWebsite(url, em, pwd)
    	    if br.LOGIN_iNFO.isOnLogin() :
    	    	print('\nLogin success as %s at \n%s' % (em, br.LOGIN_iNFO.BROWSER.url))
    	    	keyPress = input('Type `yes` or `ENTER` to set as current session or any key to skip: ')

    	    	if keyPress == 'yes' or keyPress == '':
    	    		self.BROWSER_SESSION= br

    	    else:
    	    	print('\nLogin fail')
                
    	    print('''
            *   relogin
            x   exit
            ''')
            
    	    if input(self.chooselabel) =='x':
                break  
        return self
        
    def do_save(self, arg):
        '''

        Store current login credential into file setting, 
        e.g. save settings.json
        
        '''
        url = self.BROWSER_SESSION.LOGIN_iNFO.URL
        em  = self.BROWSER_SESSION.LOGIN_iNFO.USERNAME
        pwd = self.BROWSER_SESSION.LOGIN_iNFO.PASSWORD

        if url=='' or em=='' or em=='':
            print('\nCannot read your valid credential, No login session in current state.\nThis action is not available.')
            return self

        rootElement ='credentials'


        b=[]
        a = rJ(arg).read()
        tempCredential= {'username':em, 'password':pwd, 'baseurl':url}
        print(a)
        if hasattr(a,"__getitem__") :
            a = a[rootElement]
            a.append(tempCredential)
            b = a
        else:
            b.append(tempCredential)  

        b = {rootElement:b}
        rJ(arg).createFromObject(b).save()      

        return self


