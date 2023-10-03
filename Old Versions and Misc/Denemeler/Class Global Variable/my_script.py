# my_script.py dosyası

from my_class import MyClass
global my_global_variable
my_global_variable = 42

my_object = MyClass(my_global_variable)

print(my_global_variable)   # 42
print(my_object.my_variable)   # 42

my_global_variable = 123

print(my_global_variable)   # 123
print(my_object.my_variable)   # 123
