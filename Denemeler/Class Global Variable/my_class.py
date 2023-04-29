# my_class.py dosyası

class MyClass:
    def __init__(self, my_variable):
        self.my_variable = my_variable

    def update_global_variable(self, new_value):
        global my_global_variable
        my_global_variable = new_value
        self.my_variable = my_global_variable
