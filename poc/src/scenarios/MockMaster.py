import os
from mirage.core import scenario
from mirage.libs import io,ble,esb,utils
from mock import MOCK_VALUES

class MockMaster(scenario.Scenario):

	useKeyboard = False

	def onStart(self):

		# slave_iface = 'hci{}'.format(int(self.args['INTERFACE'][-1:]) + 1)
		# io.info('Using slave interface ' + slave_iface)
		# m = utils.loadModule('ble_info')
		# m['SHOW_CAPABILITIES'] = 'no'
		# m['INTERFACE'] = slave_iface
		# io.info('Recovering ' + slave_iface + ' BD address')
		# result = m.execute()
		# if result['success'] == False:
		# 	io.fail('Failed to recover BD address from interface ' + slave_iface)
		# 	utils.exitMirage()
		
		# iface_info = result['output']
		# iface_bd = iface_info['ADDRESS']
		# io.info('Slave interface (' + slave_iface + ') BD address : ' + iface_bd)

		# m = utils.loadModule('ble_slave')
		# m['INTERFACE'] = slave_iface
		# m['GATT_FILE'] = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/gatt.ini'
		# m['SCENARIO'] = 'MockSlave'
		# m.execute()

		# scan for slave		
		self.target = ""

		self.module.receiver.onEvent("BLEAdvertisement",callback=self.onAdvertisement)
		self.module.receiver.setScan(enable=True)
		
		#self.module.scan(seconds=2)
		#self.module.connect(connectionType="public")
		return True

	def onAdvertisement(self, packet):
		if packet.type == 'ADV_IND':
			for part in packet.data:
				# search for our slave in GAP adv data
				if hasattr(part, 'local_name') and part.local_name.decode('utf-8') == MOCK_VALUES['gap']['localName']:
					self.target = packet.addr
		if self.target != "":
			io.success('Found slave at ' + self.target)
			self.module.receiver.setScan(enable=False)
			self.module.connect(target=self.target, connectionType='public')
		
	def onSlaveConnect(self):
		io.success('Connected to slave')
		# TODO requests
		return True

	def onEnd(self):
		return True
	
	def onKey(self,key):
		return True

	def onSlaveConnectionParameterUpdateRequest(self, packet):
		print('onSlaveConnectionParameterUpdateRequest')
		print(packet.__class__)
		return True