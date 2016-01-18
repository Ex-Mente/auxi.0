from auxi.simulation.path_engine import *
from auxi.simulation.investigation import *


class Writer():
    def __init__(self, file_path):
        self.file_path = file_path

    def create_file_from_investigation(self, investigation):
        print("Abstract Method. Make use of a derived class.")
