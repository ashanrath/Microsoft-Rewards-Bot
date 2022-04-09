# Configuring Telegram updates for MS Reward Bot

To enable Telegram updates, you must 

1. Check/create your Telegram API key and Chat ID. There are multiple ways to do this. One option is via the get_id_bot: https://telegram.me/get_id_bot
2. Open `ms_rewards_telegram_bot.json` and add in your API key and chat ID:
```json
[
	{
		"telegram_apikey": "0123456789:AAAAbbCCCCCCCdddd-eeeeeeeeeeeeeeeee",
		"telegram_chatid": "-0123456789012"
    }	
]
```
3. Save the file.
4. Update [runbot.bat]/[runbot.sh] and add the `--telegram` flag.

Telegram updates should be sent after searches are complete and shown as:
	```
	Update for {email}
		☒ PC  90/90  ☒ Punch Card 100/100
		☒ Mob 60/60  ☒ Quiz       170/170
	Total Points:  XX,XXX
	```


# Optional - Include redemption value of current points

The telegram update can also be used to show the value of any redemption options available with the current point balance.

1. Go to https://rewards.microsoft.com/redeem/shop and confirm the details of any item that you wish to track for.
2. Open `ms_rewards_redeem_options.json.example` and add in the details of any item to be tracked.
```
[
	{
		"type": "Xbox Live",
		"short_desc": "XBL",
		"currency": "$",
		"value": "5",
		"price": "4750"
    },	
	{
		"type": "Other Gift Voucher",
		"short_desc": "GV",
		"currency": "$",
		"value": "5",
		"price": "6750"
    }		
]
```
3. Save the file.


Telegram updates should now include the redemption value the current point balance.

	```
	Update for {email}
		☒ PC  90/90  ☒ Punch Card 100/100
		☒ Mob 60/60  ☒ Quiz       170/170
	Total Points:  10,848 ($10 XBL, $5 GV)
	```

