#!/usr/bin/env python
import oandapyv20 as v20
from datetime import datetime
from order.view import print_order_create_response_transactions
import subprocess

class brokerEstablish():
    def __init__(self, api_key, acc_id):
        self.api_key = api_key
        self.acc_id = acc_id
        self.api = v20.Context(
              'api-fxpractice.oanda.com', # Hostname
              '443',                      # Port
              token='API KEY')

    # Leave since_ as 0 if current rate is wanted. Else input iso-format
    def getRate(self, since_):
        if since_ == 0:
            price_time = datetime.utcnow().isoformat('T')+'Z'
        else:
            price_time = since_

        response = self.api.pricing.get(
                        self.acc_id,
                        instruments='EUR_USD',
                        since=price_time,
                        includeUnitsAvailable=False)
                        
        # Process the response
        print("Response: {} ({})".format(response.status, response.reason))
        print_order_create_response_transactions(response)

        '''
        for price in response.get("prices", 200):
                if latest_price_time is None or price.time > latest_price_time:
        '''
    
    def getRates(self, day):
        return_code = subprocess.call("/C duka -d {}".format(day), shell=True)
        print(return_code)
        
def main(day):
    bE = brokerEstablish()
    bE.getRates(day)
    
if __name__ == "__main__":
    main("2017-02-02")