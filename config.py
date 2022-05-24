# https://towardsdatascience.com/simple-trick-to-work-with-relative-paths-in-python-c072cdc9acb9

#  import os
# ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

# import os
# from config.definitions import ROOT_DIR
# print(os.path.join(ROOT_DIR, 'data', 'mydata.json'))


# relative_path 
# - data 
# -- mydata.json 
# - processes
# -- load_data.py

# import os
# print(os.path.dirname(__file__))
# # Results in
# # C:\projects\relative_path\processes

# import os
# print(os.path.join(os.path.dirname(__file__), '..', 'data', 'mydata.json'))
# # results in C:\projects\relative_path\processes\..\data\mydata.json

# print(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data', 'mydata.json')))
# # results in C:\projects\relative_path\data\mydata.json

# https://www.geeksforgeeks.org/python-os-path-relpath-method/
# # Path

# path = "/home / User / Desktop / file.txt"
  
# # Path of Start directory

# start = "/home / User / ihritik / file.txt"

# # Compute the relative file path
# # to the given path from the 
# # the given start directory.

# relative_path = os.path.relpath(path, start)
  
# # Print the relative file path
# # to the given path from the 
# # the given start directory.

# print(relative_path)
# ../../Desktop/file.txt