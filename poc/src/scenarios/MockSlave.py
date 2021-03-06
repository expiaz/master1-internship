from mirage.core import scenario
from mirage.libs import io,ble,esb,utils
from mirage.libs.bt_utils.assigned_numbers import AD_TYPES
import struct
from mock import MOCK_VALUES

class MockSlave(scenario.Scenario):

	useKeyboard = False

	def onStart(self):
		# Power Level between -100 and 20 dbm
		if "TXPOWER" in self.module.args and utils.integerArg(self.module.args['TXPOWER']) != None:
			self.txPwLvl = struct.pack('<b', utils.integerArg(self.module.args['TXPOWER']))
		else:
			self.txPwLvl = struct.pack('<b', MOCK_VALUES['gatt']['txPower'])

		# Local short name
		if 'NAME' in self.module.args and self.module.args['NAME'] != '':
			self.shortName = self.module.args['NAME'][0:10]
		else:
			self.shortName = MOCK_VALUES['gap']['localName']

		if 'PAIRING' in self.module.args:
			self.pairing = utils.booleanArg(self.module.args['PAIRING'])
		else:
			self.pairing = MOCK_VALUES['control']['enable_pairing']

		if self.pairing:
			self.module.pairing(active='passive')

		self.addPrimaryService()
		self.startAdv()
		return True

	def addPrimaryService(self):
		# Tx Power Level primary service
		self.module.server.addPrimaryService(ble.UUID(name="Tx Power").data)
		# Tx Power Level characteristic
		self.module.server.addCharacteristic(bytes.fromhex('2A07'), self.txPwLvl, permissions=["Read", "Notify"]) # 20 dbm

	def startAdv(self):
		# Advertisement data sent with ADV_IND
		advServices = (ble.UUID(name="Tx Power").data[::-1])
		advData = bytes([
			# Length
			2,
			# Flags data type value.
			0x01,
			# BLE general discoverable, without BR/EDR support.
			0x01 | 0x04,

			# Length
			2,
			# Tx Power Level data type value
			0x0A,
			# Tx Power Level
		]) + self.txPwLvl + bytes([

			# Length
			1 + len(self.shortName),
			# Local short name
			0x08,
			# short name
		]) + str.encode(self.shortName) + bytes([

			# Length
			1 + len(advServices),
			# Complete list of 16-bit Service UUIDs data type value.
			0x03,
			# services
		]) + advServices

		self.module.emitter.setAdvertisingParameters(type='ADV_IND', data=advData)
		self.module.emitter.setAdvertising(enable=True)
		io.info('Currently advertising ' + advData.hex() + ' using ' + self.args['INTERFACE'])

	def onEnd(self):
		return True

	def onKey(self,key):
		return True
