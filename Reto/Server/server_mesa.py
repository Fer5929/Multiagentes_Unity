#S Fernanda Colomo F - A01781983
#Ian Luis Vázquez Morán - A01027225
#Codigo para la visualización de la simulación en mesa
from trafficBase.agent import *
from trafficBase.model import CityModel
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer

def agent_portrayal(agent): #como se verá cada agente en la simulación 
    if agent is None: return
    
    portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "Layer": 1,
                 "w": 1,
                 "h": 1
                 }

    if (isinstance(agent, Road)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
    
    if (isinstance(agent, Destination)):
        portrayal["Color"] = "lightgreen"
        portrayal["Layer"] = 0

    if (isinstance(agent, Traffic_Light)):
        portrayal["Color"] = "red" if not agent.state else "green"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    if (isinstance(agent, Obstacle)):
        portrayal["Color"] = "cadetblue"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8
    
    if (isinstance(agent, Car)):
        portrayal["Color"] = "purple"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    return portrayal

width = 0
height = 0

#se usa el texto de la simulación para obtener las dimensiones del mapa
with open('static/city_files/2023_base.txt') as baseFile:
    lines = baseFile.readlines()
    width = len(lines[0])-1
    height = len(lines)

model_params = { "timetogenerate": 5} #cada cuanto se genera un carro

print(width, height)
grid = CanvasGrid(agent_portrayal, width, height, 500, 500)#se crea el grid para la simulación

server = ModularServer(CityModel, [grid], "Traffic Base", model_params)#se crea el servidor
                       
server.port = 8521 # The default
server.launch()