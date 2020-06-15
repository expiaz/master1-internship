!(function () {

    let $radar
    function onRadarCreation($el) {
        $radar = $el
    }

    function onLogsUpdate($el) {
        // scroll to bottom of logs list
        $el.scrollTop = $el.scrollHeight;
    }

    const html = htm.bind(h)

    const state = {
        logs: [],
        devices: [{
            type: 'ADV_IND',
            address: '00:45:23:53:43:64',
            name: 'test',
            company: 'John',
            flags: ['adv', 'brd', 'Discoverable over BD/EDR'],
            rssi: -56,
            txPower: -24,
            distance: 0.45
        }, {
            type: 'SCAN_RSP',
            address: '00:FF:FF:FF:FF:FF',
            name: 'iphone',
            company: 'Apple',
            flags: ['adv', 'brd'],
            rssi: -67,
            txPower: -47,
            distance: 0.78
        }],
        connections: [],
        attack: null,
        target: null
    }

    const actions = {
        /**
         * server notifications
         */
        
        log: message => ({ logs }) => ({
            logs: [
                ...logs,
                message
            ]
        }),
        // device scan report
        updateDevices: devices => ({
            devices
        }),
        // connections scan report
        updateConnections: connections => ({
            connections
        }),

        attackFinished: () => ({
            attack: null
        }),

        /**
         * server requests
         */

        startAttack: ({ attack, target }) => {
            ws.emit('startAttack', { attack, target })
            return { attack, target }
        },
        stopAttack: ({ attack, target }) => {
            ws.emit('stopAttack', { attack, target })
            return { attack: null, target: null }
        }
    }

    const colors = '#2980b9,#f1c40f,#1abc9c,#8e44ad,#34495e'.split(',')

    const view = (state, actions) => {
        deviceHdr = 'addres,type,name,company,flags,rssi,txPower,distance,spoofing'.split(',')
        connectionHdr = 'accessAddress,rssi'.split(',')

        let positions = []
        if ($radar && state.devices.length) {
            const padding = 20
            const mapSize = Math.min($radar.offsetWidth, $radar.offsetHeight) - padding
            const descDistances = state.devices.sort((a, b) => b.distance - a.distance)
            const maxRange = descDistances[0].distance

            positions = descDistances.map(({ distance, color = 'red' }, i) => {
                const size = `${distance / maxRange * mapSize}px`
                return html`
                    <div class="position" style=${{'z-index': i + 1, 'width': size, 'height': size, background: colors[i]}}></div>
                `
            })
        }
        // this is our position
        positions.push(
            html`<div class="position" style=${{'z-index': state.devices.length + 1, 'width': '10px', 'height': '10px', background: 'black'}}></div>`
        )
        
        return html`
            <main class="container">
                <div class="content">
                    <div class="controls">
                        <Control attack="scan" />
                    </div>
                    <div class="radar" oncreate=${onRadarCreation}>
                        ${positions}
                    </div>
                    <div class="logs">
                        <h2>Logs</h2>
                        <div class="messages" onupdate=${onLogsUpdate}>
                        ${state.logs.map(({ type, message }, i) => html`
                            <p class="message ${type}" key=${i}>${message}</p>
                        `)}
                        </div>
                    </div>
                </div>
                <div class="lists">
                    <div class="devices">
                        <h2>Devices</h2>
                        <List header=${deviceHdr}>
                            ${state.devices.map(Device)}
                        <//>
                    </div>

                    <div class="connections">  
                        <h2>Connections</h2>
                        <List header=${connectionHdr}>
                            ${state.connections.map(Connection)}
                        <//>
                    </div>
                </div>
            </main>
        `
    }

    // Components

    const Control = ({ attack, target = null }) => (state, actions) => {

        const getAttributes = () => {
            if (state.attack === attack) {
                // current target mismatch, not target of the attack
                if (target !== null && state.target !== target) {
                    return {
                        disabled: true
                    }
                }
                // attack and target matches
                return {
                    onclick: () => {
                        actions.stopAttack({ attack, target })
                    },
                    'class': 'control cancel'
                }
            } else if (state.attack === null) {
                // no attack currently executing
                return {
                    onclick: () => {
                        actions.startAttack({ attack, target })
                    },
                    'class': 'control start'
                }
            } else {
                // not concerned by the attack
                return {
                    disabled: true
                }
            }
        }

        const getWording = () => {
            if (state.attack === attack) {
                // current target mismatch, not target of the attack
                if (target !== null && state.target !== target) {
                    return `Start ${attack}`
                }
                // attack and target matches
                return `Stop ${attack}`
            } else if (state.attack === null) {
                // no attack currently executing
                return `Start ${attack}`
            } else {
                // not concerned by the attack
                return `Start ${attack}`
            }
        }


        return html`
            <button class="control" ... ${getAttributes()}>
                ${getWording()}
            </button>
        `
    }

    const List = ({ header }, children) => h('table', {}, [
        h('thead', {}, [
            h('tr', {}, header.map(
                field => h('td', {}, field)
            ))
        ]),
        h('tbody', {}, children)
    ])

    const Device = ({ address, type, name, company, flags, rssi, txPower, distance }, i) => html`
        <tr key=${address} style=${{background: colors[i]}}>
            <td>${address}</td>
            <td>${type}</td>
            <td>${name}</td>
            <td>${company}</td>
            <td>${flags.join(', ')}</td>
            <td>${rssi} dBm</td>
            <td>${txPower} dBm</td>
            <td>${distance} meters</td>
            <td><Control attack="spoofing" target=${address} /></td>
        </tr>
    `

    const Connection = ({ accessAddress, rssi }) => html`
        <tr key=${accessAddress}>
            <td>${accessAddress}</td>
            <td>${rssi} dBm</td>
            <td><Control attack="hijack" target=${accessAddress} /></td>
        </tr>
    `

    htm.use([
        Control,
        List,
        Device,
        Connection
    ])

    const main = app(state, actions, view, document.body)

    // Socket.IO

    const ws = io()

    ws.on('connect', () => {
        main.log({
            type: 'success',
            message: 'Connected to server'
        })
    })

    ws.on('disconnect', () => {
        main.log({
            type: 'fail',
            message: 'Disconnected from server'
        })
    })

    ws.on('attackFinished', main.attackFinished)

    ws.on('log', main.log)

    ws.on('devicesUpdate', main.updateDevices)

    ws.on('connectionsUpdate', main.updateConnections)

})();