# import timeit

# class MyClass:
#     def __init__(self):
#         self.attribute = 0

# def use_local_variable():
#     local_var = 0
#     for _ in range(1000000):
#         local_var += 1
#     return local_var

# def use_object_attribute(obj):
#     for _ in range(1000000):
#         obj.attribute += 1
#     return obj.attribute

# obj = MyClass()

# # Measure time for local variable
# local_time = timeit.timeit(use_local_variable, number=10)

# # Measure time for object attribute
# object_time = timeit.timeit(lambda: use_object_attribute(obj), number=10)

# print(f"Time using local variable: {local_time}")
# print(f"Time using object attribute: {object_time}")

# import timeit

# # Global variable
# global_var = 0

# def enclosing_function():
#     enclosing_var = 0
    
#     def inner_function():
#         nonlocal enclosing_var
#         for _ in range(1000000):
#             enclosing_var += 1
#         return enclosing_var
    
#     return inner_function

# def use_local_variable():
#     local_var = 0
#     for _ in range(1000000):
#         local_var += 1
#     return local_var

# def use_global_variable():
#     global global_var
#     global_var = 0
#     for _ in range(1000000):
#         global_var += 1
#     return global_var

# # Create the inner function that accesses the enclosing variable
# inner_function = enclosing_function()

# # Measure time for local variable
# local_time = timeit.timeit(use_local_variable, number=10)

# # Measure time for global variable
# global_time = timeit.timeit(use_global_variable, number=10)

# # Measure time for enclosing variable
# enclosing_time = timeit.timeit(inner_function, number=10)

# print(local_time)
# print(global_time)
# print(enclosing_time)

import timeit
class MyClass:
    class_attr = 0
    
    def __init__(self):
        self.instance_attr = 0

obj = MyClass()

def access_class_attr():
    return MyClass.class_attr

def access_instance_attr():
    return obj.instance_attr

# Measure time for accessing class attribute
class_attr_time = timeit.timeit(access_class_attr, number=1000000)

# Measure time for accessing instance attribute
instance_attr_time = timeit.timeit(access_instance_attr, number=1000000)

print(f"Time accessing class attribute: {class_attr_time}")
print(f"Time accessing instance attribute: {instance_attr_time}")