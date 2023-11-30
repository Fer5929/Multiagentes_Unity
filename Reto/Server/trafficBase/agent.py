from queue import PriorityQueue
import random
import networkx as nx
from mesa import Agent


class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        self.destination=None
        self.visited_nodes = set()
        self.valid=0
        self.des=False
        super().__init__(unique_id, model)

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """        
        #self.model.grid.move_to_empty(self)
       # Perform movement based on the path obtained from A* algorithm
        camino = self.astar()
        self.valid=0

        if camino and len(camino) > 1:
            current_position = self.pos
            next_position = None

        print(f"Current position: {current_position}")
        cell_content = self.model.grid.get_cell_list_contents([self.pos])
        print(f"Contents of current position: {cell_content}")
        
        for position in camino[1:]:
            if position != current_position and position not in self.visited_nodes:
                next_position = position
                break

        print(f"Next position determined by A*: {next_position}")
        penalized_graph = self.create_penalized_graph()
        print(f"Penalized graph: {penalized_graph}")
        if next_position is not None:
            current_cell = self.model.grid.get_cell_list_contents([current_position])[0]
            next_content= self.model.grid.get_cell_list_contents([next_position])
            
                
            if isinstance(current_cell, (Road,Traffic_Light)):
                #valid_directions = self.get_valid_directions(current_cell.direction)
                print(f"Penalized graph: {penalized_graph}")
                next_cell = self.model.grid.get_cell_list_contents([next_position])[0]
                print(f"Contents of next position: {next_cell}")
                #check if next position is a red light
                if (isinstance(next_cell, Traffic_Light) and next_cell.state == False) or (isinstance(current_cell,Traffic_Light) and current_cell.state == False):
                    #stay in the same position
                    print("Red light")
                    next_position = current_position
                    self.valid=1
                

                #check if next position the  destination of the car
                if next_position == self.destination.initial_position:
                    print("Next position is the destination")
                    self.model.grid.move_agent(self, next_position)
                    self.visited_nodes.add(next_position)
                    self.valid=1
                #if next position neighbors are destination le da prioridad y va a su destino (se usó por los carriles exteriores)
                elif next_position [0] +1 == self.destination.initial_position[0] and next_position[1] == self.destination.initial_position[1]:
                    print("Next position is the destination")
                    self.model.grid.move_agent(self, next_position)
                    self.visited_nodes.add(next_position)
                    self.valid=1
                elif next_position [0] -1 == self.destination.initial_position[0] and next_position[1] == self.destination.initial_position[1]:
                    print("Next position is the destination")
                    self.model.grid.move_agent(self, next_position)
                    self.visited_nodes.add(next_position)
                    self.valid=1
                elif next_position [1] +1 == self.destination.initial_position[1] and next_position[0] == self.destination.initial_position[0]:
                    print("Next position is the destination")
                    self.model.grid.move_agent(self, next_position)
                    self.visited_nodes.add(next_position)
                    self.valid=1
                elif next_position [1] -1 == self.destination.initial_position[1] and next_position[0] == self.destination.initial_position[0]:
                    print("Next position is the destination")
                    self.model.grid.move_agent(self, next_position)
                    self.visited_nodes.add(next_position)
                    self.valid=1


                while self.valid==0:
                    print(f"Penalized graph E: {penalized_graph}")
                    camino = self.astarcal(penalized_graph)
                    
                    if camino and len(camino) > 1:
                    # Identify the next valid position from the new path
                        for position in camino[1:]:
                            if position != current_position and position not in self.visited_nodes:
                                next_position = position
                                break
                    print(f"New next position determined by A*: {next_position}")
                    # Check if next_cell is at the top, bottom, left, or right of the current_cell
                    if next_position[1] == current_position[1] - 1:
                        # Next cell is at the bottom of the current cell
                        print("Next cell is at the bottom")
                        print("Current cell direction: ", current_cell.direction)
                        if isinstance(next_cell, Destination) and next_position != self.destination:
                            next_road_direction = current_cell.direction
                            print(f"Next road direction D: {next_road_direction}")
                        else:
                            next_road_direction = next_cell.direction
                            print(f"Next road direction: {next_road_direction}")
                    
                        if (current_cell.direction == "Left" or current_cell.direction=="Right") and next_road_direction =="Down":
                            #check if next position has a car
                            next_content= self.model.grid.get_cell_list_contents([next_position])
                            print(f"Contents of next position: {next_content}")
                              
                            # Check if there is a Car agent present in the same cell as the Road
                            if any(isinstance(agent, Car) for agent in next_content):
                            #stay in the same position
                                print("Car in front")
                                next_position = current_position
                                self.valid=1
                            else:
                                print(f"Moving agent to: {next_position}")
                                self.model.grid.move_agent(self, next_position)
                                self.valid=1
                        elif (current_cell.direction == "Down") and (next_road_direction =="Left" or next_road_direction=="Right" or next_road_direction=="Down"):
                            next_content= self.model.grid.get_cell_list_contents([next_position])
                            print(f"Contents of next position: {next_content}")
                            # Check if there is a Car agent present in the same cell as the Road
                            if any(isinstance(agent, Car) for agent in next_content):
                            #stay in the same position
                                print("Car in front")
                                next_position = current_position
                                self.valid=1
                            else:
                                print(f"Moving agent to: {next_position}")
                                self.model.grid.move_agent(self, next_position)
                                self.valid=1
                        else:
                            print("No hay movimiento valido") 
                            penalized_graph.remove_node(next_position)
                            camino = self.astarcal(penalized_graph)
                            self.valid=0

                        
                    elif next_position[1] == current_position[1] + 1:
                        # Next cell is at the top of the current cell
                        print("Next cell is at the top")
                        print("Current cell direction: ", current_cell.direction)
                        if isinstance(next_cell, Destination) and next_position != self.destination:
                            next_road_direction = current_cell.direction
                            print(f"Next road direction D: {next_road_direction}")
                        else:
                            next_road_direction = next_cell.direction
                            print(f"Next road direction: {next_road_direction}")

                        
                        if (current_cell.direction == "Left" or current_cell.direction=="Right") and next_road_direction =="Up":
                            next_content= self.model.grid.get_cell_list_contents([next_position])
                            print(f"Contents of next position: {next_content}")
                            # Check if there is a Car agent present in the same cell as the Road
                            if any(isinstance(agent, Car) for agent in next_content):
                            #stay in the same position
                                print("Car in front")
                                next_position = current_position
                                self.valid=1
                            else:
                                print(f"Moving agent to: {next_position}")
                                self.model.grid.move_agent(self, next_position)
                                self.valid=1
                        elif (current_cell.direction == "Up") and (next_road_direction =="Left" or next_road_direction=="Right" or next_road_direction=="Up"):
                            next_content= self.model.grid.get_cell_list_contents([next_position])
                            print(f"Contents of next position: {next_content}")
                            # Check if there is a Car agent present in the same cell as the Road
                            if any(isinstance(agent, Car) for agent in next_content):
                            #stay in the same position
                                print("Car in front")
                                next_position = current_position
                                self.valid=1
                            else:
                                print(f"Moving agent to: {next_position}")
                                self.model.grid.move_agent(self, next_position)
                                self.valid=1
                        else:
                            print("No hay movimiento valido") 
                            penalized_graph.remove_node(next_position)
                            camino = self.astarcal(penalized_graph)
                            self.valid=0


                    elif next_position[0] == current_position[0] - 1:
                        # Next cell is at the left of the current cell
                        print("Next cell is at the left")
                        print("Current cell direction: ", current_cell.direction)
                        if isinstance(next_cell, Destination) and next_position != self.destination:
                            next_road_direction = current_cell.direction
                            print(f"Next road direction D: {next_road_direction}")
                        else:
                            next_road_direction = next_cell.direction
                            print(f"Next road direction: {next_road_direction}")
                    
                        if (current_cell.direction == "Up" or current_cell.direction=="Down") and next_road_direction =="Left":
                            next_content= self.model.grid.get_cell_list_contents([next_position])
                            print(f"Contents of next position: {next_content}")
                            # Check if there is a Car agent present in the same cell as the Road
                            if any(isinstance(agent, Car) for agent in next_content):
                            #stay in the same position
                                print("Car in front")
                                next_position = current_position
                                self.valid=1
                            else:
                                print(f"Moving agent to: {next_position}")
                                self.model.grid.move_agent(self, next_position)
                                self.valid=1
                        elif (current_cell.direction == "Left") and (next_road_direction =="Left" or next_road_direction=="Up" or next_road_direction=="Down"):
                            next_content= self.model.grid.get_cell_list_contents([next_position])
                            print(f"Contents of next position: {next_content}")
                            # Check if there is a Car agent present in the same cell as the Road
                            if any(isinstance(agent, Car) for agent in next_content):
                            #stay in the same position
                                print("Car in front")
                                next_position = current_position
                                self.valid=1
                            else:
                                print(f"Moving agent to: {next_position}")
                                self.model.grid.move_agent(self, next_position)
                                self.valid=1
                        else:
                            print("No hay movimiento valido") 
                            penalized_graph.remove_node(next_position)
                            
                            self.valid=0
                    elif next_position[0] == current_position[0] + 1:
                        # Next cell is at the right of the current cell
                        print("Next cell is at the right")
                        print("Current cell direction: ", current_cell.direction)
                        if isinstance(next_cell, Destination) and next_position != self.destination:
                            next_road_direction = current_cell.direction
                            print(f"Next road direction D: {next_road_direction}")
                        else:
                            next_road_direction = next_cell.direction
                            print(f"Next road direction: {next_road_direction}")
                    
                        if (current_cell.direction == "Up" or current_cell.direction=="Down") and next_road_direction =="Right":
                            next_content= self.model.grid.get_cell_list_contents([next_position])
                            print(f"Contents of next position: {next_content}")
                            # Check if there is a Car agent present in the same cell as the Road
                            if any(isinstance(agent, Car) for agent in next_content):
                            #stay in the same position
                                print("Car in front")
                                next_position = current_position
                                self.valid=1
                            else:
                                print(f"Moving agent to: {next_position}")
                                self.model.grid.move_agent(self, next_position)
                                self.valid=1
                        elif (current_cell.direction == "Right") and (next_road_direction =="Right" or next_road_direction=="Up" or next_road_direction=="Down"):
                            next_content= self.model.grid.get_cell_list_contents([next_position])
                            print(f"Contents of next position: {next_content}")
                            # Check if there is a Car agent present in the same cell as the Road
                            if any(isinstance(agent, Car) for agent in next_content):
                            #stay in the same position
                                print("Car in front")
                                next_position = current_position
                                self.valid=1
                            else:
                                print(f"Moving agent to: {next_position}")
                                self.model.grid.move_agent(self, next_position)
                                self.valid=1
                        else:
                            print("No hay movimiento valido") 
                            penalized_graph.remove_node(next_position)
                            camino = self.astarcal(penalized_graph)
                            self.valid=0
                        
                

                

        #print all the agents in a cell 
        
        if self.pos == self.destination.initial_position:
            self.model.car_count+=1
            print("DESTINATION")
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
            
            


    
    def select_random_destination(self):
        """Selects a random destination agent from the available ones"""
        destination_agents = [agent for agent in self.model.schedule.agents if isinstance(agent, Destination)]
        if destination_agents:
            self.destination = random.choice(destination_agents)
    def create_penalized_graph(self):
        # Create a penalized graph based on the original grid
        grid_graph = nx.grid_2d_graph(self.model.width, self.model.height)

        # Remove nodes corresponding to positions with obstacles
        obstacles = [agent.pos for agent in self.model.schedule.agents if isinstance(agent, Obstacle)]
        for obstacle_pos in obstacles:
            grid_graph.remove_node(obstacle_pos)

        return grid_graph
    def astar(self):
        # Create a graph representing the grid
        grid_graph = nx.grid_2d_graph(self.model.width, self.model.height)

        # Remove nodes corresponding to positions with obstacles
        obstacles = [agent.pos for agent in self.model.schedule.agents if isinstance(agent, Obstacle)]
        for obstacle_pos in obstacles:
            grid_graph.remove_node(obstacle_pos)

        # Calculate path using A* algorithm
        start = self.pos
        goal = self.destination.initial_position

        try:
            path = nx.astar_path(grid_graph, start, goal)
            return path
        except nx.NetworkXNoPath:
            return None
        
    def astarcal(self, graph):
    # Calculate path using A* algorithm with the given graph
        start = self.pos
        goal = self.destination.initial_position

        try:
            path = nx.astar_path(graph, start, goal)
            return path
        except nx.NetworkXNoPath:
            return None
    
    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        if self.destination is None: #se asegura que una vez definida la posicion inicial, no se cambie
            self.select_random_destination()
        print("destiny")
        print(self.destination.initial_position)
        print("ID", self.unique_id)
        self.move()

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10, direction= "Left"):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.timeToChange = timeToChange
        self.direction = direction
      

    def step(self):
        """ 
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        
        if self.model.schedule.steps % self.timeToChange == 0:
            self.state = not self.state
        
        
        # Check if there is a Car agent present in the same cell as the Road
        

class Destination(Agent):

   
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        initial_position = None

    def set_initial_position(self, pos):
        # Set the initial position when the agent is placed on the grid
        self.initial_position = pos
        
    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction
     

    def step(self):
       pass
           

