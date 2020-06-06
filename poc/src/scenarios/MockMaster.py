import os
from mirage.core import scenario
from mirage.libs import io,ble,esb,utils
from mock import MOCK_VALUES

class MockMaster(scenario.Scenario):

	useKeyboard = False

	def onStart(self):
		self.target = ""

		#self.module.receiver.onEvent("BLEAdvertisement",callback=self.onAdvertisement)
		#self.module.receiver.setScan(enable=True)
		
		self.module.scan(seconds='2')
		self.module.connect(self.module.targets[0])
		return True

	def onAdvertisement(self, packet):
		if self.target != "":
			return

		if packet.type == 'ADV_IND':
			for part in packet.data:
				# search for our slave in GAP adv data
				if hasattr(part, 'local_name') and part.local_name.decode('utf-8') == MOCK_VALUES['gap']['localName']:
					self.target = packet.addr
		if self.target != "":
			io.success('Found slave at ' + self.target)
			self.module.receiver.setScan(enable=False)

			# m = utils.loadModule('ble_connect')
			# m['TARGET'] = self.target
			# m['CONNECTION_TYPE'] = 'public'
			# m['INTERFACE'] = self.args['INTERFACE']
			# m['TIMEOUT'] = '3'
			# ret = m.execute()
			# if ret['success'] == False:
			# 	utils.exitMirage()

			self.module.connect(target=self.target)
		
	def onSlaveConnect(self):
		io.success('Connected to slave')
		self.requestSlave()

		if MOCK_VALUES['control']['enable_pairing']:
			self.module.pairing(active='active')
			self.requestSlave()

		self.module.disconnect()
		return True

	def requestSlave(self):
		requests = MOCK_VALUES['control']['number_requests']
		tick = MOCK_VALUES['control']['request_time_interval']

		# m = utils.loadModule('ble_discover')
		# m['INTERFACE'] = self.args['INTERFACE']
		# m['WHAT'] = 'all'

		while requests > 0:
			self.module.discover(what='all')
			requests = requests - 1
			utils.wait(seconds=tick)
			# ret = m.execute()
			# if ret['success']:
			# 	requests = requests - 1
			# 	utils.wait(seconds=tick)
			# else:
			# 	requests = 0

	def onEnd(self):
		return True
	
	def onKey(self,key):
		return True