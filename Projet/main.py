from flask import Flask, make_response, render_template, request
import pymongo
from pymongo import MongoClient

import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

from data_scrap import scrap
from insert_db import insert_value_db






if __name__ == '__main__':
    scrap()
    insert_value_db()




    """app = Flask(__name__)

client = MongoClient(host="mongo", port=27017)

def get_db_race():
    db_race = client['Race']
    return db_race

def get_db_pitstop():
    db_pitstop = client['Pitstop']
    return db_pitstop

def get_db_race():
    db_tyres = client['Tyres']
    return db_tyres


@app.route('/')
def ping_server():
    return "Into plateform"

@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return get_strongest_club(request.args.get('data'))

@app.route('/menu')
def fetch_sku():
    return render_template("menu.html")

@app.route('/driver')
def fetch_sku():
    return render_template("driver.html")

@app.route('/team')
def fetch_sku():
    return render_template("team.html")

@app.route('/grand_prix')
def fetch_sku():
    return render_template("grand_prix.html")




"""