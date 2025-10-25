# Student Name: Tom Thach
# Titan Email: tomthach@csu.fullerton.edu
# Project: CPSC 335 – Interactive Campus Navigation System
# Date: 10-19-2025

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from collections import deque
import random
import math

app = tk.Tk()

app.geometry("1200x700")

# Styling for ComboBoxes

style= ttk.Style()
style.theme_use('clam')
style.configure("TCombobox",
                fieldbackground="#2b2d3b",
                background="#494c65",
                foreground="#F8F8FF",
                font=("Segoe UI Black", 15))


graph = {}
node_positions = {}
edges = {}
comboboxes = []


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




#Frame Layout 1 (asdasdsad)
frame = tk.Frame(master=app, background="#2b2d3b", width=350)
frame.pack(side = "left", fill = "y")
frame.pack_propagate(False)


#Frame Layout 2 (Graph)
frame2 = tk.Frame(master=app, background="#2b2d3b")
frame2.pack(side = "right", fill = "both", expand = True)
graph_label = tk.Label(master=frame2, text = "Campus Map")
graph_label.pack(pady=10)



#LABEL
label = tk.Label(master=frame, text = "🧱 Add Building", background= "#2b2d3b", foreground= "#F8F8FF", font = ("Segoe UI Black", 18))
label.pack(side = "top", padx=10, pady=(25,5))

entry = tk.Entry(master=frame, width=300, foreground="#F8F8FF", 
                 background= "#2b2d3b", font = ("Segoe UI Black", 20))
entry.pack(side = "top", padx=10, pady=2)


#Creating Button Frame within the Frame
button_layout = tk.Frame(master=frame, background= "#2b2d3b")
button_layout.pack(side="top", padx=14, pady=1, fill="x")

#Buttons
clear_button = tk.Button(master=button_layout, text = "Clear", background = "#676386",
                foreground="#F8F8FF", font = ("Segoe UI Black", 12), width = 10, height=1)
clear_button.pack(side = "left", padx=(40,20), pady=4)

add_button = tk.Button(master=button_layout, text = "Add", background = "#8A87A4",
                 foreground="#F8F8FF", font = ("Segoe UI Black", 12), width = 10, height=1)
add_button.pack(side = "left", padx=10, pady=4)


#Connect Buildings
connecting_building_label = tk.Label(master=frame, background= "#2b2d3b", text = "Connect Buildings", 
                                     foreground = "#F8F8FF", font = ("Segoe UI Black", 18))
connecting_building_label.pack(side = "top", padx=10, pady=(30,0))


#FROM
from_row = tk.Frame(master=frame, background= "#2b2d3b")
from_row.pack(side="top", padx=10, pady=(4, 0), fill="x")


from_label = tk.Label(master=from_row, text="From:", background= "#2b2d3b", foreground = "#F8F8FF", font = ("Segoe UI Black", 14))
from_label.pack(side = "left", padx=(2,4), pady=2)
from_combo_box = ttk.Combobox(master=from_row, values = [""], width=5,
                             foreground ="#F8F8FF", font = ("Segoe UI Black", 15), background= "#2b2d3b")
from_combo_box.pack(side = "left", padx=1)

distance_entry = tk.Entry(master = from_row, width=8, foreground ="#F8F8FF",
                      background= "#2b2d3b", font = ("Segoe UI Black", 12))
distance_entry.pack(side = "left", padx=5)

accessibility_switch = tk.Checkbutton(master=from_row, text = "Access.", font = ("Segoe UI Black", 12), background= "#8A87A4", fg = "#F8F8FF" )
accessibility_switch.pack(side = "left")

#TO

to_row = tk.Frame(master=frame, background= "#2b2d3b")
to_row.pack(side="top", padx=10, fill="x")


to_label = tk.Label(master=to_row, text="To:", background= "#2b2d3b", foreground = "#F8F8FF", font = ("Segoe UI Black", 14))
to_label.pack(side = "left", padx=(26,4), pady=5)
to_combo_box = ttk.Combobox(master=to_row, values = [""], width=5,
                             foreground ="#F8F8FF", font = ("Segoe UI Black", 15), background= "#2b2d3b")
to_combo_box.pack(side = "left", padx=1)

time_entry = tk.Entry(master = to_row, width=8, foreground ="#F8F8FF",
                      background= "#2b2d3b", font = ("Segoe UI Black", 12))
time_entry.pack(side = "left", padx=5)

change_button = tk.Button(master=to_row, text = "Change", background = "#8A87A4",
                 foreground ="#F8F8FF", font = ("Segoe UI Black", 12), width = 6, height=1)
change_button.pack(side = "left", padx=1, pady=4)


#Randomize Weights
randomize_label = tk.Label(master=frame, text = "Randomize All Weights", foreground = "#F8F8FF", font = ("Segoe UI Black", 18), 
                           background= "#2b2d3b")
randomize_label.pack(side = "top", padx=10, pady=(30,0))

randomize_button = tk.Button(master=frame, text = "Randomize", background = "#676386",
                             foreground ="#F8F8FF", font = ("Segoe UI Black", 12), width = 10, height=1)
randomize_button.pack(side = "top", padx=10, pady=(1, 30))

#BFS and DFS Implementation

BFS_DFS_label = tk.Label(master=frame, text = "BFS/DFS Test", foreground = "#F8F8FF", font = ("Segoe UI Black", 18),
                         background= "#2b2d3b")
BFS_DFS_label.pack(side = "top", padx=10)

#Start 
start_row = tk.Frame(master=frame, background= "#2b2d3b")
start_row.pack(side="top", padx=10, pady=(4, 0), fill="x")


start_label = tk.Label(master=start_row, text="Start:", foreground = "#F8F8FF", font = ("Segoe UI Black", 14),
                       background= "#2b2d3b")
start_label.pack(side = "left", padx=(2,4), pady=2)
start_combo_box = ttk.Combobox(master=start_row, values = [""], width=4,
                               foreground ="#F8F8FF", font = ("Segoe UI Black", 15), background= "#2b2d3b")
start_combo_box.pack(side = "left", padx=1)

end_label = tk.Label(master=start_row, text="End:", foreground = "#F8F8FF", font = ("Segoe UI Black", 14),
                     background= "#2b2d3b")
end_label.pack(side = "left", padx=(20,4), pady=2)
end_combo_box = ttk.Combobox(master=start_row, values = [""], width=4,
                               foreground ="#F8F8FF", font = ("Segoe UI Black", 15), background= "#2b2d3b")
end_combo_box.pack(side = "left", padx=1)



BFS_DFS_layout = tk.Frame(master=frame, background= "#2b2d3b")
BFS_DFS_layout.pack(side="top", padx=14, pady=10, fill="x")

# Buttons
BFS_button = tk.Button(master=BFS_DFS_layout, text="BFS", background="#676386",
                       foreground ="#F8F8FF", font=("Segoe UI Black", 12), width = 5, height=1)
BFS_button.pack(side="left", padx=(80, 20), pady=4)

DFS_button = tk.Button(master=BFS_DFS_layout, text="DFS", background="#676386",
                       foreground ="#F8F8FF", font=("Segoe UI Black", 12), width = 5, height=1)
DFS_button.pack(side="left", padx=10, pady=4)


accessibility_switch_BFS_DFS = tk.Checkbutton(master=frame, text = "Accessibility", font = ("Segoe UI Black", 12), width=2)
accessibility_switch_BFS_DFS.pack(side = "top")

edge_closure = tk.Checkbutton(master=frame, text = "Edge Closure", font = ("Segoe UI Black", 12))
edge_closure.pack(side = "top", padx=(5,1))


#GRAPH


def add_building():
    name = entry.get().strip()
    if not name:
        tk.messagebox.showerror("ERROR", "Building name cannot be empty")
        return
    if name in graph:
        tk.messagebox.showerror("ERROR", "Building name already exists")
        return

    graph[name] = []
    print(graph)
    entry.delete(0, "end")





def create_edge():
    a = from_combo_box.get().strip()
    b = to_combo_box.get().strip()

    if not a or not b:
        messagebox.showerror("Error", "Select two buildings!")
        return
    
    if a == b:
        messagebox.showerror("Error", "Select two unique buildings!")
        return

    try:
        distance = int(distance_entry.get())
        time = int(time_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Distance and time must be numbers!")
        return


add_button.configure(command=add_building)
change_button.configure(command=create_edge)

app.mainloop()