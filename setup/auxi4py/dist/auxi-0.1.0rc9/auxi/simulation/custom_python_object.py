from auxi.modelling.business import NamedObject


class custom_python_object(NamedObject):
    def __init__(self):
        NamedObject.__init__(self)
        self.name = "custom_python_object"
