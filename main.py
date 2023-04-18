from subprocess import check_output
from rich.console import Console

console = Console()
datas = check_output(['netsh','wlan', 'show', 'profiles']).decode('utf-8').split('\n')
profiles = []
passwords = []
for data in datas:
	if 'All User Profile' in data:
		profiles.append(data.split(":", 1)[1].strip())
for profile in profiles:
	try:
		data = check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8').split('\n')
		for each in data:
			if 'Key Content' in each:
				passwords.append(each.split(':')[1][1:-1])
	except:
		pass

for profile, password in zip(profiles, passwords):
	console.print(f'[green]{profile}[yellow]|[blue]{password}')

# CyberTitus 2021
