import mesa
import random

class Trash(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = 1

    def step(self):
        pass


class Robot(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "Cleaning"
        self.moves = 0

    def move(self):
        # Definimos la lista de posiciones posibles
        nextStep = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)

        # De forma aleatroia seleccionamos una posición de la lista
        new_position = self.random.choice(nextStep)
        self.model.grid.move_agent(self, new_position)
        self.moves += 1

    def step(self):
        self.move()

        # Obtiene la lista de los agentes en la posición actual
        cellmates = self.model.grid.get_cell_list_contents([self.pos])

        # En cada paso, si la celda está sucia, se limpia; si la cella está limpia, se mueve. 
        if any(isinstance(agent, Trash) for agent in cellmates):
            trash = next(
                agent for agent in cellmates if isinstance(agent, Trash))

            self.state = "Cleaning"
            self.model.grid.remove_agent(trash)

        else:
            self.state = "Moving"

        # # Imprimir el estado del agente de tipo Vacuum
        # print("Vacuum", self.unique_id, ":", self.state)

class Simulation(mesa.Model):
    def __init__(self, M, N, n_agents, dirtyCells, max_steps=100):
        self.num_agents = n_agents
        self.grid = mesa.space.MultiGrid(M, N, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.max_steps = max_steps
        self.running = True

        room = M * N

        dirtyCells = int(room * dirtyCells / 100)


        # Creamos los robots aspiradores (agentes)
        for i in range(self.num_agents):
            r = Robot(i, self)
            self.schedule.add(r)

            self.grid.place_agent(r, (1, 1)) # El agente se inicializa en la posición (1, 1)

        counter = 0

        # Creamos al agente que representa la suciedad
        while counter < dirtyCells:
            a = random.randrange(self.grid.width)
            b = random.randrange(self.grid.height)

            if self.grid.is_cell_empty((a, b)):
                trash = Trash(counter, self)
                self.grid.place_agent(trash, (a, b))
                counter += 1

        # Data Collector para obtener la cantidad de celdas sucias con el paso del tiempo
        self.TRData = mesa.DataCollector(
            {
                "Trash remaining": self.dirtyCells,
            }
        )

        self.TRData.collect(self)

        # Data Collector para obtener el porcentaje de celdas limpias con el paso del tiempo
        self.PCData = mesa.DataCollector(
            {
                "Percentage of clean cells": self.cleanCellsP,
            }
        )

        self.PCData.collect(self)

        # Data Collector para obtener el total de movimientos con el paso del tiempo
        self.TMData = mesa.DataCollector(
            {
                "Total Moves": self.totalMoves,
            }
        )
        self.TMData.collect(self)

        

    def step(self):
        # Si se alcanza el límite de pasos, se detiene la simulación
        if self.schedule.steps >= self.max_steps:
            self.running = False

        # Si aún no se alcanza el límite de pasos, se ejecuta el paso de la simulación a menos que no haya celdas sucias
        elif self.schedule.steps < self.max_steps:
            if self.dirtyCells() == 0:
                self.running = False

            else:
                self.schedule.step()
        
        self.TRData.collect(self)
        self.PCData.collect(self)
        self.TMData.collect(self)

    def run_model(self):
        # Mientras la simulación se esté ejecutando
        while self.running:
            # Ejecuta el paso de la simulación
            self.step()

    # Fucnión que nos permite obtener los movimeintos totales de los agentes
    def totalMoves(self):
        movesCounter = 0
        for agent in self.schedule.agents:
            movesCounter += agent.moves
        return movesCounter

    # Función que nos permite obtener el número de celdas limpias
    def cleanCells(self):
        cleanCellsCounter = 0
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if not any(isinstance(agent, Trash) for agent in cell_content):
                cleanCellsCounter += 1
        return cleanCellsCounter

    # Función que nos permite obtener el porcentaje de celdas limpias
    def cleanCellsP(self):
        return self.cleanCells() / (self.grid.width * self.grid.height) * 100

    # Función que nos permite obtener el número de celdas sucias
    def dirtyCells(self):
        dirtyCellsCounter = 0
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if any(isinstance(agent, Trash) for agent in cell_content):
                dirtyCellsCounter += 1
        return dirtyCellsCounter

    # Función que nos permite obtener el porcentaje de celdas sucias
    def dirtyCellsP(self):
        # Calcula el porcentaje de celdas Dirty
        return self.dirtyCells() / (self.grid.width * self.grid.height) * 100
