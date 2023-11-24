from mesa import DataCollector, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import Road, Traffic_Light, Obstacle, Destination, Car
import json
import random

class CityModel(Model):
    """ 
        Creates a model based on a city map.

        Args:
            N: Number of agents in the simulation
    """
    def __init__(self, N, timetogenerate, timecounter = 0):

        # Load the map dictionary. The dictionary maps the characters in the map file to the corresponding agent.
        dataDictionary = json.load(open("city_files/mapDictionary.json"))
        self.timetogenerate = timetogenerate
        self.time_counter = timecounter  # Counter to keep track of the steps
        self.traffic_lights = []

        # Load the map file. The map file is a text file where each character represents an agent.
        with open('city_files/tl.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            # Goes through each character in the map file and creates the corresponding agent.
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
        
        corners = [(1, 1), (1, self.height - 2), (self.width - 2, 1), (self.width - 1, self.height - 2)]
        
        for corner in corners:
            agent = Car(f"car_{corner}", self)
            self.schedule.add(agent)  
            self.grid.place_agent(agent, corner)

        self.num_agents = N
        self.running = True

        #place N cars in the grid randomly if there is only road at the cell
       

        # ...

        class CityModel(Model):
            """ 
                Creates a model based on a city map.

                Args:
                    N: Number of agents in the simulation
                    timetogenerate: Number of steps to generate a new car
            """
            def __init__(self, N, timetogenerate):
                # ...

                self.timetogenerate = timetogenerate
                self.time_counter = 0  # Counter to keep track of the steps

                # ...

            def step(self):
                '''Advance the model by one step.'''
                self.schedule.step()

                # Increment the time counter
                self.time_counter += 1

                # Check if it's time to generate a new car
                if self.time_counter % self.timetogenerate == 0:
                    # Get a random corner
                    corner = [(1, 1), (1, self.height - 2), (self.width - 2, 1), (self.width - 1, self.height - 2)]
        
                    # Create a new car agent
                    agent = Car(random.choice(corner), self)
                    self.schedule.add(agent)  
                    self.grid.place_agent(agent, corner)
     


      
        #self.datacollector = DataCollector(
         #   agentreporters={"Cars":lambda m: sum(1 for agent in m.schedule.agents if isinstance(agent, Car))})



    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        # Increment the time counter
        self.time_counter += 1

        # Check if it's time to generate a new car
        if self.time_counter % self.timetogenerate == 0:
            # Get a random corner
            corner = random.choice([(1, 1), (1, self.height - 2), (self.width - 2, 1), (self.width - 1, self.height - 2)])
        

            # Create a new car agent
            agent = Car(1000+ self.time_counter, self)
            self.schedule.add(agent)  
            self.grid.place_agent(agent, corner)
            
    
    

        