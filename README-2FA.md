# using 2FA with MS Reward Bot

To automate the 2FA process, you must register a new time based 2FA for your account. 

1. Follow the steps to register a new time based 2FA until you reach the barcode scan step.
   - Goto https://account.microsoft.com/security
   - Sign in with your Microsoft account
   - Click on "Advanced security options"
   - Click on "Add a new way to sign in"
   - Choose "Use an app" in the pop-up menu   
   - Click on "set up a different Authenticator app"   
   - If it reminds you the risk and ask if you want to continue, click on "Yes/Next/Accept"...   
2. Under the barcode, click on "I can't scan the barcode"
3. Now you should see the Secret key
4. Open `ms_rewards_login_dict.json` and under your credential block, add `"secret": "secretKeyWithoutSpace"`. You must **remove all spaces**. 
```json
[
    {
        "email": "my@email.com",
        "password": "my_password",
        "secret": "secretKeyWithoutSpace"
    }
]
```
5. Save the file.
6. Go back to the webpage, and click on "I'll scan a barcode instead".
7. Scan the barcode with your preferred authenticator app, such as "Google Authenticator" or "Microsoft Authenticator".
8. Follow the instructions and finish the remaining setup.

You can still use your APP for authentication.

Please be aware that your credentials are stored in plain text. You should not share the file with anyone or use the bot in a shared, unsecure environment. Any one with the `secret key` will be able to generate a 2FA token to pass the verfication.