from mirage.libs import utils

MOCK_VALUES = {
    'gatt': {
        'txPower': 20
    },
    'gap': {
        'localName': 'Test slave'
    }
}

def mockMaster():
    m = utils.loadModule('ble_master')
    m['SCENARIO'] = 'MockMaster'
    m['INTERFACE'] = 'hci1'
    m.execute()

def mockSlave():
    m = utils.loadModule('ble_slave')
    m['SCENARIO'] = 'MockSlave'
    m['INTERFACE'] = 'hci0'
    m.execute()