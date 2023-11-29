# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. October 2023git 

from flask import Flask, request, jsonify
from trafficBase.model import CityModel
from trafficBase.agent import *

# Size of the board:
#number_agents = 10
citymodel = None
currentStep = 0
timetogenerate= 5 
timecounter = 0

app = Flask("Traffic example")

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

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global citymodel

    if request.method == 'GET':
        agentPositions = [{"id": str(b.unique_id), "x": x, "y":0, "z":z} for a, (x, z) in citymodel.grid.coord_iter() for b in a if isinstance(b, Car)]

        return jsonify({'positions':agentPositions})

@app.route('/getLights', methods=['GET'])
def getLights():
    global citymodel

    if request.method == 'GET':
        agentPositions = [{"id": str(b.unique_id), "x": x, "y":0, "z":z ,"state":b.state} for a, (x, z) in citymodel.grid.coord_iter() for b in a if isinstance(b, Traffic_Light)]

        return jsonify({'positions':agentPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, citymodel
    if request.method == 'GET':
        citymodel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)