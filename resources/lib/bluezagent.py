from log import log

class BlueZAgentHandler:
	def __init__(self, blueZ):
		self.blueZ = blueZ

	def RequestPinCode(self, message, device):
		log(f"Pairing request from {device}")
		self.blueZ.return_func(message, "s", "9876")  # Your fixed PIN

	def Release(self, message):
		self.blueZ.return_func(message)

	def AuthorizeService(self, message, device, uuid):
		self.blueZ.return_func(message)

	def Cancel(self, message):
		self.blueZ.return_func(message)

class BlueZAgent:
	def __init__(self, blueZ):
		self.blueZ = blueZ
		self.agent_path = '/org/kodi/btagent'

	def Start(self):
		value = self.blueZ.call_func("org.bluez.AgentManager1", "/org/bluez", "RegisterAgent", "os", self.agent_path, "KeyboardDisplay")
		log(f"result RegisterAgent {value}")
		self.blueZ.call_func("org.bluez.AgentManager1", "/org/bluez", "RequestDefaultAgent", "o", self.agent_path )
		log(f"result RequestDefaultAgent {value}")

	def Stop(self):
		value = self.blueZ.call_func("org.bluez.AgentManager1", "/org/bluez", "UnregisterAgent", "o", self.agent_path)
		log(f"result UnregisterAgent {value}")
