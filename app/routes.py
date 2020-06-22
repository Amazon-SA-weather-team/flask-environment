from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from app import app
from app.forms import LoginForm, RegistrationForm, UpdateProfileForm
from app.models import User
from app import db
from werkzeug.urls import url_parse
import requests

@app.route('/')
@app.route('/index')
@login_required
def index():


    # Call API get weather Info
    #currentWeather(current_user.city)
    #fiveDay(current_user.city)

    # Hard code data for code and test use
    data = {'coord': {'lon': -77.39, 'lat': 38.97}, 
    'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 
    'base': 'stations', 
    'main': {'temp': 299.71, 'feels_like': 299.7, 'temp_min': 298.71, 'temp_max': 300.93, 'pressure': 1019, 'humidity': 57}, 
    'visibility': 16093, 
    'wind': {'speed': 3.6, 'deg': 160}, 
    'clouds': {'all': 75}, 
    'dt': 1592505232, 
    'sys': {'type': 1, 'id': 4481, 'country': 'US', 'sunrise': 1592473427, 'sunset': 1592527071}, 
    'timezone': -14400, 
    'id': 4763793, 
    'name': 'Herndon', 
    'cod': 200}


    data['main']['temp'] = round(data['main']['temp'] * 9/5 -459.67, 1)
    data['main']['feels_like'] = round(data['main']['feels_like'] * 9/5 -459.67, 1)
    data['main']['temp_min'] = round(data['main']['temp_min'] * 9/5 -459.67, 1)
    data['main']['temp_max'] = round(data['main']['temp_max'] * 9/5 -459.67, 1)

    return render_template("index.html", title='Home Page', data = data)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        user.address = form.address.data
        user.city = form.city.data
        print(user.city)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you update your profile!')
        return redirect(url_for('index'))
    return render_template('profile.html', title='Profile', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is already have authenticated
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Save User into the database
        user = User(username=form.username.data, email=form.email.data, address=form.address.data, city=form.city.data)
        print(user)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# Get current weather data
def currentWeather(city):

    url = "https://community-open-weather-map.p.rapidapi.com/weather"

    querystring = {"id":"2172797","units":"%22metric%22 or %22imperial%22","mode":"xml%2C html","q":city}

    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': "e0cd5870dcmshdd4c9a6671e756fp12c7f7jsnaa9b5447322b"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    # Convert temp unit
    data['main']['temp'] = round(data['main']['temp'] * 9/5 -459.67, 1)
    data['main']['feels_like'] = round(data['main']['feels_like'] * 9/5 -459.67, 1)
    data['main']['temp_min'] = round(data['main']['temp_min'] * 9/5 -459.67, 1)
    data['main']['temp_max'] = round(data['main']['temp_max'] * 9/5 -459.67, 1)

    return data

# Get five days forecase weather data
def fiveDay(city):
    url = "https://community-open-weather-map.p.rapidapi.com/forecast"

    querystring = {"q":city}

    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': "e0cd5870dcmshdd4c9a6671e756fp12c7f7jsnaa9b5447322b"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()

    # Convert temp unit
    for list in data['list']:
        list['main']['temp'] = round(list['main']['temp'] * 9 / 5 - 459.67, 1)
        list['main']['feels_like'] = round(list['main']['feels_like'] * 9 / 5 - 459.67, 1)
        list['main']['temp_min'] = round(list['main']['temp_min'] * 9 / 5 - 459.67, 1)
        list['main']['temp_max'] = round(list['main']['temp_max'] * 9 / 5 - 459.67, 1)

    return data