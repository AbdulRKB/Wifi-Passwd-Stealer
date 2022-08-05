## Run as Administrator
import re
from subprocess import check_output


class WP:
    '''
    To get all WiFi Names & Passwords, Call the json_data. 
    '''
    def __init__(self):
        self.names = []
        self.passwords = []
        self.command = "netsh wlan show profile "
        self.pattern_name = "All User Profile\s{5}: (.*)\r"
        self.pattern_password = "Key Content\s{12}: (.*)\r"
    
    def getWiFis(self) -> list:
        '''
            Gets WiFi Names
        '''
        data=check_output(self.command).decode()
        wifis=re.findall(self.pattern_name, data)
        return wifis
    
    def getWiFiPasswd(self, name: str) -> str:
        '''
            Gets Password of a Given WiFi Name
        '''
        name+=' key=clear'
        data=check_output(self.command+name).decode()
        try:
            password = re.findall(self.pattern_password, data)[0]
        except IndexError:
            password = '<blank>'
        return password

    def json_data(self):
        data = {}
        names = self.getWiFis()
        passwords = [self.getWiFiPasswd(name) for name in names]
        for name, password in zip(names, passwords):
            data[name] = password
        return data
