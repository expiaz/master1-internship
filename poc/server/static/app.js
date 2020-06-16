!(function () {

    let $radar
    function onRadarCreation($el) {
        $radar = $el
    }

    function onLogsUpdate($el) {
        // scroll to bottom of logs list
        $el.scrollTop = $el.scrollHeight;
    }

    function getText(attack) {
        switch (attack) {
            case 'scanDevice':
                return 'scan devices'
            case 'scanConnection':
                return 'scan connections'
            default:
                return attack
        }
    }

    const html = htm.bind(h)

    const state = {
        logs: [],
        devices: [{
            address: 'AA:AA:AA:AA:AA:AA',
            type: 'ADV_IND',
            distance: 0.3,
            color: '#d3f4c3'
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

        attackStarted: ({ attack, target }) => state => ({
            attack,
            target,
            ...actions.log({
                'type': 'success',
                'message': `${getText(attack)}${target ? `on ${target}` : ''} started`
            })(state)
        }),

        attackStopped: () => state => ({
            attack: null,
            target: null,
            ...actions.log({
                'type': 'fail',
                'message': `${getText(state.attack)}${state.target ? `on ${state.target}` : ''} stopped`
            })(state)
        }),

        /**
         * server requests
         */

        startAttack: ({ attack, target }) => {
            ws.emit('startAttack', { attack, target })
        },
        stopAttack: ({ attack, target }) => {
            ws.emit('stopAttack', { attack, target })
        }
    }

    window.actions = actions

    const view = (state, actions) => {
        deviceHdr = 'address,type,name,company,flags,rssi,txPower,distance,attack'.split(',')
        connectionHdr = 'accessAddress,rssi,attack'.split(',')

        console.log(state)

        let positions = []
        if ($radar && state.devices.length) {
            const padding = 20
            const mapSize = Math.min($radar.offsetWidth, $radar.offsetHeight) - padding
            const descDistances = state.devices.sort((a, b) => b.distance - a.distance)
            const maxRange = descDistances[0].distance

            positions = descDistances.map(({ distance, color }, i) => {
                const size = `${distance / maxRange * mapSize}px`
                return html`
                    <div class="position" style=${{ zIndex: i + 1, width: size, height: size, background: color}}></div>
                `
            })
        }
        
        return html`
            <main class="container">
                <div class="content">
                    <div class="controls">
                        <Control attack="scanDevice" />
                        <Control attack="scanConnection" />
                    </div>
                    <div class="radar" oncreate=${onRadarCreation}>
                        ${positions}
                        <div class="position origin" style=${{zIndex: state.devices.length + 1}}></div>
                        <Legend devices=${state.devices} />
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
                        <div class="devices-list">
                            <List header=${deviceHdr}>
                                ${state.devices.map(Device)}
                            <//>
                        </div>
                    </div>

                    <div class="connections">  
                        <h2>Connections</h2>
                        <div class="connections-list">
                            <List header=${connectionHdr}>
                                ${state.connections.map(Connection)}
                            <//>
                        </div>
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
                    return `Start ${getText(attack)}`
                }
                // attack and target matches
                return `Stop ${getText(attack)}`
            } else if (state.attack === null) {
                // no attack currently executing
                return `Start ${getText(attack)}`
            } else {
                // not concerned by the attack
                return `Start ${getText(attack)}`
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

    function fmtDft(value, fmt = null, dft = '?') {
        if (value) {
            return fmt || value
        } else {
            return dft
        }
    }

    const Device = ({ address, type, name, company, flags, rssi, txPower, distance, color }) => html`
        <tr key=${address} style=${{background: color}}>
            <td>${address}</td>
            <td>${type}</td>
            <td>${fmtDft(name)}</td>
            <td>${fmtDft(company)}</td>
            <td>${fmtDft(flags, flags, 'None')}</td>
            <td>${fmtDft(rssi, `${rssi} dBm`, '?')}</td>
            <td>${fmtDft(txPower, `${txPower} dBm`, '?')}</td>
            <td>${fmtDft(distance, `${distance} meters`, '?')}</td>
            <td><Control attack="spoof" target=${address} /></td>
        </tr>
    `

    const Connection = ({ accessAddress, rssi }) => html`
        <tr key=${accessAddress}>
            <td>${accessAddress}</td>
            <td>${rssi} dBm</td>
            <td><Control attack="hijack" target=${accessAddress} /></td>
        </tr>
    `

    const Legend = ({ devices }) => {
        const elligibleDevices = devices.filter(({ distance }) => !!distance)
        if (elligibleDevices.length == 0)
            return

        return html`
            <div class="legend" style=${{ zIndex: devices.length + 1 }}>
            ${elligibleDevices.map(({ color, distance }) => html`
                <div>
                    <div class="color" style=${{ background: color }}></div>
                    <div class="distance">${distance}m</div>
                </div>
            `)}
            </div>
        `
    }

    htm.use([
        Control,
        List,
        Device,
        Connection,
        Legend
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
    })

    ws.on('disconnect', () => {
        main.log({
            type: 'fail',
            message: 'Disconnected from server'
        })
    })

    ws.on('attackStarted', main.attackStarted)

    ws.on('attackStopped', main.attackStopped)

    ws.on('log', main.log)

    ws.on('devicesUpdate', main.updateDevices)

    ws.on('connectionsUpdate', main.updateConnections)

})();