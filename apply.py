# Student Name: Tom Thach
# Titan Email: tomthach@csu.fullerton.edu
# Project: CPSC 335 – Interactive Campus Navigation System
# Date: 10-19-2025

import tkinter as tk
from tkinter import messagebox
from customtkinter import *
from collections import deque


app = CTk()

app.geometry("1200x700")
set_appearance_mode("dark")

# SETTING UP BFS // DFS Functions

def bfs_shortest_paths(graph, start):
    dist = {v: float('inf') for v in graph}
    parent = {v: None for v in graph}
    visited = set()
    q = deque([start])
    visited.add(start)
    dist[start] = 0
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)
    return dist, parent, order

def reconstruction_path(parent, start, target):
    rev_path = []
    cur = target
    while cur is not None:
        rev_path.append(cur)
        if cur == start:
            break
        cur = parent.get(cur, None)
    if not rev_path or rev_path[-1] != start:
        return []
    return list(reversed(rev_path))

def dfs_cycle_and_topo(graph):
    color = {v: 0 for v in graph}
    postorder = []
    has_cycle = False
    def visit(u):
        nonlocal has_cycle
        color[u] = 1
        for v in graph[u]:
            if color[v] == 0:
                visit(v)
            elif color[v] == 1:
                has_cycle = True
                return
        color[u] = 2
        postorder.append(u)
    for node in graph:
        if color[node] == 0:
            visit(node)
        if has_cycle:
            return True, []
    topo = list(reversed(postorder))
    return False, topo


graph = {}

def add_building():
    name = entry.get().strip()
    if not name:
        tk.messagebox.showerror("ERROR", "Building name cannot be empty")
        return
    if name in graph:
        tk.messagebox.showerror("ERROR", "Building name already exists")

    graph[name] = []
    print(graph)




#Frame Layout 1 (asdasdsad)
frame = CTkFrame(master=app, fg_color="#2b2d3b", border_color="#494c65", border_width=6, width=350, corner_radius=0)
frame.pack(side = LEFT, fill = "y")
frame.pack_propagate(False)


#Frame Layout 2 (Graph)
frame2 = CTkFrame(master=app, fg_color="transparent", border_color="#494c65", border_width=6, corner_radius=0)
frame2.pack(side = RIGHT, fill = "both", expand = True)
graph_label = CTkLabel(master=frame2, text = "Campus Map")
graph_label.pack(pady=10)



#LABEL
label = CTkLabel(master=frame, text = "🧱 Add Building", text_color= "#F8F8FF", font = ("Segoe UI Black", 18))
label.pack(side = TOP, padx=10, pady=(25,5))

entry = CTkEntry(master=frame, placeholder_text="Names...", width=300, text_color="#F8F8FF", 
                 fg_color= "#2b2d3b", border_color="#494c65", border_width= 4, font = ("Segoe UI Black", 20))
entry.pack(side = TOP, padx=10, pady=2)


#Creating Button Frame within the Frame
button_layout = CTkFrame(master=frame, fg_color="transparent")
button_layout.pack(side=TOP, padx=14, pady=1, fill="x")

#Buttons
clear_button = CTkButton(master=button_layout, text = "Clear", corner_radius=10, fg_color = "#676386", border_color="#494c65", border_width=3,
                text_color="#F8F8FF", font = ("Segoe UI Black", 15), hover_color="#BCB8DE")
clear_button.pack(side = LEFT, padx=10, pady=4)

add_button = CTkButton(master=button_layout, text = "Add", corner_radius=10, fg_color = "#8A87A4", border_color="#494c65", border_width=3,
                 text_color="#F8F8FF", font = ("Segoe UI Black", 15), hover_color="#BCB8DE")
add_button.pack(side = LEFT, padx=10, pady=4)
add_button.configure(command=add_building)

#Connect Buildings
connecting_building_label = CTkLabel(master=frame, text = "Connect Buildings", text_color= "#F8F8FF", font = ("Segoe UI Black", 18))
connecting_building_label.pack(side = TOP, padx=10, pady=(50,0))


#FROM
from_row = CTkFrame(master=frame, fg_color="transparent")
from_row.pack(side=TOP, padx=10, pady=(4, 0), fill="x")


from_label = CTkLabel(master=from_row, text="From:", text_color= "#F8F8FF", font = ("Segoe UI Black", 18))
from_label.pack(side = LEFT, padx=(2,4), pady=2)
from_combo_box = CTkComboBox(master=from_row, values = ["CS", "LIB", "TSU"], width=80, border_color="#494c65", border_width=3,
                             text_color="#F8F8FF", font = ("Segoe UI Black", 15), fg_color= "#2b2d3b", button_color="#494c65")
from_combo_box.pack(side = LEFT, padx=1)

distance_entry = CTkEntry(master = from_row, placeholder_text="Distances", width=80, text_color="#F8F8FF",
                      fg_color= "#2b2d3b", border_color="#494c65", border_width= 4, font = ("Segoe UI Black", 12))
distance_entry.pack(side = LEFT, padx=5)

accessibility_switch = CTkSwitch(master=from_row, text = "Access.", button_color="#8A87A4", progress_color="#B4B1CD", 
                                 font = ("Segoe UI Black", 12))
accessibility_switch.pack(side = LEFT)

#TO

to_row = CTkFrame(master=frame, fg_color="transparent")
to_row.pack(side=TOP, padx=10, fill="x")


to_label = CTkLabel(master=to_row, text="To:", text_color= "#F8F8FF", font = ("Segoe UI Black", 18))
to_label.pack(side = LEFT, padx=(26,4), pady=2)
to_combo_box = CTkComboBox(master=to_row, values = ["CS", "LIB", "TSU"], width=80, border_color="#494c65", border_width=3,
                             text_color="#F8F8FF", font = ("Segoe UI Black", 15), fg_color= "#2b2d3b", button_color="#494c65")
to_combo_box.pack(side = LEFT, padx=1)

time_entry = CTkEntry(master = to_row, placeholder_text="Times", width=80, text_color="#F8F8FF",
                      fg_color= "#2b2d3b", border_color="#494c65", border_width= 4, font = ("Segoe UI Black", 12))
time_entry.pack(side = LEFT, padx=5)

change_button = CTkButton(master=to_row, text = "Change", corner_radius=10, fg_color = "#8A87A4", border_color="#494c65", border_width=3,
                 text_color="#F8F8FF", font = ("Segoe UI Black", 15), hover_color="#BCB8DE")
change_button.pack(side = LEFT, padx=1, pady=4)


#Randomize Weights
randomize_label = CTkLabel(master=frame, text = "Randomize All Weights", text_color= "#F8F8FF", font = ("Segoe UI Black", 18))
randomize_label.pack(side = TOP, padx=10, pady=(50,0))

randomize_button = CTkButton(master=frame, text = "Randomize", corner_radius=10, fg_color = "#676386", border_color="#494c65", border_width=3,
                text_color="#F8F8FF", font = ("Segoe UI Black", 15), hover_color="#BCB8DE")
randomize_button.pack(side = TOP, padx=10, pady=(1, 50))

#BFS and DFS Implementation

BFS_DFS_label = CTkLabel(master=frame, text = "BFS/DFS Test", text_color= "#F8F8FF", font = ("Segoe UI Black", 18))
BFS_DFS_label.pack(side = TOP, padx=10)

#Start 
start_row = CTkFrame(master=frame, fg_color="transparent")
start_row.pack(side=TOP, padx=10, pady=(4, 0), fill="x")


start_label = CTkLabel(master=start_row, text="Start:", text_color= "#F8F8FF", font = ("Segoe UI Black", 18))
start_label.pack(side = LEFT, padx=(2,4), pady=2)
start_combo_box = CTkComboBox(master=start_row, values = ["CS", "LIB", "TSU"], width=80, border_color="#494c65", border_width=3,
                             text_color="#F8F8FF", font = ("Segoe UI Black", 15), fg_color= "#2b2d3b", button_color="#494c65")
start_combo_box.pack(side = LEFT, padx=1)

end_label = CTkLabel(master=start_row, text="End:", text_color= "#F8F8FF", font = ("Segoe UI Black", 18))
end_label.pack(side = LEFT, padx=(20,4), pady=2)
end_combo_box = CTkComboBox(master=start_row, values = ["CS", "LIB", "TSU"], width=80, border_color="#494c65", border_width=3,
                             text_color="#F8F8FF", font = ("Segoe UI Black", 15), fg_color= "#2b2d3b", button_color="#494c65")
end_combo_box.pack(side = LEFT, padx=1)



BFS_DFS_layout = CTkFrame(master=frame, fg_color="transparent")
BFS_DFS_layout.pack(side=TOP, padx=14, pady=10, fill="x")

# Buttons
BFS_button = CTkButton(master=BFS_DFS_layout, text="BFS", corner_radius=10, fg_color="#676386",
                       border_color="#494c65", border_width=3, text_color="#F8F8FF", font=("Segoe UI Black", 15), hover_color="#BCB8DE")
BFS_button.pack(side=LEFT, padx=10, pady=4)

DFS_button = CTkButton(master=BFS_DFS_layout, text="DFS", corner_radius=10, fg_color="#676386",
                       border_color="#494c65", border_width=3, text_color="#F8F8FF", font=("Segoe UI Black", 15), hover_color="#BCB8DE")
DFS_button.pack(side=LEFT, padx=10, pady=4)

accessibility_switch_BFS_DFS = CTkSwitch(master=frame, text = "Accessibility", button_color="#8A87A4", progress_color="#B4B1CD", 
                                 font = ("Segoe UI Black", 12))
accessibility_switch_BFS_DFS.pack(side = TOP)

edge_closure = CTkSwitch(master=frame, text = "Edge Closure", button_color="#8A87A4", progress_color="#B4B1CD", 
                                 font = ("Segoe UI Black", 12))
edge_closure.pack(side = TOP, padx=(5,1))

#STATUS BOX
status_textbox = CTkTextbox(master=frame, corner_radius=16, scrollbar_button_color="#2b2d3b", border_color="#494c65", 
                            fg_color="#2b2d3b", border_width=4, width=450, height=2)
status_textbox.pack(side = TOP, padx = 8, pady = 20)

status_textbox.configure(state="disabled")


#GRAPH


app.mainloop()