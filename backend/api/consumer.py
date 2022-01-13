import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
	def connect(self):
		# accept connection
		self.accept()

	def disconnect(self,close_code):
		pass

	#recieve message from websocket
	def recieve(self,text_data):
