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

# import timeit
# class MyClass:
#     class_attr = 0
    
#     def __init__(self):
#         self.instance_attr = 0

# obj = MyClass()

# def access_class_attr():
#     return MyClass.class_attr

# def access_instance_attr():
#     return obj.instance_attr

# # Measure time for accessing class attribute
# class_attr_time = timeit.timeit(access_class_attr, number=1000000)

# # Measure time for accessing instance attribute
# instance_attr_time = timeit.timeit(access_instance_attr, number=1000000)

# print(f"Time accessing class attribute: {class_attr_time}")
# print(f"Time accessing instance attribute: {instance_attr_time}")

import timeit

class MyClass:
    class_var_int = 1

    def method_access_class_var_int(self):
        return MyClass.class_var_int

    def method_access_local_var_int(self):
        local_var = 1
        return local_var

obj = MyClass()

# Timing access to a class variable (int)
access_class_var_int_time = timeit.timeit('obj.method_access_class_var_int()', globals=globals(), number=1000000)

# Timing access to a local variable (int)
access_local_var_int_time = timeit.timeit('obj.method_access_local_var_int()', globals=globals(), number=1000000)

print(f"Time to access a class variable (int): {access_class_var_int_time}")
print(f"Time to access a local variable (int): {access_local_var_int_time}")

# import timeit
# import numpy as np

# class MyClass:
#     class_var = np.uint64(1)

#     def method_access_class_var(self):
#         return MyClass.class_var

#     def method_create_local_var(self):
#         local_var = np.uint64(1)
#         return local_var

#     def method_create_local_int(self):
#         local_var = 1
#         return local_var

# obj = MyClass()

# # Timing access to a class variable (np.uint64)
# access_class_var_time = timeit.timeit('obj.method_access_class_var()', globals=globals(), number=1000000)

# # Timing creation of a local variable (np.uint64)
# create_local_var_time = timeit.timeit('obj.method_create_local_var()', globals=globals(), number=1000000)

# # Timing creation of a local variable (native int)
# create_local_int_time = timeit.timeit('obj.method_create_local_int()', globals=globals(), number=1000000)

# print(f"Time to access a class variable (np.uint64): {access_class_var_time}")
# print(f"Time to create a local variable (np.uint64): {create_local_var_time}")
# print(f"Time to create a local variable (native int): {create_local_int_time}")

# import timeit

# def bitwise_and_twice(a, b):
#     return a & b  & c

# def bitwise_and_once(a, b):
#     temp = a & b
#     return temp

# # Example values
# a = 0b1101101
# b = 0b1011011
# c = 0b1110110

# # Timing bitwise AND operation called twice
# time_twice = timeit.timeit('bitwise_and_twice(a, b)', globals=globals(), number=1000000)

# # Timing bitwise AND operation stored and used
# time_once = timeit.timeit('bitwise_and_once(a, b)', globals=globals(), number=1000000)

# print(f"Time to call bitwise AND operation twice: {time_twice}")
# print(f"Time to store and reuse bitwise AND operation: {time_once}")

"""
        ##############################################################
        # For each Figure # Blue
        ##############################################################
        ########################## Pawns #############################
        for fig in Board.l_blue_p:
            # attacking Pawns
            if((fig & Board.blue_p_hit_right << Board.bphr) | (fig & Board.blue_p_hit_left << Board.bphl)) & Board.red:
                # untargeted
                if fig & ~Board.red_hits:
                    eval += b
                # targeted & protected
                elif fig & Board.blue_hits:
                    eval += b
                # targeted
                else:
                    eval += b

            # non-attacking Pawns
            else:
                # targeted
                if fig & Board.red_hits:
                    # protected
                    if fig & Board.blue_hits:
                        eval += b
                    
                    # unprotected
                    else:
                        eval += b
                # untargeted & non-attacking
                else:
                    eval += b
        
            ##############################################################
            # Certain Pawn Areas # Blue
            ##############################################################
            
            # Targeted
            if fig & ~Board.red_hits:
                # Valueble Pawn H7 untargeted
                if fig & Board.H7:
                    eval += b
                    # no Red Pawn on C8
                    if ~(Board.C8 & Board.red_p):
                        eval += b

                # Valueble Pawn H2 untargeted
                if blue_p_untarget & Board.H2:
                    eval += b
                    # no Red Pawn on F8          
                    if ~(Board.F8 & Board.red_p):
                        eval += b
                

            
        # TODO: Knights
        ########################## Knights #############################
        for fig in Board.l_blue_k: 
            # non-targeted
            if fig & ~Board.red_hits:

            ##############################################################
            # Certain Knight Areas # Blue
            ##############################################################

                # Possible Knight on r5 untargeted
                if fig & Board.r5:
                    eval += b

                # Knight on r5 untargeted or at least one possible takeback
                if fig & Board.r4:
                    eval += b
        """
