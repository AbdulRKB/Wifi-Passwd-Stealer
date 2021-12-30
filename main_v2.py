from subprocess import check_output


def getNames():
    data = check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').splitlines() 
    names = [x.split(':')[1].strip() for x in data if 'All User Profile' in x]
    return names


def getPasswords(names):
    passwords = []
    for i in names:
        data = check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').splitlines()
        passwords+=[x.split(':')[1].strip() for x in data if "Key Content" in x]
        for x in data:
            if 'Absent' in x:
                passwords.append('<blank>')
    return passwords

names = getNames()
passwords = getPasswords(names)



for name, password in zip(names, passwords):
    print(f'{name}:{password}')
