!(function () {

    const html = htm.bind(h)

    const state = {
        logs: [],
        devices: [],
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

    const view = (state, actions) => {
        deviceHdr = 'addres,name,company,flags,rssi,txPower,distance,spoofing'.split(',')
        connectionHdr = 'accessAddress,rssi'.split(',')

        return html`
            <main>
                <div class="controls">
                    <Control attack="scan" />
                </div>

                <h2>Devices</h2>
                <List header=${deviceHdr}>
                    ${state.devices.map(Device)}
                <//>

                <h2>Connections</h2>
                <List header=${connectionHdr}>
                    ${state.connections.map(Connection)}
                <//>

                <h2>Logs</h2>
                <div class="logs">
                ${state.logs.map(({ type, message }, i) => html`
                    <p class="log ${type}" key=${i}>${message}</p>
                `)}
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
                    }
                }
            } else if (state.attack === null) {
                // no attack currently executing
                return {
                    onclick: () => {
                        actions.startAttack({ attack, target })
                    }
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
                    return attack
                }
                // attack and target matches
                return `Stop ${attack}`
            } else if (state.attack === null) {
                // no attack currently executing
                return `Start ${attack}`
            } else {
                // not concerned by the attack
                return attack
            }
        }

        return html`
            <button ... ${getAttributes()}>
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

    const Device = ({ address, name, company, flags, rssi, txPower, distance }) => html`
        <tr key=${address}>
            <td>${address}</td>
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

    window.main = main

    // Socket.IO

    const ws = io()

    ws.on('connect', () => {
        main.log({
            type: 'success',
            message: 'Connected to server'
        })

        ws.emit('test', {
            type: 'test',
            data: 12
        })
    })

    ws.on('disconnect', () => {
        main.log({
            type: 'fail',
            message: 'Disconnected from server'
        })
    })

    ws.on('log', main.log)

    ws.on('updateDevices', main.updateDevices)

    ws.on('updateConnections', main.updateConnections)

})();