import v20
from datetime import datetime

class brokerEstablish():
    def __self__(self, api_key, acc_id):
        self.api_key = api_key
        self.acc_id = acc_id
        self.api
        
    def connect(self):
        self.api = v20.Context(
              'api-fxpractice.oanda.com',
              '443',
              token='HERE GOES YOUR API KEY')
    def getRate(self):
        latest_price_time = datetime.utcnow().isoformat('T')+'Z'

        response = self.api.pricing.get(
                        self.acc_id,
                        instruments='EUR_USD',
                        since=latest_price_time,
                        includeUnitsAvailable=False)
        
        for price in response.get("prices", 200):
                if latest_price_time is None or price.time > latest_price_time: