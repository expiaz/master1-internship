from mirage.libs import utils

MOCK_VALUES = {
    'gatt': {
        'txPower': 45 # value between -20 and 70 dbm
    },
    'gap': {
        'localName': 'Test slave'
    },
    'control': {
        'number_requests': 1,
        'request_time_interval': 10,
        'enable_pairing': True
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