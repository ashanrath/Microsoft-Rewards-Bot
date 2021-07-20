from msreward.account.login import MSRLogin
from msreward.account.stats import MSRStats


class MSRAccount(MSRLogin, MSRStats):
    
    def __init__(self, browser, email, pswd, otp_secret):
        self._browser = browser
        self.email = email
        self.pswd = pswd
        self.otp_secret = otp_secret
        super().__init__()

    def is_complete(self):
        pass
    