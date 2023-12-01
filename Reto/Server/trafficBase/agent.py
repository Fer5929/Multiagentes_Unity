#S Fernanda Colomo F - A01781983
#Ian Luis Vázquez Morán - A01027225
#Codigo del comportamiento de cada agente
"""En este código se encuentra la lógica de cada agente, tal como el movimiento y validación del mismo por 
parte del carro usando A*, el cambio de estado de los semáforos, etc. Es importante ya que es la lógica 
a usar en la simulación"""

from queue import PriorityQueue
import random
import networkx as nx
from mesa import Agent


class Car(Agent):
    """
    Agent that moves in a given direction to reach its destination.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of four directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        self.destination=None #destino del carro
        self.visited_nodes = set() #nodos visitados
        self.valid=0 #si el movimiento es valido 
        super().__init__(unique_id, model)

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """        
       
        camino = self.astar()
        #llama a la función de A* que se va a regresar el camino posible evitando los obstáculos
        self.valid=0
        #se declara el moviemiento de valido como 0 hasta ver si es posible moverse

        #revisa si el camino es valido y si es mayor a 1, es decir, si hay un camino posible
        if camino and len(camino) > 1:
            current_position = self.pos
            next_position = None

        #print(f"Current position: {current_position}")
        #obtiene los contenidos de la celda 
        cell_content = self.model.grid.get_cell_list_contents([self.pos])
        #print(f"Contents of current position: {cell_content}")
        
        for position in camino[1:]:#revisa si hay un camino posible que no se haya vistiado (evita retroceso)
            if position != current_position and position not in self.visited_nodes:
                next_position = position
                break

        #print(f"Next position determined by A*: {next_position}")
        penalized_graph = self.create_penalized_graph()
        #se crea un grafo "penalizado" en el cual se eliminan nodos para poder recalcular la ruta sin esos nodos 
        #print(f"Penalized graph: {penalized_graph}")

        #Se obtienen contenidos de la celda acutal y de la siguiente
        if next_position is not None:
            current_cell = self.model.grid.get_cell_list_contents([current_position])[0]
            next_content= self.model.grid.get_cell_list_contents([next_position])
            
                
            if isinstance(current_cell, (Road,Traffic_Light)):
                # si el auto se encuentra en una celda con un camino o un semáforo
                #valid_directions = self.get_valid_directions(current_cell.direction)
                #print(f"Penalized graph: {penalized_graph}")
                next_cell = self.model.grid.get_cell_list_contents([next_position])[0]
                #print(f"Contents of next position: {next_cell}")
                #Revisa si el semáforo está en rojo y si lo esta se queda en la misma posición
                if (isinstance(next_cell, Traffic_Light) and next_cell.state == False) or (isinstance(current_cell,Traffic_Light) and current_cell.state == False):
                    #stay in the same position
                    print("Red light")
                    next_position = current_position
                    self.valid=1 #se declara el movimiento como valido
                

                #check if next position the  destination of the car
                if next_position == self.destination.initial_position:
                    print("Next position is the destination")
                    self.model.grid.move_agent(self, next_position)
                    self.visited_nodes.add(next_position)
                    self.valid=1
                    #si la pocisión siguiente es el destino, se mueve a esa posición y se declara el movimiento como valido

                #if next position neighbors are destination le da prioridad y va a su destino (se usó por los carriles exteriores)
                #revisa cada posible posición
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
                    #si no es ninguno de los caosos anteriores se revisa si se puede mover a donde A* indica
                    #print(f"Penalized graph E: {penalized_graph}")
                    camino = self.astarcal(penalized_graph)#se recalcula usando astarcal con el grafo penalizado
                    
                    if camino and len(camino) > 1:
                    # Identify the next valid position from the new path
                        for position in camino[1:]:
                            if position != current_position and position not in self.visited_nodes:
                                next_position = position
                                break
                    print(f"New next position determined by A*: {next_position}")
                    #Revisa si la siguiente posición está a la izquierda, derecha, arriba o abajo de la posición actual
                    #Esto se usa para validar si la dirección en la que se encuentra la siguiente posición es válida con la dirección actual
                    #Explora todos los posibles resultados y si es válida la toma de lo contrario se elimina ese nodo y se recalculará la ruta
                    if next_position[1] == current_position[1] - 1:
                        # Next cell is at the bottom of the current cell
                        #print("Next cell is at the bottom")
                        #print("Current cell direction: ", current_cell.direction)
                        if isinstance(next_cell, Destination) and next_position != self.destination:
                            next_road_direction = current_cell.direction
                            #print(f"Next road direction D: {next_road_direction}")
                        else:
                            next_road_direction = next_cell.direction
                            #print(f"Next road direction: {next_road_direction}")
                    
                        if (current_cell.direction == "Left" or current_cell.direction=="Right") and next_road_direction =="Down":
                            #check if next position has a car
                            next_content= self.model.grid.get_cell_list_contents([next_position])
                            #print(f"Contents of next position: {next_content}")
                              
                            if any(isinstance(agent, Car) for agent in next_content):
                            #para evitar choques se espera si hay un carro en la celda que sigue
                                #print("Car in front")
                                next_position = current_position
                                self.valid=1
                            else:
                                #print(f"Moving agent to: {next_position}")
                                self.model.grid.move_agent(self, next_position)
                                self.valid=1
                        elif (current_cell.direction == "Down") and (next_road_direction =="Left" or next_road_direction=="Right" or next_road_direction=="Down"):
                            next_content= self.model.grid.get_cell_list_contents([next_position])
                            #print(f"Contents of next position: {next_content}")
                            # Check if there is a Car agent present in the same cell as the Road
                            if any(isinstance(agent, Car) for agent in next_content):
                            #stay in the same position
                                #print("Car in front")
                                next_position = current_position
                                self.valid=1
                            else:
                                #print(f"Moving agent to: {next_position}")
                                self.model.grid.move_agent(self, next_position)
                                self.valid=1
                        else:
                            #print("No hay movimiento valido") 
                            penalized_graph.remove_node(next_position)
                            camino = self.astarcal(penalized_graph)
                            self.valid=0

                        
                    elif next_position[1] == current_position[1] + 1:
                        # Next cell is at the top of the current cell
                        #print("Next cell is at the top")
                        #print("Current cell direction: ", current_cell.direction)
                        if isinstance(next_cell, Destination) and next_position != self.destination:
                            next_road_direction = current_cell.direction
                            #print(f"Next road direction D: {next_road_direction}")
                        else:
                            next_road_direction = next_cell.direction
                            #print(f"Next road direction: {next_road_direction}")

                        
                        if (current_cell.direction == "Left" or current_cell.direction=="Right") and next_road_direction =="Up":
                            next_content= self.model.grid.get_cell_list_contents([next_position])
                            #print(f"Contents of next position: {next_content}")
                            # Check if there is a Car agent present in the same cell as the Road
                            if any(isinstance(agent, Car) for agent in next_content):
                            #stay in the same position
                                #print("Car in front")
                                next_position = current_position
                                self.valid=1
                            else:
                                #print(f"Moving agent to: {next_position}")
                                self.model.grid.move_agent(self, next_position)
                                self.valid=1
                        elif (current_cell.direction == "Up") and (next_road_direction =="Left" or next_road_direction=="Right" or next_road_direction=="Up"):
                            next_content= self.model.grid.get_cell_list_contents([next_position])
                            #print(f"Contents of next position: {next_content}")
                            # Check if there is a Car agent present in the same cell as the Road
                            if any(isinstance(agent, Car) for agent in next_content):
                            #stay in the same position
                                #print("Car in front")
                                next_position = current_position
                                self.valid=1
                            else:
                                #print(f"Moving agent to: {next_position}")
                                self.model.grid.move_agent(self, next_position)
                                self.valid=1
                        else:
                            #print("No hay movimiento valido") 
                            penalized_graph.remove_node(next_position)
                            camino = self.astarcal(penalized_graph)
                            self.valid=0


                    elif next_position[0] == current_position[0] - 1:
                        # Next cell is at the left of the current cell
                        #print("Next cell is at the left")
                        #print("Current cell direction: ", current_cell.direction)
                        if isinstance(next_cell, Destination) and next_position != self.destination:
                            next_road_direction = current_cell.direction
                            #print(f"Next road direction D: {next_road_direction}")
                        else:
                            next_road_direction = next_cell.direction
                            #print(f"Next road direction: {next_road_direction}")
                    
                        if (current_cell.direction == "Up" or current_cell.direction=="Down") and next_road_direction =="Left":
                            next_content= self.model.grid.get_cell_list_contents([next_position])
                            #print(f"Contents of next position: {next_content}")
                            # Check if there is a Car agent present in the same cell as the Road
                            if any(isinstance(agent, Car) for agent in next_content):
                            #stay in the same position
                                #print("Car in front")
                                next_position = current_position
                                self.valid=1
                            else:
                                #print(f"Moving agent to: {next_position}")
                                self.model.grid.move_agent(self, next_position)
                                self.valid=1
                        elif (current_cell.direction == "Left") and (next_road_direction =="Left" or next_road_direction=="Up" or next_road_direction=="Down"):
                            next_content= self.model.grid.get_cell_list_contents([next_position])
                            #print(f"Contents of next position: {next_content}")
                            # Check if there is a Car agent present in the same cell as the Road
                            if any(isinstance(agent, Car) for agent in next_content):
                            #stay in the same position
                                #print("Car in front")
                                next_position = current_position
                                self.valid=1
                            else:
                                #print(f"Moving agent to: {next_position}")
                                self.model.grid.move_agent(self, next_position)
                                self.valid=1
                        else:
                            #print("No hay movimiento valido") 
                            penalized_graph.remove_node(next_position)
                            
                            self.valid=0
                    elif next_position[0] == current_position[0] + 1:
                        # Next cell is at the right of the current cell
                        #print("Next cell is at the right")
                        #print("Current cell direction: ", current_cell.direction)
                        if isinstance(next_cell, Destination) and next_position != self.destination:
                            next_road_direction = current_cell.direction
                            #print(f"Next road direction D: {next_road_direction}")
                        else:
                            next_road_direction = next_cell.direction
                            #print(f"Next road direction: {next_road_direction}")
                    
                        if (current_cell.direction == "Up" or current_cell.direction=="Down") and next_road_direction =="Right":
                            next_content= self.model.grid.get_cell_list_contents([next_position])
                            #print(f"Contents of next position: {next_content}")
                            # Check if there is a Car agent present in the same cell as the Road
                            if any(isinstance(agent, Car) for agent in next_content):
                            #stay in the same position
                                #print("Car in front")
                                next_position = current_position
                                self.valid=1
                            else:
                                #print(f"Moving agent to: {next_position}")
                                self.model.grid.move_agent(self, next_position)
                                self.valid=1
                        elif (current_cell.direction == "Right") and (next_road_direction =="Right" or next_road_direction=="Up" or next_road_direction=="Down"):
                            next_content= self.model.grid.get_cell_list_contents([next_position])
                            #print(f"Contents of next position: {next_content}")
                            # Check if there is a Car agent present in the same cell as the Road
                            if any(isinstance(agent, Car) for agent in next_content):
                            #stay in the same position
                                #print("Car in front")
                                next_position = current_position
                                self.valid=1
                            else:
                                #print(f"Moving agent to: {next_position}")
                                self.model.grid.move_agent(self, next_position)
                                self.valid=1
                        else:
                            #print("No hay movimiento valido") 
                            penalized_graph.remove_node(next_position)
                            camino = self.astarcal(penalized_graph)
                            self.valid=0
                        
                

                

        #si el agente llegó a su destino se agrega 1 al countes (presentación)
        #también se elimina el agente de la simulación
        
        if self.pos == self.destination.initial_position:
            self.model.car_count+=1
            #print("DESTINATION")
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
            
            


    
    def select_random_destination(self):
        """Selects a random destination agent and assigns it to the agent (CAR)"""
        destination_agents = [agent for agent in self.model.schedule.agents if isinstance(agent, Destination)]
        if destination_agents:
            self.destination = random.choice(destination_agents)
    def create_penalized_graph(self):
        # Crea un grafo penalizado a partir del grafo original 
        grid_graph = nx.grid_2d_graph(self.model.width, self.model.height)

        # Quita los nodos con obstáculos
        obstacles = [agent.pos for agent in self.model.schedule.agents if isinstance(agent, Obstacle)]
        for obstacle_pos in obstacles:
            grid_graph.remove_node(obstacle_pos)

        return grid_graph
    def astar(self):
        """A* algorithm to find the shortest path from the agent's current position to its destination using NetworkX"""
        # Crea un grafo con el grid
        grid_graph = nx.grid_2d_graph(self.model.width, self.model.height)

        # Quita los nodos obstáculo
        obstacles = [agent.pos for agent in self.model.schedule.agents if isinstance(agent, Obstacle)]
        for obstacle_pos in obstacles:
            grid_graph.remove_node(obstacle_pos)

        # En base a la posición inicial y final, calcula el camino más corto
        start = self.pos
        goal = self.destination.initial_position

        try:
            path = nx.astar_path(grid_graph, start, goal)
            return path#regresa el camino (variable camino en Agent Car)
        except nx.NetworkXNoPath:
            return None
        
    def astarcal(self, graph):
    # Tiene la misma lógica que A* pero se usa para recalcular el camino 
    #por eso recibe un grafo penalizado
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
            self.select_random_destination()#elige el destino
        #print("destiny")
        #print(self.destination.initial_position)
        #print("ID", self.unique_id)
        self.move()#llama a move que contiene toda la lógica de movimiento

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
        #cambia su estado en el tiempo N dado
        if self.model.schedule.steps % self.timeToChange == 0:
            self.state = not self.state
        
        
        

class Destination(Agent):

   
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        initial_position = None

    def set_initial_position(self, pos):
        # Set the initial position when the agent is placed on the grid
        #se pasa la posición inicial al agent car para que sepa a donde ir
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
        self.direction = direction #se le da la dirreción correspondiente al modelo (mapa)
     

    def step(self):
       pass
           

