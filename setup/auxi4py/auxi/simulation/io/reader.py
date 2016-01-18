from auxi.simulation.path_engine import *
from auxi.simulation.investigation import *


class Reader():
    def __init__(self, file_path):
        self.file_path = file_path

    def update_scenario_from_file(self, investigation, scenario_name):
        print("Abstract Method. Make use of a derived class.")
