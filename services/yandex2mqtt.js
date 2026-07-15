/** Returns the env value or throws if the variable is not set. */
const requireEnv = (name) => {
    const value = process.env[name];
    if (!value) {
        throw new Error(`Required environment variable ${name} is not set`);
    }
    // console.log(name, ' = ', value);
    return value;
};

module.exports = {
    mqtt: {
        host: requireEnv('SS_MQ_HOST'),
        port: parseInt(requireEnv('SS_MQ_PORT')),
        user: requireEnv('SS_MQ_USER'),
        password: requireEnv('SS_MQ_PASS'),
    },

    https: {
        privateKey: '/etc/ssl/certs/ssl-selfsigned.key',
        certificate: '/etc/ssl/certs/ssl-selfsigned.crt',
        port: 4001,
    },

    clients: [
        {
            id: '1',
            name: 'Yandex',
            clientId: requireEnv('SS_CLIENT_ID'),
            clientSecret: requireEnv('SS_CLIENT_SECRET'),
            isTrusted: false,
        },
    ],

    users: [
        {
            id: '1',
            username: requireEnv('SS_LOCAL_USER'),
            password: requireEnv('SS_LOCAL_PASS'),
            name: 'Administrator',
        },
    ],

    devices: [
        // Please configure with '--devices ./data/devices.js', see 'config.devices.orig.js'
    ],

    notification: [
        {
            skill_id: requireEnv('SS_NOTF_SKILL_ID'),
            oauth_token: requireEnv('SS_NOTF_OAUTH_TOKEN'),
            user_id: '1'
        },
    ]
};
