# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. October 2023git 
#S Fernanda Colomo F - A01781983
#Ian Luis Vázquez Morán - A01027225
#Código para el servidor en flask para conectar con Unity

"""En este código se hacen todos los Get y Post necesarios para la simulación que se enviará a Unity"""
from flask import Flask, request, jsonify
from trafficBase.model import CityModel
from trafficBase.agent import *
from trafficBase.model import *
import requests

# Size of the board:
#number_agents = 10
citymodel = None
currentStep = 0
timetogenerate= 5 
timecounter = 0

app = Flask("Traffic example")

#se hace un POST para enviar los datos de la simulación tales como el modelo, el tiempo de generacion y el cronometro
@app.route('/init', methods=['POST'])
def initModel():
    global currentStep, citymodel, timetogenerate, timecounter

    if request.method == 'POST':
        #number_agents = int(request.form.get('NAgents'))
        timetogenerate = int(request.form.get('timetogenerate'))
        timecounter = int(request.form.get('timecounter'))
        currentStep = 0
        print(request.form)
        citymodel = CityModel(timetogenerate, timecounter)

        return jsonify({"message":"Parameters recieved, model initiated."})

#GetAgents obtiene los agentes, en específio la pocisión de los autos 
@app.route('/getAgents', methods=['GET'])
def getAgents():
    global citymodel

    if request.method == 'GET':
        agentPositions = [{"id": str(b.unique_id), "x": x, "y":0, "z":z} for a, (x, z) in citymodel.grid.coord_iter() for b in a if isinstance(b, Car)]

        return jsonify({'positions':agentPositions})

#GetLights obtiene los semaforos y su estado
@app.route('/getLights', methods=['GET'])
def getLights():
    global citymodel

    if request.method == 'GET':
        agentPositions = [{"id": str(b.unique_id), "x": x, "y":0, "z":z ,"state":b.state} for a, (x, z) in citymodel.grid.coord_iter() for b in a if isinstance(b, Traffic_Light)]

        return jsonify({'positions':agentPositions})
#update actualiza el modelo en cada step dado
@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, citymodel
    if request.method == 'GET':
        citymodel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})



if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)

    