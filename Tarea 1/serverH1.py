from Robot import Simulation
import mesa 

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                "Filled": "true",
                "Layer": 0,
                "Color": "red",
                "r": 0.5}

    if agent.state == 1:
        portrayal["Color"] = "brown"
        portrayal["r"] = 0.2
    elif agent.state == "Cleaning":
        portrayal["Color"] = "red"
    else:
        portrayal["Color"] = "red"
    return portrayal

grid = mesa.visualization.CanvasGrid(agent_portrayal, 12, 12, 500, 500)

TRchart = mesa.visualization.ChartModule(
    [{"Label": "Trash remaining", "Color": "Blue"}], data_collector_name="TRData"
)

PCchart = mesa.visualization.ChartModule(
    [{"Label": "Percentage of clean cells", "Color": "Green"}], data_collector_name="PCData"
)

TMchart = mesa.visualization.ChartModule(
    [{"Label": "Total Moves", "Color": "Gray"}], data_collector_name="TMData"
)

server = mesa.visualization.ModularServer(
    Simulation, [grid,TRchart, PCchart, TMchart], "Envyroment", {"M": 12, "N": 12, "n_agents": 5, "dirtyCells": 30 }
    )

server.port = 8001 # The default
server.launch()