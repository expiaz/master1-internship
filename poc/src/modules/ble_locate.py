from mirage.core import module
from mirage.libs import utils,ble,io
from collections import deque
from scapy.layers.bluetooth import EIR_Hdr

class ble_locate(module.WirelessModule):
	def init(self):
		self.technology = "ble"
		self.type = "locate"
		self.description = "Localisation of nearby BLE devices from RSSI"
		self.args = {
			'ENVIRONMENT_FACTOR': '2',
			"INTERFACE": "microbit0",
			'TIME': '5',
			'CALLBACK': None,
			'WINDOW': '5'
		}
		self.dependencies = ["ble_sniff"]

	'''
	Approximation of the distance using signal strength indicator from calibrated value using following formulae:
	RSSI = TxPower - 10 * n * log(distance)
	n = ENVIRONMENT_FACTOR
	distance = 10 ^ ((TxPower - RSSI) / (10 * n))
	
	:param rssi: signal strength indicator
	:param txPower: calibrated value measured at 1 meter from the device
	:return: distance in meters from the device
	'''
	def approximateDistance(self, rssi, txPower):
		if txPower is None:
			return None
		if (rssi < 0):
			rssi = -rssi
		return round(pow(10, ((txPower - rssi) / (10 * self.n))), 2)

	def checkAdvertisementsCapabilities(self):
		return self.receiver.hasCapabilities("SNIFFING_ADVERTISEMENTS")

	def checkExistingConnectionCapabilities(self):
		return self.receiver.hasCapabilities("SNIFFING_EXISTING_CONNECTION")

	def onAdvertisement(self, packet):
		if isinstance(packet, ble.BLEAdvertisement) and hasattr(packet, 'additionalInformations'):
			address = packet.addr
			rssi = packet.additionalInformations.rssi
			if address in self.devices:
				self.values[address].append(rssi)
				avg_rssi = round(sum(self.values[address]) / len(self.values[address]))
				if self.devices[address]['rssi'] != avg_rssi:
					self.devices[address]['rssi'] = avg_rssi
					self.devices[address]['distance'] = self.approximateDistance(avg_rssi, self.devices[address]['txPower'])
					self._dirty = True
			else:
				localName = ""
				company = ""
				flags = ""
				txPower = None
				address = packet.addr
				for part in packet.data:
					if hasattr(part, 'level'):
						txPower = part.level
					if hasattr(part, "local_name"):
						localName = part.local_name.decode('ascii','ignore').replace("\0", "")
					elif hasattr(part, "company_id"):
						company = ble.AssignedNumbers.getCompanyByNumber(int(part.company_id))
						if company is None:
							company = ""
					elif hasattr(part,"flags"):
						flags = ble.AssignedNumbers.getStringsbyFlags(part.flags)
				self.devices[address] = {
					'address': address,
					'name': localName,
					'company': company,
					'flags': flags,
					'txPower': txPower,
					'rssi': rssi,
					'distance': self.approximateDistance(rssi, txPower)
				}
				self.values[address] = deque(maxlen=self.windowSize)
				self._dirty = True
			

	def display(self, devices, connections):
		deviceHdr = list(next(iter(devices.values())).keys()) if len(devices) else []
		deviceContent = [list(device.values()) for device in devices.values()]
		io.chart(deviceHdr, deviceContent, "Devices found")
		# io.chart(list(connections.keys()), list(connections.values()), "Connections found")

	def run(self):
		self.emitter = self.getEmitter(interface=self.args['INTERFACE'])
		self.receiver = self.getReceiver(interface=self.args['INTERFACE'])
		self.windowSize = utils.integerArg(self.args['WINDOW'])
		self.n = utils.integerArg(self.args['ENVIRONMENT_FACTOR'])
		self.devices = {}
		self.connections = {}
		# store rssi values over time
		self.values = {}
		self.callback = self.args['CALLBACK'] if callable(self.args['CALLBACK']) else self.display

		self._dirty = False

		if self.checkAdvertisementsCapabilities():
			self.receiver.setSweepingMode(enable=True, sequence=[37,38,39])
			self.receiver.sniffAdvertisements(address="FF:FF:FF:FF:FF:FF")
			self.receiver.onEvent("*", callback=self.onAdvertisement)
			
			remainingTime = utils.integerArg(self.args['TIME']) if self.args["TIME"] != "" else -1
			while remainingTime != 0:
				utils.wait(seconds=1)
				remainingTime -= 1
				if (self._dirty):
					self.callback(self.devices, self.connections)
					self._dirty = False
		else:
			io.fail("Interface provided is not able to sniff advertisements.")

		# Enter your code here.
		return self.ok({})
