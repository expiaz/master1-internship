!(function () {

    const html = htm.bind(h)

    const state = {
        logs: [],
        devices: [],
        connections: [],
        action: null
    }

    const actions = {
        // server notifications
        
        log: message => ({ logs }) => ({
            logs: [
                ...logs,
                message
            ]
        }),
        updateDevices: devices => ({
            devices
        }),
        updateConnections: connections => ({
            connections
        }),

        // server requests

        startScan: () => {
            ws.emit('attack', {
                type: 'scan'
            })
        }
    }

    const view = (state, actions) => html`
        <main>
            <div class="controls">
                <button onclick=${actions.startScan}>Scan</button>
            </div>

            <h2>Devices</h2>
            <Table data=${state.devices} lineView=${Device} />

            <h2>Connections</h2>
            <Table data=${state.connections} lineView=${Connection} />

            <h2>Logs</h2>
            <div class="logs">
            ${state.logs.map(({ type, message }, i) => html`
                <p class="log ${type}" key=${i}>${message}</p>
            `)}
            </div>
        </main>
    `

    // Components

    const Table = ({ data, lineView }) => !!data.length
        ? html `
            <table>
                <thead>
                    <tr>
                    ${Object.keys(data[0]).map(field => html`
                        <td>${field}</td>
                    `)}
                    </tr>
                </thead>
                <tbody>
                ${data.map(line => lineView(line))}
                </tbody>
            </table>
        `
        : null

    const Device = ({ address, name, company, flags, rssi, txPower, distance }) => html`
        <tr key=${address}>
            <td>${address}</td>
            <td>${name}</td>
            <td>${company}</td>
            <td>${flags.join(', ')}</td>
            <td>${rssi} dBm</td>
            <td>${txPower} dBm</td>
            <td>${distance} meters</td>
        </tr>
    `

    const Connection = ({ accessAddress, rssi }) => html`
        <tr key=${accessAddress}>
            <td>${accessAddress}</td>
            <td>${rssi} dBm</td>
        </tr>
    `

    htm.use([
        Table,
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

    ws.on('devices', main.updateDevices)

    ws.on('connections', main.updateConnections)

})();