from .console import console
from model.website import sparkWebsite
from utils.readJson import rJ


class menu_login(console):
    '''
    Login function
    '''
    __URL = ''
    __USERNAME = ''
    __PASSWORD = ''

    BROWSER_SESSION = sparkWebsite()

    def do_show(self, arg):
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

        temp = {}
        selection = {}
        num = 1

        if str(arg).startswith("[{") and str(arg).endswith("}]"):
            import json
            p = json.loads(arg)
            for a in p:
                temp[a['baseurl']] = {
                    'email': a['username'], 'pwd': a['password']}
                selection[num] = a['baseurl']
                print(str(num) + "\t: "+selection[num])
                num += 1

        while True:
            inp = input('Type your targeted site number : ')
            i = 0
            try:
                i = int(inp)
            except:
                pass

            if i >= 1 and i <= num:
                url = selection[i]
                em  = temp[url]['email']
                pwd = temp[url]['pwd']
            else:
                print('\nOverload !!!\n')
                url = self.myInput('Url      : ', self.__URL)
                em  = self.myInput('Username : ', self.__USERNAME)
                pwd = self.myInput('Password : ', self.__PASSWORD)

            br = sparkWebsite(url, em, pwd)
            if br.LOGIN_iNFO.isOnLogin():
                print('\nLogin success as %s at \n%s' %
                      (em, br.LOGIN_iNFO.BROWSER.url))
                keyPress = input(
                    'Type `yes` or `ENTER` to set as current session or any key to skip: ')

                if keyPress == 'yes' or keyPress == '':
                    self.BROWSER_SESSION = br

            else:
                print('\nLogin fail')

            print('''
            *   relogin
            x   exit
            ''')

            if input(self.chooselabel) == 'x':
                break
        return self

    def do_save(self, arg):
        '''

        Store current login credential into file setting, 
        e.g. save settings.json

        '''
        url = self.BROWSER_SESSION.LOGIN_iNFO.URL
        em = self.BROWSER_SESSION.LOGIN_iNFO.USERNAME
        pwd = self.BROWSER_SESSION.LOGIN_iNFO.PASSWORD

        if url == '' or em == '' or em == '':
            print('\nCannot read your valid credential, No login session in current state.\nThis action is not available.')
            return self

        rootElement = 'credentials'

        b = []
        a = rJ(arg).read()
        tempCredential = {'username': em, 'password': pwd, 'baseurl': url}
        print(a)
        if hasattr(a, "__getitem__"):
            a = a[rootElement]
            a.append(tempCredential)
            b = a
        else:
            b.append(tempCredential)

        b = {rootElement: b}
        rJ(arg).createFromObject(b).save()

        return self
