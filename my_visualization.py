from my_functions import MyFunctions
from gecko_functions import GeckoFunctions
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np

# child class to MyFunctions()
class MyVisualization(MyFunctions):



    def plotGraph(self):
        data = GeckoFunctions.get_coin_data_days(self, 'bitcoin', 'usd', 5000)
        time = []
        price = []
        for i in data['prices']:
            time.append(i[0])
            price.append(i[1])


        plt.yscale('log')
        plt.plot(time, price)
        plt.show()


        #price.append(format(i[1], '.2f'))
        #time.append(self.human_time(i[0].strftime('%d %m %Y %H:%M:%S')))
        #print(str(self.human_time(i[0]).strftime('%d %m %Y %H:%M:%S')) + '\t' + str(format(i[1], '.12f')))
