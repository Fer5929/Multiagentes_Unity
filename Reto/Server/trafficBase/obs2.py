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
        super().__init__(unique_id, model)

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """        
        #self.model.grid.move_to_empty(self)
       # Perform movement based on the path obtained from A* algorithm
        camino = self.astar()

        if camino and len(camino) > 1:
            current_position = self.pos
            next_position = None

        print(f"Current position: {current_position}")

        # Find the next position that is not the same as the current position
        for position in camino[1:]:
            if position != current_position:
                next_position = position
                break

        print(f"Next position determined by A*: {next_position}")

        # If next_position is still None, it means all positions in camino are the same as current_position
        # In this case, the agent stays in the same place (current_position)
        if next_position is not None:
            # Check if the road direction affects the next position
            current_cell = self.model.grid.get_cell_list_contents([current_position])[0]
            if isinstance(current_cell, Road):
                valid_directions = self.get_valid_directions(current_cell.direction)
                print(f"Valid directions: {valid_directions}")

                if next_position not in valid_directions:
                    print(f"Next position {next_position} not valid based on road direction")

                    # Recalculate path with A* algorithm
                    camino = self.astar()
                    if camino and len(camino) > 1:
                        # Update next_position based on the new path
                        for position in camino[1:]:
                            if position != current_position:
                                next_position = position
                                break

                        print(f"New next position determined by A*: {next_position}")
            
                else:
                    # Move the agent to the next position
                    print(f"Moving agent to: {next_position}")
                    self.model.grid.move_agent(self, next_position)

        if self.pos == self.destination.initial_position:
            # Destroy agent if it reaches its destination
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)

    def get_valid_directions(self, road_direction):
        # Define valid directions based on the road's direction
         # Get the position of the agent
        x, y = self.pos

    # Define valid directions based on the road's direction
        if road_direction == "Left":
        # Check the neighbors' directions
            left_neighbor = []
            up_neighbor = []
            down_neighbor = []

            # Check if the agent is not at the border
            if x > 0:
                left_neighbor = self.model.grid.get_cell_list_contents([(x - 1, y)])  # Left neighbor
        
            if y < self.model.height - 1:
                up_neighbor = self.model.grid.get_cell_list_contents([(x, y + 1)])  # Up neighbor
        
            if y > 0:
                down_neighbor = self.model.grid.get_cell_list_contents([(x, y - 1)])  # Down neighbor

            valid_directions = ["Left"]

            # Check if the left neighbor's direction allows movement from the current road
            if any(isinstance(cell, Road) and cell.direction in ["Left", "Up", "Down"] for cell in left_neighbor):
                valid_directions.append("Left")

            # Check if either the up or down neighbor's direction allows movement from the current road
            if any(isinstance(cell, Road) and cell.direction in ["Up", "Down"] for cell in up_neighbor):
                valid_directions.append("Up")

            if any(isinstance(cell, Road) and cell.direction in ["Up", "Down"] for cell in down_neighbor):
                valid_directions.append("Down")

            return valid_directions

        elif road_direction == "Up":
            return ["Left", "Up", "Right"]
        
        elif road_direction == "Right":
            # Check the neighbors' directions
            #right_neighbor = []
            up_neighbor = []
            down_neighbor = []

            # Check if the agent is not at the border
            #if x > 0:
                #left_neighbor = self.model.grid.get_cell_list_contents([(x - 1, y)])  # Left neighbor
        
            if y < self.model.height - 1:
                up_neighbor = self.model.grid.get_cell_list_contents([(x, y + 1)])  # Up neighbor
        
            if y > 0:
                down_neighbor = self.model.grid.get_cell_list_contents([(x, y - 1)])  # Down neighbor

            

            valid_directions = ["Right"]

            # Check if the right neighbor's direction allows movement from the current road
            #if any(isinstance(cell, Road) and cell.direction in ["Right", "Up", "Down"] for cell in right_neighbor):
             #   valid_directions.append("Right")

            # Check if either the up or down neighbor's direction allows movement from the current road
            if any(isinstance(cell, Road) and cell.direction in ["Up"] for cell in up_neighbor):
                valid_directions.append("Up")

            if any(isinstance(cell, Road) and cell.direction in [ "Down"] for cell in down_neighbor):
                valid_directions.append("Down")

            return valid_directions
        
        #revisar los elifs
        elif road_direction == "Down":
        # Check the neighbors' directions
            left_neighbor = []
            right_neighbor = []
            down_neighbor = []

            # Check if the agent is not at the border
            if x > 0:
                left_neighbor = self.model.grid.get_cell_list_contents([(x - 1, y)])  # Left neighbor
        
            if y < self.model.width - 1:
                right_neighbor = self.model.grid.get_cell_list_contents([(x, y + 1)])  # Up neighbor
        
            if y > 0:
                down_neighbor = self.model.grid.get_cell_list_contents([(x, y - 1)])  # Down neighbor

            valid_directions = []

            # Check if the left neighbor's direction allows movement from the current road
            if any(isinstance(cell, Road) and cell.direction in ["Right"] for cell in right_neighbor):
                valid_directions.append("Right")

            # Check if either the up or down neighbor's direction allows movement from the current road
            if any(isinstance(cell, Road) and cell.direction in ["Left"] for cell in left_neighbor):
                valid_directions.append("Left")

            if any(isinstance(cell, Road) and cell.direction in ["Down", "Right", "Left"] for cell in down_neighbor):
                valid_directions.append("Down")
            
            return valid_directions
        
        else:
            # Default case: return all directions
            return ["Left", "Up", "Right", "Down"]
    def select_random_destination(self):
        """Selects a random destination agent from the available ones"""
        destination_agents = [agent for agent in self.model.schedule.agents if isinstance(agent, Destination)]
        if destination_agents:
            self.destination = random.choice(destination_agents)
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
    
    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        if self.destination is None: #se asegura que una vez definida la posicion inicial, no se cambie
            self.select_random_destination()
        print("destiny")
        print(self.destination.initial_position)
        self.move()

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
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

    def step(self):
        """ 
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
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
