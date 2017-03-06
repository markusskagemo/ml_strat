#!/usr/bin/env python
import v20
from datetime import datetime
from order.view import print_order_create_response_transactions

class brokerEstablish():
    def __init__(self, api_key, acc_id):
        self.api_key = api_key
        self.acc_id = acc_id
        self.api = v20.Context(
              'api-fxpractice.oanda.com', # Hostname
              '443',                      # Port
              token='API KEY')

    def getRate(self):
        latest_price_time = datetime.utcnow().isoformat('T')+'Z'

        response = self.api.pricing.get(
                        self.acc_id,
                        instruments='EUR_USD',
                        since=latest_price_time,
                        includeUnitsAvailable=False)
                        
        # Process the response
        print("Response: {} ({})".format(response.status, response.reason))
        print_order_create_response_transactions(response)

        '''
        for price in response.get("prices", 200):
                if latest_price_time is None or price.time > latest_price_time:
        '''