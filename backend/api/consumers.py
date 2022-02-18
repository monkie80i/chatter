import json
from channels.generic.websocket import WebsocketConsumer,AsyncJsonWebsocketConsumer

class ChatConsumer(WebsocketConsumer):
	def connect(self):
		# accept connection
		self.accept()

	def disconnect(self,close_code):
		pass

	#recieve message from websocket
	def recieve(self,text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		# send message to WebSocket
		self.send(text_data=json.dumps({'message': message}))

class NotificationConsumer(AsyncJsonWebsocketConsumer):
	async def connect(self):
		# We're always going to accept the connection, though we may
		# close it later based on other factors.
		await self.accept()

	async def notify(self, event):
		"""
		This handles calls elsewhere in this codebase that look
		like:
			channel_layer.group_send(group_name, {
				'type': 'notify',  # This routes it to this handler.
				'content': json_message,
			})

		Don't try to directly use send_json or anything; this
		decoupling will help you as things grow.
		"""
		await self.send_json(event["content"])


	async def receive_json(self, content, **kwargs):
		"""
		This handles data sent over the wire from the client.

		We need to validate that the received data is of the correct
		form. You can do this with a simple DRF serializer.

		We then need to use that validated data to confirm that the
		requesting user (available in self.scope["user"] because of
		the use of channels.auth.AuthMiddlewareStack in routing) is
		allowed to subscribe to the requested object.
		"""

		serializer = self.get_serializer(data=content)
		if not serializer.is_valid():
		    return
		# Define this method on your serializer:
		group_name = serializer.get_group_name()
		# The AsyncJsonWebsocketConsumer parent class has a
		# self.groups list already. It uses it in cleanup.
		self.groups.append(group_name)
		# This actually subscribes the requesting socket to the
		# named group:
		await self.channel_layer.group_add(
		    group_name,
		    self.channel_name,
		)

	def get_serializer(self, *, data):
		"""
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)