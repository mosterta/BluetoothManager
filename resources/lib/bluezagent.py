from log import log
import xbmc
import xbmcgui
import random

class BluetoothDialog(xbmcgui.Window):
    def __init__(self, device_id, pin):
        super(BluetoothDialog, self).__init__()

        # Erstelle das erste Label für die Gerät-ID
        self.label_device_id = xbmcgui.ControlLabel(50, 50, 300, 100, f"Device-ID: {device_id}", textColor="0xFFFFFFFF")
        self.addControl(self.label_device_id)

        # Erstelle das zweite Label für die PIN, das direkt daneben positioniert ist
        self.label_pin = xbmcgui.ControlLabel(370, 50, 100, 100, f"PIN: {pin}", textColor="0xFFFFFFFF")
        self.addControl(self.label_pin)

    def close_dialog(self):
        self.close()

class BlueZAgentHandler:
	def __init__(self, blueZ):
		self.blueZ = blueZ

	def RequestPinCode(self, message, device):
		log(f"AgentHandler: Pairing request from {device}")
		self.blueZ.return_func(message, "s", "9876")  # Your fixed PIN
		#pin = random.randrange(1000000)
		# Erstelle und zeige das Dialog-Fenster
		#self.dialog = BluetoothDialog(device, pin)
		#self.dialog.show()
		#self.blueZ.return_func(message, "s", str(pin))  # Your fixed PIN

	def Release(self, message):
		log(f"AgentHandler: Release")
		if self.dialog:
			self.dialog.close_dialog()
		self.blueZ.return_func(message)

	def AuthorizeService(self, message, device, uuid):
		log(f"AgentHandler: AuthorizeService {device} {uuid}")
		self.blueZ.return_func(message)

	def Cancel(self, message):
		log(f"AgentHandler: Cancel")
		if self.dialog:
			self.dialog.close_dialog()
		self.blueZ.return_func(message)
		
	def DisplayPin(self, message):
		log(f"AgentHandler: DisplayPin")		

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

