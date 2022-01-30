from flask import Flask
app = Flask(__name__)  
import pymongo
from flask import request
from flask import render_template, render_template_string
import plotly_express as px
import pandas as pd
import json
import plotly

from data_scrap import scrap
from insert_db import insert_value_db

# Page pour erreur 404
@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

# Page d'accueil
@app.route('/')
def index():
     return render_template('hello.html')

# Page pour la liste des drivers
@app.route('/drivers',methods=['GET'])
def show_drivers():
     collection = database['Race']
     # Liste des différents drivers
     cur = collection.distinct("Driver")
     return render_template('drivers.html',cur=cur,name=None)

# Page pour consulter les statistiques d'un driver
@app.route('/drivers/<name>',methods=['GET'])
def show_driver_stats(name):
     collection = database['Race']
     driver = database['Driver']

     # Test pour savoir si le Driver est dans la base de données
     l = collection.aggregate([
          {"$match":{"Driver":name}}
     ])

     if len(list(l))==0:
          return render_template('404.html')
          
     # 10 dernières participations
     par = collection.aggregate([
          {"$match":{"Driver":name}},
          {"$sort":{"Year":-1}},
          {"$limit":10}
     ])

     # Nombre de DNFs par année
     dnf_year = collection.aggregate([
          {"$match":{"Gap_Time":"DNF","Driver":name}},
          {"$group": {"_id":"$Year","Number of DNF":{"$sum":1}}},
          {"$sort":{"_id":1}}
     ])

     # Nombre de DNFs par Grand Prix
     dnf_gp = collection.aggregate([
          {"$match":{"Gap_Time":"DNF","Driver":name}},
          {"$group": {"_id":"$Grand_Prix","Number of DNF":{"$sum":1}}},
          {"$sort":{"Number of DNF":-1}},
          {"$limit":10}
     ])

     # Position moyenne par année
     pos_year = collection.aggregate([
          {"$match":{"Driver":name}},
          {"$group": {"_id":"$Year","Rank Averaged Position":{"$avg":"$Position"}}},
          {"$sort":{"_id":1}}
     ])

     # Position moyenne par Grand Prix
     pos_gp = collection.aggregate([
          {"$match":{"Driver":name}},
          {"$group": {"_id":"$Grand_Prix","Rank Averaged Position":{"$avg":"$Position"}}},
          {"$sort":{"Rank Averaged Position":1}},
          #{"$limit":5}
     ])

     # Nombre de victoires
     wins = len(list(collection.aggregate([
          {"$match":{"Driver":name,"Position":1}}
     ])))

     # Nombre de victoires par année
     win_year = collection.aggregate([
          {"$match":{"Driver":name,"Position":1}},
          {"$group": {"_id":"$Year","Number of wins":{"$sum": 1}}},
          {"$sort":{"_id":1}}
     ])

     # Nombre de victoires par Grand Prix
     win_gp = collection.aggregate([
          {"$match":{"Driver":name,"Position":1}},
          {"$group": {"_id":"$Grand_Prix","Number of wins":{"$sum": 1}}},
          {"$sort":{"Number of wins":-1}}
     ])

     # Nombre de Pole Positions par année
     pol_year = collection.aggregate([
          {"$match":{"Driver":name,"Pos_Qualif":1}},
          {"$group": {"_id":"$Year","Number of Pole Positions":{"$sum": 1}}},
          {"$sort":{"_id":1}},
          #{"$limit":10}
     ])

     # Nombre de Pole Positions
     pols = len(list(collection.aggregate([
          {"$match":{"Driver":name,"Pos_Qualif":1}}
     ])))

     # Nombre de Pole Positions par Grand Prix
     pol_gp = collection.aggregate([
          {"$match":{"Driver":name,"Pos_Qualif":1}},
          {"$group": {"_id":"$Grand_Prix","Number of Pole Positions":{"$sum": 1}}},
          {"$sort":{"Number of Pole Positions":-1}},
          {"$limit":10}
     ])

     # 10 meilleures positions de qualification moyennes par Grand Prix
     avg_qpos = collection.aggregate([
          {"$match":{"Driver":name}},
          {"$group": {"_id":"$Grand_Prix","Averaged Qualifying Position":{"$avg": "$Pos_Qualif"}}},
          {"$sort":{"Averaged Qualifying Position":1}},
          {"$limit":10}
     ])

     # 10 plus grandes vitesses atteintes
     speed = collection.aggregate([
          {"$match":{"Driver":name}},
          {"$sort":{"Avg_Speed":-1}},
          {"$limit":10}
     ])

     # Graphique montrant le nombre de points par année
     data = pd.DataFrame(list(driver.aggregate([
          {"$match":{"Driver":name}},
          {"$group": {"_id":"$Year","Season Standing":{"$sum":"$Season_Standing"},"Total Points":{"$avg":"$Points"}}},
          {"$sort":{"_id":1}}
     ])))
     data = data.rename(columns={"_id":"Year"})
     graph = px.line(data,y="Total Points",x="Year",hover_data=["Year","Season Standing","Total Points"])
     fig = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

     return render_template('drivers.html',name=name, fig=fig, par=par, dnf_year=dnf_year, dnf_gp=dnf_gp, pos_year=pos_year, pos_gp=pos_gp, wins=wins,
                         win_year=win_year, win_gp=win_gp, pols=pols, pol_year=pol_year, pol_gp=pol_gp, avg_qpos=avg_qpos, speed=speed)

# Page pour la liste des équipes
@app.route('/teams',methods=['GET'])
def show_teams():
     collection = database['Race']
     # Liste des différentes équipes
     cur = collection.distinct("Team")

     return render_template('teams.html',cur=cur,name=None)

# Page pour consulter les statistiques d'une équipe
@app.route('/teams/<name>',methods=['GET'])
def show_team_stats(name):
     collection = database['Race']
     team = database['Team']

     # Test pour savoir si l'équipe est dans la base de données
     l = collection.aggregate([
          {"$match":{"Team":name}}
     ])
     if len(list(l))==0:
          return render_template('404.html')
     
     # Nombre de DNFs par driver
     dnf_driver = collection.aggregate([
          {"$match":{"Team":name,"Gap_Time":"DNF"}},
          {"$group": {"_id":"$Driver","Number of DNF":{"$sum":1}}},
          {"$sort":{"_id":-1}},
          {"$limit":10}
     ]) 

     # Position moyenne par année
     rank = collection.aggregate([
          {"$match":{"Team":name}},
          {"$group": {"_id":"$Year","Average Position":{"$avg":"$Position"}}},
          {"$sort":{"_id":1}},
          #{"$limit":20}
     ])

     # 10 meilleurs temps de pitstop
     pit_time = database['Pitstop'].aggregate([
          {"$match":{"Team":name}},
          {"$sort":{"Time_Pit":1}},
          {"$limit":10}
     ])

     # Graphique montrant le nombre de points par année
     data = pd.DataFrame(list(team.aggregate([
          {"$match":{"Team":name}},
          {"$group": {"_id":"$Year","Total Points":{"$avg":"$Points"}}},
          {"$sort":{"_id":1}},
          #{"$limit":20}
     ])))
     data = data.rename(columns={"_id":"Year"})
     graph = px.line(data,y="Total Points",x="Year",hover_data=["Year","Total Points"])
     fig = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
     return render_template('teams.html',fig=fig,name=name,rank=rank,pit_time=pit_time,dnf_driver=dnf_driver)

# Page pour consulter la liste des Grand Prix
@app.route('/gps',methods=['GET'])
def show_gps():
     collection = database['Race']
     # Liste des différents Grand Prix
     cur = collection.distinct("Grand_Prix")

     return render_template('gps.html',cur=cur,name=None,year=None)

# Page pour consulter les statistiques d'un Grand Prix
@app.route('/gps/<name>',methods=['GET'])
def show_gp_stats(name):
     collection = database['Race']
     # Test pour savoir si le Grand Prix est dans la base de données
     l = collection.aggregate([
          {"$match":{"Grand_Prix":name}}
     ])
     if len(list(l))==0:
          return render_template('404.html')

     # Liste des gagnants
     winners = collection.aggregate([
          {"$match":{"Grand_Prix":name,"Position":1}},
          {"$group": {"_id":{"Driver":"$Driver"},"Number of wins":{"$sum":1}}},
          {"$sort":{"Number of win":-1}},
          #{"$limit":20}
     ])

     # Nombre de DNFs par année
     dnf_year = collection.aggregate([
          {"$match":{"Grand_Prix":name,"Gap_Time":"DNF"}},
          {"$group": {"_id":"$Year","Number of DNF":{"$sum":1}}},
          {"$sort":{"_id":1}},
          {"$limit":8}
     ])

     # 10 Drivers avec le plus de DNFs
     dnf_driver = collection.aggregate([
          {"$match":{"Grand_Prix":name,"Gap_Time":"DNF"}},
          {"$group": {"_id":"$Driver","Number of DNF":{"$sum":1}}},
          {"$sort":{"Number of DNF":-1}},
          {"$limit":10}
     ])  

     # 5 tours les plus rapides
     fast_gp = collection.aggregate([
          {"$match":{"Grand_Prix":name}},
          {"$project": {"_id":{"Driver":"$Driver","Year":"$Year"},
                         "Best Lap Time":{
                              "$dateFromString":{
                                   "dateString":"$Lap_Time",
                                   "format":"%M:%S.%LZ",
                                   "onError": '$Lap_Time',
                                   "onNull":"DNF"}
          }}},
          {"$sort":{"Best Lap Time":1}},
          {"$limit":5}
     ])

     # 5 tours les plus rapides en qualification
     fast_qual = collection.aggregate([
          {"$match":{"Grand_Prix":name}},
          {"$project": {"_id":{"Driver":"$Driver","Year":"$Year"},
                         "Best Qualifying Time":{
                              "$dateFromString":{
                                   "dateString":"$Q3",
                                   "format":"%M:%S.%LZ",
                                   "onError": '$Q3',
                                   "onNull":"DNF"}
          }}},
          {"$sort":{"Best Qualifying Time":1}},
          {"$limit":5}
     ])

     # Figure montrant les pneus les plus utilisés
     tyres = pd.DataFrame(list(database['Tyres'].aggregate([
          {"$match":{"Grand_Prix":name}},
          {"$group":{"_id":"$Tyres","Number of sets":{"$sum":1}}},
          {"$sort":{"Number of sets":-1}}
     ])))
     tyres = tyres.rename(columns={"_id":"Tyres"})
     graph_tyres = px.pie(tyres,values="Number of sets",names="Tyres", title="Most frequent tyres used the Grand Prix")
     fig_tyres = json.dumps(graph_tyres, cls=plotly.utils.PlotlyJSONEncoder)

     # Meilleurs temps par année
     best = pd.DataFrame(list(collection.aggregate([
          {"$match":{"Grand_Prix":name,"Position":1}},
          {"$project": {"_id":"$Year",
                    "Time Checkered Flag":{
                         "$dateFromString":{
                              "dateString":"$Gap_Time",
                              "format":"%H:%M:%S.%LZ",
                              "onError": '$Gap_Time',
                              "onNull":"DNF"}
          }}},
          {"$sort":{"_id":1}}
     ])))
     best = best.rename(columns={"_id":"Year"})
     graph = px.bar(best,y="Year",x="Time Checkered Flag")
     fig = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

     # Liste des courses
     races = collection.aggregate([
          {"$match":{"Grand_Prix":name}},
          {"$group":{"_id":"$Year"}},
          {"$sort":{"_id":1}}
     ])

     return render_template('gps.html',fig=fig,fig_tyres = fig_tyres,races=races,name=name,year=None,winners=winners,dnf_year=dnf_year,dnf_driver=dnf_driver,fast_gp=fast_gp,fast_qual=fast_qual,
                         tyres=tyres,best=best)

# Page pour consulter une course
@app.route('/gps/<name>/<year>',methods=['GET'])
def show_race(name,year):
     collection = database['Race']
     # Test pour savoir si la course existe
     try:
          int(year)
     except:
          return render_template('404.html')
     l = collection.aggregate([
          {"$match":{"Grand_Prix":name,"Year":int(year)}}
     ])
     if len(list(l))==0:
          return render_template('404.html')

     # Statistiques de la course
     cur = collection.aggregate([
          {"$match":{"Grand_Prix":name,"Year":int(year)}},
          {"$sort":{"Laps":-1,"Position":1}}
     ])

     return render_template('gps.html',cur=cur,name=name, year=year)

if __name__ == '__main__':
     scrap()
     insert_value_db()
     client = pymongo.MongoClient()
     database = client['projet_f']
     app.run(debug=True, port=2747) 
