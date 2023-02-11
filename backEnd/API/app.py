import os 
from flask import Flask, request
from dotenv import load_dotenv
from datetime import datetime, timezone
import psycopg2
import joblib
# ! lets define the data base query set
# ? name, games_played, goals, penalty_minutes, position_D, position_LW, model_result
# * define the creation of a table of atheletes, this will be used to store the data of the atheletes
# we can load this with prospect data 
CREATE_PLAYERS_MODEL_TABLE = "CREATE TABLE IF NOT EXISTS players (id SERIAL PRIMARY KEY, name VARCHAR(100), games_played INT, goals INT, penalty_minutes FLOAT, position_D INT, position_LW INT, model_result FLOAT);"

INSERT_PALYER = "INSERT INTO players (name, games_played, goals, penalty_minutes, position_D, position_LW, model_result) VALUES (%s, %s, %s, %s, %s, %s, %s);"

FIND_PLAYER_byName = "SELECT * FROM players WHERE name=%s;"
FIND_PLAYER_byID = "SELECT * FROM players WHERE id=%s;"


#import model
clf = joblib.load('svm_model.pkl')


load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)



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
    
        
        
   

   


@app.post("/data/addPlayers")
def add_players():
    data = request.get_json()
    cursor = connection.cursor()
    cursor.execute(INSERT_PALYER, (data["name"], data["games_played"], data["goals"], data["penalty_minutes"], data["position_D"], data["position_LW"], data["model_result"]))
    connection.commit()
    cursor.close()
    return {"message": "player added successfully."}



#method for getting all players
@app.get("/api/allplayers")
def get_all_players():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()
    cursor.close()
    return {"players": players}


#chat bot method
@app.post("/api/chatbot")
def chat_bot():
    data = request.get_json()
    
    
    #......
    # we will have to call the model here to process the data

    #then if the objective is to find a player we will query the database
    #this is a repalcement for the pd.reda_csv() method
    #we will have to query the database for the player
    #then query the stats for the player

    #then return the results

    #if the objective is to predict a player we will run the model
    #however this will take a series of post requests