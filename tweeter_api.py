import tweepy
#import sys
import time
import json
from geopy.geocoders import Nominatim
#from requests.packages.urllib3.exceptions import ReadTimeoutError

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

scatt_dict = {}

fig = plt.figure(figsize=(20, 8), dpi=250)

    # Set a title
plt.title("Tweet's around the world")

    # Declare map projection, size and resolution
map_ = Basemap(projection='merc',
               llcrnrlat=-80,
               urcrnrlat=80,
               llcrnrlon=-180,
               urcrnrlon=180,
               lat_ts=20,
               resolution='l')

map_.bluemarble(scale=0.3)
X = np.array([])
Y = np.array([])
scat = plt.scatter(X, Y)
plt.ion()
plt.show()


geolocator = Nominatim()
#non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
consumer_key = 'ajVeXnXZKlsQPlPUvev1QFOKP'
consumer_secret = 'jIFDHZaNzC3N6RjeemwuHB3hbp7U7fbCcAuljylzkX3iaTsTWU'
access_token = '2774596282-AsDjOBEx5JrxOi89W67qT9h6jc2xsx7Q2KK1kIQ'
access_token_secret = 'AXD0AsMHzjrprE2NsiwBHNJNsBMI40IHbxSgvuVbBac7n'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
#api.update_status('tweepy + oauth!')
alis = []
a = []
del_ = []



class locCat:
    def __init__(self):
        self.index_dict = {}
        self.loc_list = []
        self.add_num = 0
        self.add_order = {}
        

    def curIndex(self, location):
        return self.index_dict[location]

    def lastIndex(self):
        return len(self.loc_list) - 1

    def addLocation(self, location):
        #if location not in self.loc_list:
        self.loc_list.append(location)
        self.index_dict[location] = self.lastIndex()
        self.add_order[self.add_num] = location
        self.add_num += 1
        '''else:
            self.removeLocation_by_order(del_num)
            self.addLocation(location)'''

    def removeLocation_by_order(self, del_num):
        location = self.add_order[del_num]
        del self.add_order[del_num]
        self.removeLocation_by_name(location)
        
    def removeLocation_by_name(self, location):
        cur_index = self.curIndex(location)
        last_index = self.lastIndex()
        if cur_index != last_index:
            self.loc_list[cur_index], self.loc_list[last_index] = \
                                      self.loc_list[last_index], self.loc_list[cur_index]

            self.index_dict[self.loc_list[cur_index]] = cur_index
        self.loc_list.pop()
        del self.index_dict[location]
        
Locations = locCat()            
    
class MyStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        data_dict = json.loads(data)
        #print(data_dict)
        coordinates = data_dict['coordinates']
        location = data_dict['user']['location']
        #print(location)
        if location:
            try:
                location = geolocator.geocode(location)
                print(location.address)
                print((location.longitude, location.latitude))
                lon = location.longitude
                lat = location.latitude
                if lon and lat:
                    coords = [lon, lat]
                    scatt_dict[time.time()] = coords
            except:
                pass
            #Locations.addLocation(location)
            #print(Locations.index_dict)
            #print(Locations.loc_list)
            #print(Locations.add_order)
        return True
    
            
    
    '''def on_status(self, status):
        if isStatus:
            text = status.text
            try:
                print(text)
            except UnicodeEncodeError:
                print('UnicodeEncodeError')
                print(text.translate(non_bmp_map))
            if text:
                alis.append(len(alis))'''

#isStatus = False
while True:
    time.sleep(3)
    try:
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
        '''myStream.filter(track=['game-insight',
                                   '#game-insight', 'gameinsight',
                                   '#gameinsight'], async = True)'''

        myStream.filter(track=['putin', 'Putin'], async = True)

        while True:
            X = []
            Y = []
            scatt_dict_ = dict(scatt_dict)
            for i in scatt_dict_:
                t = time.time()
                if (t - i) >= 1:
                    del scatt_dict[i]
                else:
                    x, y = map_(scatt_dict[i][0], scatt_dict[i][1])
                    #print(x, y)
                    X.append(np.array(x))
                    Y.append(np.array(y))
            scat.set_offsets(np.c_[X, Y])
            plt.pause(0.1)
    except KeyboardInterrupt:
        break
    except:
        continue


        
    
'''del_num = 0
while True:
    time.sleep(10)
    if del_num < Locations.add_num:
        Locations.removeLocation_by_order(del_num)
        del_num += 1
    print(Locations.index_dict)
    print(Locations.loc_list)
    print(Locations.add_order)'''
    

