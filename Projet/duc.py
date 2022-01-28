from ast import Name
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

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

@app.route('/')
def index():
     return render_template('hello.html')

@app.route('/drivers',methods=['GET'])
def show_drivers():
     collection = database['Race']
     cur = collection.distinct("Driver")
     return render_template('drivers.html',cur=cur,name=None)

@app.route('/drivers/<name>',methods=['GET'])
def show_driver_stats(name):
     collection = database['Race']
     l = collection.aggregate([
          {"$match":{"Driver":name}}
     ])

     if len(list(l))==0:
          return render_template('404.html')
          
     par = collection.aggregate([
          {"$match":{"Driver":name}},
          {"$sort":{"Year":1,"Grand_Prix":1}}
     ])


     dnf_year = collection.aggregate([
          {"$match":{"Gap_Time":"DNF","Driver":name}},
          {"$group": {"_id":"$Year","Number of DNF":{"$sum":1}}},
          {"$sort":{"_id":1}},
          {"$limit":20}
     ])
     dnf_gp = collection.aggregate([
          {"$match":{"Gap_Time":"DNF","Driver":name}},
          {"$group": {"_id":"$Grand_Prix","Number of DNF":{"$sum":1}}},
          {"$sort":{"Number of DNF":-1}},
          {"$limit":20}
     ])
     pos_year = collection.aggregate([
          {"$match":{"Driver":name}},
          {"$group": {"_id":"$Year","Rank Averaged Position":{"$avg":"$Position"}}},
          {"$sort":{"_id":1}},
          #{"$limit":20}
     ])
     pos_gp = collection.aggregate([
          {"$match":{"Driver":name}},
          {"$group": {"_id":"$Grand_Prix","Rank Averaged Position":{"$avg":"$Position"}}},
          {"$sort":{"Rank Averaged Position":1}},
          #{"$limit":5}
     ])

     win_year = collection.aggregate([
          {"$match":{"Driver":name,"Position":1}},
          {"$group": {"_id":"$Year","Number of wins":{"$sum": 1}}},
          {"$sort":{"_id":1}}
     ])

     win_gp = collection.aggregate([
          {"$match":{"Driver":name,"Position":1}},
          {"$group": {"_id":"$Grand_Prix","Number of wins":{"$sum": 1}}},
          {"$sort":{"Number of wins":-1}}
     ])

     pol_year = collection.aggregate([
          {"$match":{"Driver":name,"Pos_Qualif":1}},
          {"$group": {"_id":"$Year","Number of Pole Positions":{"$sum": 1}}},
          {"$sort":{"_id":1}},
          #{"$limit":10}
     ])

     pol_gp = collection.aggregate([
          {"$match":{"Driver":name,"Pos_Qualif":1}},
          {"$group": {"_id":"$Grand_Prix","Number of Pole Positions":{"$sum": 1}}},
          {"$sort":{"Number of Pole Positions":-1}},
          #{"$limit":10}
     ])

     avg_qpos = collection.aggregate([
          {"$match":{"Driver":name}},
          {"$group": {"_id":"$Grand_Prix","Averaged Qualifying Position":{"$avg": "$Pos_Qualif"}}},
          {"$sort":{"Averaged Qualifying Position":1}},
          {"$limit":10}
     ])

     speed = collection.aggregate([
          {"$match":{"Driver":name}},
          {"$sort":{"Avg_Speed":-1}},
          {"$limit":10}
     ])

     data = pd.DataFrame(list(collection.aggregate([
          {"$match":{"Driver":name}},
          {"$group": {"_id":"$Year","Total Points":{"$sum":"$Points"}}},
          {"$sort":{"_id":1}},
          #{"$limit":20}
     ])))
     data = data.rename(columns={"_id":"Year"})
     graph = px.line(data,y="Total Points",x="Year")
     fig = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
     return render_template('drivers.html',name=name, fig=fig, par=par, dnf_year=dnf_year, dnf_gp=dnf_gp, pos_year=pos_year, pos_gp=pos_gp, 
                         win_year=win_year, win_gp=win_gp, pol_year=pol_year, pol_gp=pol_gp, avg_qpos=avg_qpos, speed=speed)


@app.route('/teams',methods=['GET'])
def show_teams():
     collection = database['Race']
     cur = collection.distinct("Team")
     return render_template('teams.html',cur=cur,name=None)

@app.route('/teams/<name>',methods=['GET'])
def show_team_stats(name):
     collection = database['Race']
     l = collection.aggregate([
          {"$match":{"Team":name}}
     ])
     if len(list(l))==0:
          return render_template('404.html')
     par = collection.aggregate([
          {"$match":{"Team":name}},
          {"$sort":{"Year":1,"Grand_Prix":1,"Driver":1}}
     ])

     if len(list(par))==0:
          return render_template('404.html')

     rank = collection.aggregate([
          {"$match":{"Team":name}},
          {"$group": {"_id":"$Year","Average Position":{"$avg":"$Position"}}},
          {"$sort":{"_id":1}},
          #{"$limit":20}
     ])

     pit_time = database['Pitstop'].aggregate([
          {"$match":{"Team":name}},
          {"$sort":{"Time_Pit":1}},
          {"$limit":10}
     ])

     data = pd.DataFrame(list(collection.aggregate([
          {"$match":{"Team":name}},
          {"$group": {"_id":"$Year","Total Points":{"$sum":"$Points"}}},
          {"$sort":{"_id":1}},
          #{"$limit":20}
     ])))
     data = data.rename(columns={"_id":"Year"})
     graph = px.line(data,y="Total Points",x="Year")
     fig = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
     return render_template('teams.html',fig=fig,par=par,name=name,rank=rank,pit_time=pit_time)

@app.route('/gps',methods=['GET'])
def show_gps():
     collection = database['Race']
     cur = collection.distinct("Grand_Prix")
     return render_template('gps.html',cur=cur,name=None,year=None)

@app.route('/gps/<name>',methods=['GET'])
def show_gp_stats(name):
     collection = database['Race']
     l = collection.aggregate([
          {"$match":{"Grand_Prix":name}}
     ])
     if len(list(l))==0:
          return render_template('404.html')

     winners = collection.aggregate([
          {"$match":{"Grand_Prix":name,"Position":1}},
          {"$group": {"_id":{"Driver":"$Driver"},"Number of wins":{"$sum":1}}},
          {"$sort":{"Number of win":-1}},
          #{"$limit":20}
     ])

     dnf_year = collection.aggregate([
          {"$match":{"Grand_Prix":name,"Gap_Time":"DNF"}},
          {"$group": {"_id":"$Year","Number of DNF":{"$sum":1}}},
          {"$sort":{"_id":1}},
     ])

     dnf_driver = collection.aggregate([
          {"$match":{"Grand_Prix":name,"Gap_Time":"DNF"}},
          {"$group": {"_id":"$Driver","Number of DNF":{"$sum":1}}},
          {"$sort":{"Number of DNF":-1}},
          {"$limit":10}
     ])  

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

     tyres = database['Tyres'].aggregate([
          {"$match":{"Grand_Prix":name}},
          {"$group":{"_id":"$Tyres","Number of sets":{"$sum":1}}},
          {"$sort":{"Number of sets":-1}}
     ])

     best = collection.aggregate([
          {"$match":{"Grand_Prix":name,"Position":1}},
          #{"$group":{"_id":"$Year","Time Checkered Flag":{"$avg":"Lap_Time"}}},
          {"$project": {"_id":{"Year":"$Year"},
                    "Time Checkered Flag":{
                         "$dateFromString":{
                              "dateString":"$Lap_Time",
                              "format":"%M:%S.%LZ",
                              "onError": '$Lap_Time',
                              "onNull":"DNF"}
          }}},
          {"$sort":{"_id":1}}
     ])
     races = collection.aggregate([
          {"$match":{"Grand_Prix":name}},
          {"$group":{"_id":"$Year"}},
          {"$sort":{"_id":1}}
     ])

     return render_template('gps.html',races=races,name=name,year=None,winners=winners,dnf_year=dnf_year,dnf_driver=dnf_driver,fast_gp=fast_gp,fast_qual=fast_qual,
                         tyres=tyres,best=best)

@app.route('/gps/<name>/<year>',methods=['GET'])
def show_race(name,year):
     collection = database['Race']
     l = collection.aggregate([
          {"$match":{"Grand_Prix":name,"Year":int(year)}}
     ])
     if len(list(l))==0:
          return render_template('404.html')
     cur = collection.aggregate([
          {"$match":{"Grand_Prix":name,"Year":int(year)}},
          {"$sort":{"Laps":-1,"Position":1}}
     ])

     return render_template('gps.html',cur=cur,name=name, year=year)

if __name__ == '__main__':
     #scrap()
     #insert_value_db()
     client = pymongo.MongoClient()
     database = client['projet_f']
     app.run(debug=True, port=2747) 
