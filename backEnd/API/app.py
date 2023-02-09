import os 
from flask import Flask, request
from dotenv import load_dotenv
from datetime import datetime, timezone
import psycopg2
import joblib
#lets define the data base query set
#name, games_played, goals, penalty_minutes, position_D, position_LW, model_result
#define the creation of a table of atheletes, this will be used to store the data of the atheletes
#we can load this with prospect data 
CREATE_PLAYERS_TABLE = "CREATE TABLE IF NOT EXISTS players (id SERIAL PRIMARY KEY, name VARCHAR(100), games_played INT, goals INT, penalty_minutes FLOAT, position_D INT, position_LW INT, model_result FLOAT)"
FIND_PLAYER_BY_NAME = "SELECT * FROM players WHERE name=%s"
ADD_PLAYER = "INSERT INTO players (name) VALUES (%s)"
#import model
clf = joblib.load('svm_model.pkl')


load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

##########################################
#here we will start the model 
####
#
#
#
##########################################

@app.post("/api/player")
def get_player():
    name = request.get_json()["name"]
    #query the database for the player
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM players WHERE name=%s", (name,))
    player = cursor.fetchone()
    cursor.close()

    if(player == None):
        return{"message": "player not found"}
    else:
        return {"player": player}
    
        
        
   

   


@app.post("/api/runModel")
def run_model():
    #this is the method that will call the model given input parameters

    #input parameters are name, games played goals penelty minutes position_D and position_LW
    data = request.get_json()
    name = data["name"]
    games_played = data["games_played"]
    goals = data["goals"]
    penalty = data["penalty_minutes"]
    position_D = data["position_D"]
    position_LW = data["position_LW"]
    assists = data["assists"]

    #we will run the model and collect the results

    model_result = clf.predict([[games_played, goals, assists, penalty, position_D, position_LW]])

    #we will first entre the results into the database
    #cursor = connection.cursor()
    #cursor.execute("INSERT INTO players (name, games_played, goals, penalty_minutes, position_D, position_LW, model_result) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, games_played, goals, penalty, position_D, position_LW, model_result))
    #connection.commit()
    #cursor.close()

    #now we return the results
    model_result = model_result.tolist()
    return {"model_result": model_result}


#method for getting all players
@app.get("/api/allplayers")
def get_all_players():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()
    cursor.close()
    return {"players": players}