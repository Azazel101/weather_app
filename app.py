import requests
from datetime import datetime,timedelta
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'

db = SQLAlchemy(app)

icons = {
    'clear-day' : 'wi-day-sunny',
    'clear-night' : 'wi-night-clear',
    'rain' : 'wi-rain',
    'snow' : 'wi-snow',
    'sleet' : 'wi-sleet',
    'wind' : 'wi-windy',
    'fog' : 'wi-fog',
    'cloudy' : 'wi-cloud',
    'partly-cloudy-day' : 'wi-day-cloudy',
    'partly-cloudy-night' : 'wi-night-alt-cloudy'
    }

api_key = {
    'darksky' : '8cf0d9b4c83a4030bfaf2c73491334cf',
    'openweathermap' : '3dca0989ce139015bd7f881af1893c5f',
    'opencagedata' : 'd82859da6a3d4320b056ab23ffe5d627'
}

weather_data = []
next_datetime = datetime.now()

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, name, latitude, longitude):
 
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

def get_openweathermap_data(city): # api_key['darksky']
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ city }&units=imperial&appid=' + api_key['openweathermap']
    r = requests.get(url).json()
    return r

def get_darksky_data(latitude, longitude):
    data = str(latitude) +','+ str(longitude)
    url = 'https://api.darksky.net/forecast/' + api_key['darksky'] + '/' + data + '?units=auto'
    r = requests.get(url.format(data)).json()
#    print(r)
    return r

def get_opencagedata(city):
    url = 'https://api.opencagedata.com/geocode/v1/json?q='+ city + '&key=' + api_key['opencagedata']
    r = requests.get(url).json()
    geo = {
    'lat' : r['results'][0]['geometry']['lat'],
    'lng' : r['results'][0]['geometry']['lng']
    }
    return geo

def get_info():
    global weather_data

    weather_data = []

    cities = City.query.all()

    for data in cities:

        r = get_darksky_data(data.latitude, data.longitude)

        wi_icon = icons[str(r['currently']['icon'])]

        weather = {
            'id' : data.id,
            'city' : data.name,
            'latitude' : data.latitude,
            'longitude' : data.longitude,
            'temperature' : r['currently']['temperature'],
            'summary' : r['currently']['summary'],
            'icon' : r['currently']['icon'],
            'wi' : wi_icon
        }

        weather_data.append(weather)
        print(weather)

@app.route('/')
def index_get():
    global next_datetime

    curr_datetime = datetime.now()

    if curr_datetime > next_datetime:
        next_datetime = curr_datetime+timedelta(minutes=5)
        get_info()

    newlist = sorted(weather_data, key=lambda k: k['temperature'])
    return render_template('index.html', weathers=weather_data, weathers_graph=newlist)

@app.route('/list')
def list_place():
    cities = City.query.all()

    all_data = []

    for data in cities:

        data = {
            'id' : data.id,
            'name' : data.name,
            'latitude' : data.latitude,
            'longitude' : data.longitude
        }
        
        all_data.append(data)
#    print(weather_data)
    return render_template('list.html', weathers=all_data)

@app.route('/graph')
def graph():
    legend = 'Actual weather on our Holiday'
    newlist = sorted(weather_data, key=lambda k: k['temperature'])
    return render_template('graph.html',weathers=newlist, legend=legend)
 
@app.route('/temp')
def temp():
    return render_template('temp.html')

@app.route('/api', methods=['POST','GET'])
def api():
    if request.method == 'POST':
        name = request.form.get('name')
        new_key = request.form.get('key')
        api_key[name] = new_key
        flash('API key succesfully updated!')

    return render_template('api.html', apis=api_key)

@app.route('/', methods=['POST'])
def index_post():
    err_msg = ''
    new_city = request.form.get('city')
    new_latitude = request.form.get('latitude')
    new_longitude = request.form.get('longitude')
        
    if new_city:
        existing_city = City.query.filter_by(name=new_city).first()

        if not existing_city:
#            new_city_data = get_darksky_data(new_latitude, new_longitude)

#            if new_city_data['cod'] == 200:
            new_city_obj = City(name=new_city, latitude=new_latitude, longitude=new_longitude)

            db.session.add(new_city_obj)
            db.session.commit()
#            else:
#                err_msg = 'City does not exist in the world!'
        else:
            err_msg = 'City already exists in the database!'

    if err_msg:
        flash(err_msg, 'error')
    else:
        flash('City added succesfully!', 'success')

    return redirect(url_for('index_get'))

@app.route('/edit', methods=['POST'])
def edit_post():
    err_msg = ''
    new_city = request.form.get('city')
    new_latitude = request.form.get('latitude')
    new_longitude = request.form.get('longitude')
        
    if new_city:
        existing_city = City.query.filter_by(name=new_city).first()

        if not existing_city:
#            new_city_data = get_darksky_data(new_latitude, new_longitude)

#            if new_city_data['cod'] == 200:
            new_city_obj = City(name=new_city, latitude=new_latitude, longitude=new_longitude)

            db.session.add(new_city_obj)
            db.session.commit()
#            else:
#                err_msg = 'City does not exist in the world!'
        else:
            err_msg = 'City already exists in the database!'

    if err_msg:
        flash(err_msg, 'error')
    else:
        flash('City added succesfully!', 'success')

    return redirect(url_for('index_get'))

@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        data = City.query.filter_by(id=request.form.get('id')).first()
        data.name = request.form.get('city')
        data.latitude = request.form.get('latitude')
        data.longitude = request.form.get('longitude')
 
        db.session.commit()
        flash('City Updated Successfully', 'success')
        get_info()
 
        return redirect(url_for('index_get'))

@app.route('/delete/<name>')
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Successfully deleted { city.name }', 'success')
    return redirect(url_for('index_get'))

#if __name__ == '__main__':
#    app.run(host='0.0.0.0')
