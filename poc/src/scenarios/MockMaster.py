import os
from mirage.core import scenario
from mirage.libs import io,ble,esb,utils
from mock import MOCK_VALUES

class MockMaster(scenario.Scenario):

	useKeyboard = False

	def onStart(self):

		if 'REQUESTS' in self.module.args and utils.integerArg(self.module.args['REQUESTS'], 0) > 0:
			self.requests = utils.integerArg(self.module.args['REQUESTS'])
		else:
			self.requests = MOCK_VALUES['control']['number_requests']

		if 'INTERVAL' in self.module.args and utils.integerArg(self.module.args['INTERVAL'], 0) > 0:
			self.interval = utils.integerArg(self.module.args['INTERVAL'])
		else:
			self.interval = MOCK_VALUES['control']['request_time_interval']

		if 'PAIRING' in self.module.args:
			self.pairing = utils.booleanArg(self.module.args['PAIRING'])
		else:
			self.pairing = MOCK_VALUES['control']['enable_pairing']

		if 'TARGET' in self.module.args and self.module.args['TARGET'] != '':
			self.target = self.module.args['TARGET']
			io.info('Provided target at ' + self.target)
			self.customConnect()
		else:
			self.target = ""

			if 'NAME' in self.module.args and self.module.args['NAME'] != '':
				self.searchFor = self.module.args['NAME']
			else:
				self.searchFor = MOCK_VALUES['gap']['localName']

			self.module.receiver.onEvent("BLEAdvertisement",callback=self.onAdvertisement)
			self.module.receiver.setScan(enable=True)
			io.info('Scanning for slave named "' + self.searchFor + '"')
		
		return True

	def onAdvertisement(self, packet):
		if self.target != "":
			return

		if packet.type == 'ADV_IND':
			for part in packet.data:
				# search for our slave in GAP adv data
				if hasattr(part, 'local_name') and part.local_name.decode('utf-8') == self.searchFor:
					self.target = packet.addr
		if self.target != "":
			io.success('Found slave at ' + self.target)
			self.module.receiver.setScan(enable=False)
			#self.module.receiver.removeCallbacks()
			#self.module.initializeCallbacks()
			self.customConnect()
		
	def customConnect(self):
		io.info("Trying to connect to slave")
		connectReq = ble.BLEConnect(dstAddr=self.target, type='public')
		self.module.emitter.sendp(connectReq)

	def onSlaveConnect(self):
		io.success('Connected to slave')
		self.requestSlave()

		if self.pairing:
			self.module.pairing(active='active')
			self.requestSlave()

		self.module.disconnect()
		return True

	def requestSlave(self):
		requests = self.requests
		while requests > 0:
			self.module.discover(what='all')
			requests = requests - 1
			utils.wait(seconds=self.interval)

	def onEnd(self):
		return True
	
	def onKey(self,key):
		return True