from mirage.libs import utils

MOCK_VALUES = {
    'gatt': {
        'txPower': -55 # value between -100 and +20 dbm
    },
    'gap': {
        'localName': 'Test slave'
    },
    'control': {
        'number_requests': 10,
        'request_time_interval': 3,
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