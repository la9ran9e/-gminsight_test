import tweepy
import time
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

# прослушка твитов   
class MyStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        data_dict = json.loads(data) #извлекаются данные твита и конвертируются в словарь
        location = data_dict['user']['location'] # извлекаются данные геолокации
        # необходимо конвертировать параметр location в параметры широты и долготы, для разметки на карте мира
        if location:
            isConverted = False
            while not isConverted:
                try:
                    location = geolocator.geocode(location)
                    isConverted = True
                except GeocoderTimedOut:
                    isConverted = False
            # после конвертации сохраняем параметры и время твита
            # в виде количества секунд с начала эпохи в словарь
            if location:
                print(location.address)
                print((location.longitude, location.latitude))
                lon = location.longitude
                lat = location.latitude
                if lon and lat:
                    coords = [lon, lat]
                    scatt_dict[time.time()] = coords
        return True

#создаем карту мира, на которую будут нанесены точки
fig = plt.figure(figsize = (25, 10), dpi=250)
plt.title("#gameinsight tweet's around the world")
map_ = Basemap(projection='merc',
                llcrnrlat=-80,
                urcrnrlat=80,
                llcrnrlon=-180,
                urcrnrlon=180,
                lat_ts=20
                )
map_.bluemarble(scale=0.3)
# для real-time карты потребуется заранее создать путой объект scatter 
X = np.array([])
Y = np.array([])
scat = plt.scatter(X, Y)
plt.ion() # карта интерактивная
plt.show()

# проводим аутентификацию для tweeter api
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

scatt_dict = {} #создаем словарь в котором будут храниться время твита и его геолокация
geolocator = Nominatim() # создаем геолокатор для конвертации location в координаты широты и долготы

# прослушка и отметки на карте
while True:
    try:
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
        myStream.filter(track=['#gameinsight'], async = True)
        # добавление и удаление точек на карте
        # решено создать бесконечный цикл, который будет просматривать сохраненые в словаре scatt_dict данные и удалять "просроченные"
        # а после размещать содержимое словаря на карте
        while True:
            X = [] #создаются списки для широты и долготы, в которые будут сохранены конвертированные параметры
            Y = [] # для отображения на карте
            
            scatt_dict_ = dict(scatt_dict)# создается поверхностная копия словаря, так как он может измениться в ходе работы этого участка кода
            for i in scatt_dict_: # обходится список с поиском "просроченных" твитов
                t = time.time() # время просмотра элемента словаря
                if (t - i) >= 1:
                    del scatt_dict[i] # удаление "просроченного" элемента
                else: # если элемент не просрочен, то выкладываем его на карту
                    x, y = map_(scatt_dict[i][0], scatt_dict[i][1])
                    X.append(np.array(x))
                    Y.append(np.array(y))
            scat.set_offsets(np.c_[X, Y])
            plt.pause(0.1)
    except KeyboardInterrupt:
        break
    except:
        continue
