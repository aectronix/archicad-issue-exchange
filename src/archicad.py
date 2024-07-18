import json
import tapir_py
import urllib.request

from archicad import ACConnection

class ArchicadWrapper():

	def __init__(self, port=19723):

		self.port = port
		self.commands = None
		self.types = None
		self.utilities = None
		self.tapir = None

		self.connect()

	def connect(self):

		try:
			client = ACConnection.connect(int(self.port))
			commands = client.commands
			if commands.IsAlive():
				self.commands = commands
				self.types = client.types
				self.utilities = client.utilities
				self.tapir = TapirWrapper(port=self.port)
				print(f'Connected to Archicad: {commands.GetProductInfo()}, Tapir: {type(self.tapir)}')
		except Exception as e:
			raise e

class TapirWrapper():

	def __init__(self, host='http://127.0.0.1', port=19723):

		self.host = host
		self.port = port

	def run (self, command, parameters):
	    commandResult = self.run_api_command ('API.ExecuteAddOnCommand', {
	        'addOnCommandId': {
	            'commandNamespace': 'TapirCommand',
	            'commandName': command
	        },
	        'addOnCommandParameters': parameters
	    })
	    if commandResult == None:
	        return None
	    return commandResult['addOnCommandResponse']

	def run_api_command (self, command, parameters):
	    connection_object = urllib.request.Request ('{}:{}'.format (self.host, self.port))
	    connection_object.add_header ('Content-Type', 'application/json')

	    request_data = {
	        'command' : command,
	        'parameters': parameters
	    }
	    request_string = json.dumps (request_data).encode ('utf8')
	    
	    response_data = urllib.request.urlopen (connection_object, request_string)
	    response_json = json.loads (response_data.read())
	    
	    if not response_json['succeeded']:
	        return None
	    
	    return response_json['result']