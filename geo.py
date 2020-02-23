from opencage.geocoder import OpenCageGeocode
import requests


key = 'd82859da6a3d4320b056ab23ffe5d627'
geocoder = OpenCageGeocode(key)

query = u'Bratislava'
results = geocoder.geocode(query)

url = 'https://api.opencagedata.com/geocode/v1/json?q=Bratislava&key=d82859da6a3d4320b056ab23ffe5d627&pretty=1'

r = requests.get(url).json()

geo = {
    'lat' : r['results'][0]['geometry']['lat'],
    'lng' : r['results'][0]['geometry']['lng']
}

print(geo)

#print(u'%f;%f;%s;%s' % (results[0]['geometry']['lat'], 
#                        results[0]['geometry']['lng'],
#                        results[0]['components']['country_code'],
#                        results[0]['annotations']['timezone']['name']))