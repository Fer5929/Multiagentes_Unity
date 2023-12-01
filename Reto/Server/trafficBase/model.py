#S Fernanda Colomo F - A01781983
#Ian Luis Vázquez Morán - A01027225
#Codigo del modelo de la simulacón 
"""En este código se construye el modelo de la simulación y se colocan los agentes en el mapa"""
from mesa import DataCollector, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from trafficBase.agent import Road, Traffic_Light, Obstacle, Destination, Car
import json
import random
import requests

class CityModel(Model):
    """ 
        Creates a model based on a city map.

        Args:
            N: Number of agents in the simulation
    """
    def __init__(self, timetogenerate=5 , timecounter = 0):

        # Load the map dictionary. The dictionary maps the characters in the map file to the corresponding agent.
        dataDictionary = json.load(open("static/city_files/mapDictionary.json"))
        self.timetogenerate = timetogenerate
        self.time_counter = timecounter  # Counter to keep track of the steps
        self.traffic_lights = []

        # Load the map file. The map file is a text file where each character represents an agent.
        with open('static/city_files/2023_base.txt') as baseFile:
            #lee el archivo y obtiene las dimensiones del mismo
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            #se hace un multigrid para poder tener varios agentes en una misma celda
            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            # Coloca los agentes en base al diccionario y al mapa dado
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        #print(agent.direction)

                    elif col in ["S", "s","T","t"]:
                        change = [15, 7]
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if col == "S" or col == "s" else True, 15 if col =="S" or col =="s" else 7,dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.schedule.add(agent)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.schedule.add(agent)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        agent.set_initial_position((c, self.height - r - 1)) 
        
        #coloca un carro en cada esquina del mapa en el primer step
        corners = [(1, 1), (1, self.height - 2), (self.width - 2, 1), (self.width - 1, self.height - 2)]
        
        for corner in corners:
            agent = Car(f"car_{corner}", self)
            self.schedule.add(agent)  
            self.grid.place_agent(agent, corner)
            print(agent.unique_id)

        


       
        self.running = True
        self.car_count = 0 #contador de carros que llegan a su destino (presentación)
        

        

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        # Increment the time counter
        self.time_counter += 1
        #obtiene las posiciones de los agentes y las imprime en consola (se usa para debuggear)
        agentPositions = [(b.unique_id) for a, (x, z) in self.grid.coord_iter() for b in a if isinstance(b, Car)]
        print(agentPositions)

      
       
        
        # Check if it's time to generate a new car en este ejemplo se genera un carro cada 5 steps pero puede cambiar 
        print(f"Current value of timetogenerate: {self.timetogenerate}")
        if self.time_counter % self.timetogenerate == 0:
            # Get a random spawn point
            spawn = random.choice([(1, 1), (self.width - 1, self.height - 2)])
        

            # Create a new car agent
            agent = Car(1000+ self.time_counter, self)
            self.schedule.add(agent)  
            self.grid.place_agent(agent, spawn)

        #if self.time_counter % 100 == 0:#envia los datos de la simulación cada 100 steps (presentación)

         #   url = "http://52.1.3.19:8585/api/"
         #   endpoint = "attempts"

            #data = {
             #   "year" : 2023,
             #   "classroom" : 302,
              #  "name" : "Equipo 15",
               # "num_cars": 453+self.car_count
            #}

            #headers = {
             #   "Content-Type": "application/json"
            #}

            #response = requests.post(url+endpoint, data=json.dumps(data), headers=headers)
            #print ("LISTO")
            #print("Request " + "successful" if response.status_code == 200 else "failed", "Status code:", response.status_code)
            #print("Response:", response.json())  