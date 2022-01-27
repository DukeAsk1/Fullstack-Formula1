import pandas as pd
import pymongo
import json
from datetime import datetime


def insert_value_db():

    try:
        df_race_result = pd.read_json("data_s/race_result.json")
    except:
        print("data_s/race_result.json not found")
        quit()

    try:
        df_pitstop = pd.read_json("data_s/pit_stop.json")
    except:
        print("data_s/pit_stop.json not found")
        quit()
    try:
        df_qualif_before = pd.read_json("data_s/qualif.json")
    except:
        print("data_s/qualif.json not found")
        quit()
    try:
        df_fastest_a = pd.read_json("data_s/fastest_a.json")
    except:
        print("data_s/fastest_a.json not found")
        quit()
    try:
        df_fastest_b = pd.read_json("data_s/fastest_b.json")
    except:
        print("data_s/fastest_b.json not found")
        quit()
    try:
        df_tyres = pd.read_json("data_s/tyres.json")
    except:
        print("data_s/tyres.json not found")
        quit()
    
    try:
        df_qualif_2021_no_sprint = pd.read_json("data_s/qualif_2021_no_sprint.json")
    except:
        print("data_s/qualif_2021_no_sprint.json not found")
        quit()
    try:
       df_qualif_2021_sprint = pd.read_json("data_s/qualif_2021_sprint.json")
    except:
        print("data_s/qualif_2021_sprint.json not found")
        quit()


    df_fastest = pd.concat([df_fastest_a, df_fastest_b], axis=0)

    df_qualif = pd.concat([df_qualif_before,df_qualif_2021_sprint,df_qualif_2021_no_sprint],axis=0)

    df_qualif = df_qualif.rename(columns={'Position':'Pos_Qualif'})
    df_fastest = df_fastest.rename(columns={'Position':'Speed_Rank','Time':'Lap_Time'})
    df_pitstop = df_pitstop.rename(columns={'Time':'Time_Pit','Laps':'Lap_pit'})

    df_fastest_spa = df_fastest[(df_fastest['title']=='Yas Marina Circuit, Yas Island') & (df_fastest['Date']=="2021")]
    df_fastest_spa['title'] = df_fastest_spa['title'].str.replace('Yas Marina Circuit, Yas Island',"Circuit de Spa-Francorchamps, Spa-Francorchamps")
    df_fastest_spa["Speed_Rank"] = df_fastest_spa["Speed_Rank"].astype(str)
    df_fastest_spa["Lap_Time"] = df_fastest_spa["Lap_Time"].astype(str)
    df_fastest_spa["Avg_Speed"] = df_fastest_spa["Avg_Speed"].astype(str)
    df_fastest_spa['Date'] = df_fastest_spa['Date'].astype(str)

    for val in df_fastest_spa["Speed_Rank"]:
        df_fastest_spa["Speed_Rank"] = df_fastest_spa["Speed_Rank"].str.replace(val,"NaN")

    for val in df_fastest_spa["Lap_Time"]:
        df_fastest_spa["Lap_Time"] = df_fastest_spa["Lap_Time"].str.replace(val,"NaN")

    for val in df_fastest_spa["Avg_Speed"]:
        df_fastest_spa["Avg_Speed"] = df_fastest_spa["Avg_Speed"].str.replace(val,"NaN")

    df_fastest_spa["Date"] = df_fastest_spa["Date"].str.replace("2021","2021-08-29")

    df_fastest = pd.concat([df_fastest, df_fastest_spa], axis=0)


    df1 = pd.merge(df_race_result, df_fastest,  how='right', left_on=['title','Date','Number','Driver','Team'], right_on = ['title','Date','Number','Driver','Team']).fillna("NaN")
    df_race = pd.merge(df1, df_qualif,  how='right', left_on=['title','Date','Number','Driver','Team'], right_on = ['title','Date','Number','Driver','Team']).fillna('NaN')

    df_race["Date"] = df_race['Date'].astype(str)
    split_date = df_race['Date'].str.split("-",n=1).str[0]
    df_race['title'] = df_race['title'].str.replace("Circuit de Catalunya, Spain","Catalunya, Barcelona")
    df_race['title'] = df_race['title'].str.replace("Circuit de Barcelona-Catalunya, Spain","Catalunya, Barcelona")
    df_race['title'] = df_race['title'].str.replace("Valencia Street Circuit, Spain","Street Circuit, Valencia")
    df_race.loc[df_race.Date == "2020-07-12", "title"] = "Styria, Styria"
    df_race.loc[df_race.Date == "2021-06-27", "title"] = "Styria, Styria"
    df_race.loc[df_race.Date == "2020-08-09", "title"] = "Silverstone, Silverstone_70th"
    split_gp = df_race['title'].str.split(", ",n=1).str[1]
    df_race['Date']=split_date
    df_race['title']=split_gp
    df_race = df_race.rename(columns={'title':'Grand_Prix','Date':'Year'})

    df_pitstop["Date"] = df_pitstop['Date'].astype(str)
    split_date = df_pitstop['Date'].str.split("-",n=1).str[0]
    split_gp = df_pitstop['title'].str.split(", ",n=1).str[1]
    df_pitstop['Date']=split_date
    df_pitstop['title']=split_gp
    df_pitstop = df_pitstop.rename(columns={'title':'Grand_Prix','Date':'Year'})


    df_race["Avg_Speed"] = df_race['Avg_Speed'].astype("float64")
    df_race['Points'] = df_race['Points'].astype("float64")
    df_race['Position'] = pd.to_numeric(df_race['Position'],errors="coerce")
    df_race['Lap_Time'] = "0" + df_race['Lap_Time'].astype(str)
    df_race["Pos_Qualif"] = pd.to_numeric(df_race['Pos_Qualif'],errors="coerce")
    df_race['Q1'] = "0" + df_race['Q1'].astype(str)
    df_race['Q2'] = "0" + df_race['Q2'].astype(str)
    df_race['Q3'] = "0" + df_race['Q3'].astype(str)
    df_race = df_race.rename(columns={'Time':'Gap_Time'})

    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Sakhir","Bahrain")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Melbourne","Australia")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Shanghai","China")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Spielberg","Austria")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Kuala Lumpur","Malaysia")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Budapest","Hungary")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Monte Carlo","Monaco")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Sochi","Russia")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Montreal","Canada")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Great Britain","Silverstone")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Le Castellet","France")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Portimão","Portugal")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Belgium","Spa-Francorchamps")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Hockenheim","Germany")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Nürburgring","Germany")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Italy","Monza")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Mugello","Tuscany")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Suzuka","Japan")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Istanbul","Turkey")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Mexico City","Mexico")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Austin","United States")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("São Paulo","Brazil")
    df_race['Grand_Prix'] = df_race['Grand_Prix'].str.replace("Lusail","Qatar")

    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Sakhir","Bahrain")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Melbourne","Australia")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Shanghai","China")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Spielberg","Austria")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Kuala Lumpur","Malaysia")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Budapest","Hungary")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Monte Carlo","Monaco")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Sochi","Russia")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Montreal","Canada")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Great Britain","Silverstone")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Le Castellet","France")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Portimão","Portugal")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Belgium","Spa-Francorchamps")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Hockenheim","Germany")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Nürburgring","Germany")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Italy","Monza")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Mugello","Tuscany")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Suzuka","Japan")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Istanbul","Turkey")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Mexico City","Mexico")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Austin","United States")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("São Paulo","Brazil")
    df_pitstop['Grand_Prix'] = df_pitstop['Grand_Prix'].str.replace("Lusail","Qatar")


    df_pitstop['Num_stop'] = df_pitstop['Num_stop'].astype("float64")
    #df_pitstop["Time_Pit"] = df_pitstop['Time_Pit'].astype("float64",errors="ignore")
    df_pitstop = df_pitstop[~df_pitstop['Time_Pit'].str.contains(":",na=False)]
    df_pitstop['Time_Pit'] = df_pitstop['Time_Pit'].astype("float64")

    df_tyres = df_tyres.rename(columns={'title':'Year','GP':'Grand_Prix'})
    split_year = df_tyres['Year'].str.split(" ",n=2).str[2]
    split_driver = df_tyres['Driver'].str.split(" ",n=1).str[1]
    df_tyres['Year']=split_year
    df_tyres['Driver']=split_driver

    df_tyres['Grand_Prix'] = df_tyres['Grand_Prix'].str.replace("Sakhir","Bahrain")
    df_tyres['Grand_Prix'] = df_tyres['Grand_Prix'].str.replace("Azerbaijan","Baku")
    df_tyres['Grand_Prix'] = df_tyres['Grand_Prix'].str.replace("Spain","Barcelona")
    df_tyres['Grand_Prix'] = df_tyres['Grand_Prix'].str.replace("Great Britain","Silverstone")
    df_tyres['Grand_Prix'] = df_tyres['Grand_Prix'].str.replace("70TH Anniversary","Silverstone_70th")
    df_tyres['Grand_Prix'] = df_tyres['Grand_Prix'].str.replace("Belgium","Spa-Francorchamps")
    df_tyres['Grand_Prix'] = df_tyres['Grand_Prix'].str.replace("Italy","Monza")
    df_tyres['Grand_Prix'] = df_tyres['Grand_Prix'].str.replace("Europe","Baku")
    df_tyres['Grand_Prix'] = df_tyres['Grand_Prix'].str.replace("Russian","Russia")
    df_tyres['Grand_Prix'] = df_tyres['Grand_Prix'].str.replace("Europa","Valencia")
    df_tyres['Grand_Prix'] = df_tyres['Grand_Prix'].str.replace("Netherlands","Zandvoort")
    df_tyres['Grand_Prix'] = df_tyres['Grand_Prix'].str.replace("Korea","South Korea")
    df_tyres['Grand_Prix'] = df_tyres['Grand_Prix'].str.replace("Saudi Arabia","Jeddah")


    df_fastest_spa = df_fastest[(df_fastest['title']=='Yas Marina Circuit, Yas Island') & (df_fastest['Date']=="2021")]
    df_fastest_spa['title'] = df_fastest_spa['title'].str.replace('Yas Marina Circuit, Yas Island',"Circuit de Spa-Francorchamps, Spa-Francorchamps")
    df_fastest_spa["Speed_Rank"] = df_fastest_spa["Speed_Rank"].astype(str)
    df_fastest_spa["Lap_Time"] = df_fastest_spa["Lap_Time"].astype(str)
    df_fastest_spa["Avg_Speed"] = df_fastest_spa["Avg_Speed"].astype(str)

    for val in df_fastest_spa["Speed_Rank"]:
        df_fastest_spa["Speed_Rank"] = df_fastest_spa["Speed_Rank"].str.replace(val,"NaN")

    for val in df_fastest_spa["Lap_Time"]:
        df_fastest_spa["Lap_Time"] = df_fastest_spa["Lap_Time"].str.replace(val,"NaN")

    for val in df_fastest_spa["Avg_Speed"]:
        df_fastest_spa["Avg_Speed"] = df_fastest_spa["Avg_Speed"].str.replace(val,"NaN")


    df_fastest = pd.concat([df_fastest, df_fastest_spa], axis=0)



    try:
        client = pymongo.MongoClient()
        database = client['projet_f']
    except:
        print("Problem to access MongoDB")

    try:
        database['Race'].drop() 
        database['Tyres'].drop()
        database['Pitstop'].drop()
    
    except:
        print("No collections to delete")

    try:
        entry = df_race.to_json(orient="records")
        entry = json.loads(entry)
        database['Race'].insert_many(entry)
    except:
        print("Dataframe Race not found")
        quit()

    try:
        
        entry = df_tyres.to_json(orient="records")
        entry = json.loads(entry)
        database['Tyres'].insert_many(entry)
    except:
        print("Dataframe Tyres not found")
        quit()

    try:
        
        entry = df_pitstop.to_json(orient="records")
        entry = json.loads(entry)
        database['Pitstop'].insert_many(entry)
    except:
        print("Dataframe Pitstop not found")
        quit()


"""
df_race_result = pd.read_json("data/race_result.json")
    df_pitstop = pd.read_json("data/pit_stop.json")
    df_qualif = pd.read_json("data/qualif.json")
    df_fastest_a = pd.read_json("data/fastest_a.json")
    df_fastest_b = pd.read_json("data/fastest_b.json")

df_tyres = pd.read_json("data/tyres.json")


"""