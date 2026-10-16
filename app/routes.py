from flask import render_template
from app import app, forms

#register the route into the object "routing table" (URL -> function) 

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Octav'}
    #invokes jinja
    return render_template('index.html', title = 'Home', user=user)

@app.route('/login')
def login():
    form = forms.LoginForm()
    #render.template automatically search for templates in templates folder
    return render_template('login.html', title='Sign In', form=form)

@app.route('/registru')
def registru():
    return render_template('registru.html', title='Registru')
