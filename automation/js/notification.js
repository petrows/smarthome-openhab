/**
 * @file Broadcast notifications.
 *
 * Any command sent to `global_message` is broadcast to all openHAB Cloud
 * (mobile app) clients and to the Telegram bot, then the item is cleared
 * so the same message can be sent again later.
 */

const { rules, triggers, items, actions } = require('openhab');

rules.JSRule({
    name: 'Broadcast message',
    id: 'broadcast-message',
    triggers: [triggers.ItemCommandTrigger('global_message')],
    execute: (event) => {
        const message = event.receivedCommand.replaceAll('\\n', '\n');

        console.warn(message);

        actions.NotificationAction.sendBroadcastNotification(message);
        actions.get('telegram', 'telegram:telegramBot:PWS_Notification').sendTelegram(message);

        // Clear after sending, so an identical message triggers again next time
        items.getItem('global_message').postUpdate('');
    },
});
