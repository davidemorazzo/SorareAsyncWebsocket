import websockets
from websockets.exceptions import ConnectionClosed
import asyncio
import json


class SorareWebsocket:

	""" 
	Fully async websocket to create a subscription with Sorare graphql API

	- 	Put your code to be executed on each message in the function _on_message(). In the variable 'data' inside _on_message there
		will be the data sent by the API.
	
	- 	Run the websocket calling: await connectWS(my_query). 
		A good practise is to run this function with asyncio.create_task(connectWS(...)), since the function is
		meant to run forever and simply awaiting it ( await connectWS() ) can be a problem.
	
	"""
	
	def __init__(self) -> None:
		pass

	async def connectWS(self, subscription_query:str):
		
		""" 
		Use this function to create and run forever the websocket.
		"""
		
		if not subscription_query:
			return

		w_socket = 'wss://ws.sorare.com/cable'
		identifier = json.dumps({"channel": "GraphqlChannel"})
		subscription_query_header = {
			"query": subscription_query,
			"variables": {},
			"operationName": "onAnyCardUpdated",
			"action": "execute"
		}

		# Keep connection open forever
		async for ws in websockets.connect(w_socket, ping_interval=60):
			try:
				await self._on_connect(ws, identifier, subscription_query_header)				
				async for message in ws:
					response = json.loads(message)
					if not response.get('type') in ['welcome', 'confirm_subscription']:
						if response.get('type') == 'ping':
							await ws.pong()
						elif response.get('message'):
							if response.get('message').get('result')['data']:
								# On message callback
								asyncio.create_task(self._on_message(response))
						else:
							# Unkown message type
							pass
			
			except ConnectionClosed as e:
				# When a connection is closed with Sorare this exception is raised and the websocket automatically
				# tries to reconnect 
				pass
			except asyncio.CancelledError:
				# If this function is cancelled while it's running via the asyncio task.cancel() method
				# this exception is raised
				return
			except Exception as e:
				pass
		

	async def _on_connect(self, websocket, identifier, query):
		"""
		Send the subscription query to establish the websocket
		"""
		subscribe_command = {"command": "subscribe", "identifier": identifier}
		await websocket.send(json.dumps(subscribe_command).encode())
		await asyncio.sleep(1)
		message_command = {
			"command": "message",
			"identifier": identifier,
			"data": json.dumps(query)
		}
		await websocket.send(json.dumps(message_command).encode())


	
	async def _on_message(self, response):
		"""
		Function executed on message from the WS socket
		"""
		data = response['message']['result']['data']
		if not data:
			return

		## YOUR CODE HERE


