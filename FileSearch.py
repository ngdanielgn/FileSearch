# Python 2.7
# Daniel Nguyen
# danielnguyen741@gmail.com

# Script that takes user input to recursively walk down a root directory and
# output number of files found that contain "keyword"
# per directory and output a graph

import os, re
import matplotlib.pyplot as plt
import numpy as npy
from collections import OrderedDict

root_dir = raw_input('Enter root directory: ')
keyword = raw_input('Enter keyword: ')
root_dir = root_dir.rstrip()
file_dict = {}

# Breadth-first search of directory checks each file
# if file contains "keyword"
def file_contains(working_dir,keyword, sub_dir = ''):
    # Retrieves root, directory, and files of working directory
        root = next(os.walk(working_dir))[0]
        dirs = next(os.walk(working_dir))[1]
        files = next(os.walk(working_dir))[2]

        sub_dir = split_path_name(working_dir, sub_dir)
        for file in files:
            # Appends file name to directory to retrieve full file path
            file_path = os.path.join(root, file)

            # Initializes dictionary to 0
            if sub_dir not in file_dict:
                file_dict[sub_dir] = 0

            with open(file_path, 'r') as myfile:
                data = myfile.read()

            # Checks if file contains keyword regular expression
            # if true increment dictionary key by 1
            if bool(re.search(keyword, data)):
               file_dict[sub_dir] += 1

        # Recurse into next directory
        for dir in dirs:
            next_dir = os.path.join(working_dir, dir)
            file_contains(next_dir, keyword, sub_dir)

# Prints out sorted dictionary and dot plo
def output(file_dict):
    print sorted(file_dict.items())
    file_dict = OrderedDict(sorted(file_dict.items()))

    graph = npy.arange(len(file_dict))
    plt.plot(graph, file_dict.values(), 'ro')
    plt.xticks(graph, file_dict.keys(), rotation=13)
    plt.yticks(npy.arange(0, max(file_dict.values())+2, 1))
    plt.ylim(0, max(file_dict.values())+2)

    plt.title('Number of Files with Keyword')
    plt.xlabel('Subdirectory Names')
    plt.ylabel('Count')
    plt.show()

# Creates path name that starts with initial directory
# and appends the next directory
def split_path_name(path, curr_dir = ''):
    new_curr = os.path.basename(path)
    if curr_dir != '':
        return os.path.join(curr_dir, new_curr)
    else:
        return new_curr


if keyword != '':
    try:
        file_contains(root_dir, keyword)
    except StopIteration:
        print "Directory Not Found"
    else:
        output(file_dict)
else:
    print "No keyword entered"


# Test Cases
# Enter empty root directory
# Result: output "Directory Not Found" process exits

# Enter whitespace for root directory
# Result: output "Directory Not Found" process exits

# Enter empty keyword
# Result: Output "No keyword entered" process exits

# Enter whitespace for keyword
# Result: Script will continue as normal

# Enter missing root directory
# Result: Output "Directory Not Found" process exits

# Test with empty file
# Result: Script continues as normal

# Test with multiple folders and files
# Result: Script continues as normal

# File is an executable
# Result: Function will skip over file
