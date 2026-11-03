from flask import render_template, request
from app import app, forms
import pandas_module as pd_mod
import registry_module as reg_mod
import json

#register the route into the object "routing table" (URL -> function) 
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Octav'}
    #invokes jinja
    return render_template('index.html', title = 'Home', user=user)

@app.route('/index/<name>')
def index_name(name):
    user= {'username': name}
    return render_template('index.html', title='Home', user=user)

@app.route('/login')
def login():
    form = forms.LoginForm()
    #render.template automatically search for templates in templates folder
    return render_template('login.html', title='Sign In', form=form)

@app.route('/registru')
def registru():
    df = pd_mod.get_registry_data()
    pd_mod.format_registry_data(df)
    nr_inreg_list = df['Număr']
    data_list = df['din data']

    return render_template('registru.html', title='Registru', nr_inreg_list=nr_inreg_list, data_list=data_list)

@app.route('/filter')
def filter():
    return render_template('filtru.html')

@app.route('/iesire')
def iesire():
    return render_template('iesire.html')

@app.route('/intrare')
def intrare():
    return render_template('intrare.html')

#methods declare what type of request the route can handle
@app.route('/card-details', methods=['POST'])
def details():
    #request.form = dictionary style containing payload of request.
    #we use get() to not crash if a key does not exist.
    #to implement sql query for the actual document
    nr = request.form.get('number')
    date = request.form.get('datee')
    connection = reg_mod.get_connection()
    with connection.cursor() as cursor:
        stmt = """SELECT iddoc, nrinreg, dtinreg, subnrinreg, subdtinreg, inties, modintrare, tipintrare, termen_zile, termen_data, emitent, emailemitent, nrinregemit, dtinregemit, destinatar, emaildestinatar, compartiment_ies, continut_int,
            continut_ies, repartdanu,repartizat, dtrepar, tipiesire, modexp, solras_danu, solras_data, nrinregdest, dtinregdest, nrinreg_cnx, dtinreg_cnx, inddos, mot_anul, stare, utilizator, last_update FROM registru WHERE nrinreg=%s"""
        cursor.execute(stmt,(nr))
        record = cursor.fetchone()
        print(type(record))
    return render_template('card-details.html', document_number=nr, document_date=date, input_mode=record.get('modintrare'),
        type_mode=record.get('tipintrare'), issuer=record.get('emitent'), nr_issuer=record.get('nrinregemit'), period_days=record.get('termen_zile'),
        period_data=record.get('termen_data'), depart=record.get('repartdanu'), description_in=record.get('continut_intrare'), solutioned=record.get('solras_danu'),
        solutionated_data=record.get('solras_data'), description_out=record.get('continut_ies'), receiver_nr=record.get('nrinregdest'), out_mode=record.get('tip_iesire'),
        nr_dest = record.get('nrinregdest'))
