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
highlighted_path = []
accessibility_var = tk.IntVar()
accessibility_only_var = tk.IntVar()
edge_closure_var = tk.IntVar()


# SETTING UP BFS // DFS Functions

def bfs_shortest_paths(graph, start, accessible_only=False, respect_closures=False):
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
                edge_key = tuple(sorted([u, v]))
                edge_data = edges.get(edge_key, {})
                
                # Skip closed edges when respecting closures
                if respect_closures and edge_data.get('closed', False):
                    continue
                
                if accessible_only and not edge_data.get('accessible', True):
                    continue
                
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

def dfs_path(graph, start, target, accessible_only=False, respect_closures=False):
    visited = set()
    path = []
    order = []
    
    def dfs_visit(node):
        visited.add(node)
        order.append(node)
        path.append(node)
        
        if node == target:
            return True
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                edge_key = tuple(sorted([node, neighbor]))
                edge_data = edges.get(edge_key, {})
                
                if respect_closures and edge_data.get('closed', False):
                    continue
                
                if accessible_only and not edge_data.get('accessible', True):
                    continue
                
                if dfs_visit(neighbor):
                    return True
        
        path.pop()
        return False
    
    found = dfs_visit(start)
    return path if found else [], order

#Frame Layout 1 (GUI Interface)
frame = tk.Frame(master=app, background="#2b2d3b", width=350)
frame.pack(side = "left", fill = "y")
frame.pack_propagate(False)


#Frame Layout 2 (Graph Interface)
frame2 = tk.Frame(master=app, background="#2b2d3b")
frame2.pack(side = "right", fill = "both", expand = True)
graph_label = tk.Label(master=frame2, text = "Campus Map", background="#2b2d3b", foreground="#F8F8FF", font=("Segoe UI Black", 20))
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

distance_entry = tk.Entry(master = from_row, width=8, foreground ="#888888",
                      background= "#2b2d3b", font = ("Segoe UI Black", 12))
distance_entry.pack(side = "left", padx=5)
distance_entry.insert(0, "Distance")

accessibility_switch = tk.Checkbutton(master=from_row, text = "Access.", font = ("Segoe UI Black", 12), background= "#8A87A4", fg = "black",
                                      width=15, variable = accessibility_var)
accessibility_switch.pack(side = "left")

#TO

to_row = tk.Frame(master=frame, background= "#2b2d3b")
to_row.pack(side="top", padx=10, fill="x")


to_label = tk.Label(master=to_row, text="To:", background= "#2b2d3b", foreground = "#F8F8FF", font = ("Segoe UI Black", 14))
to_label.pack(side = "left", padx=(26,4), pady=5)
to_combo_box = ttk.Combobox(master=to_row, values = [""], width=5,
                             foreground ="#F8F8FF", font = ("Segoe UI Black", 15), background= "#2b2d3b")
to_combo_box.pack(side = "left", padx=1)

time_entry = tk.Entry(master = to_row, width=8, foreground ="#888888",
                      background= "#2b2d3b", font = ("Segoe UI Black", 12))
time_entry.pack(side = "left", padx=5)
time_entry.insert(0, "Time")

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


accessibility_switch_BFS_DFS = tk.Checkbutton(master=frame, text = "Accessibility", font = ("Segoe UI Black", 12),
                                              width=15, variable=accessibility_only_var, background="#676386", fg="black")
accessibility_switch_BFS_DFS.pack(side = "top")

edge_closure = tk.Checkbutton(master=frame, text = "Respect Closures", font = ("Segoe UI Black", 12),
                              width=15, variable=edge_closure_var, background="#676386", fg="black")
edge_closure.pack(side = "top")


#GRAPH

graph_frame = tk.Frame(master=frame2, bg="black")
graph_frame.pack()
comboboxes = [from_combo_box, to_combo_box, start_combo_box, end_combo_box]
#Frame for the graph
graph_canvas = tk.Canvas(frame2, bg="white", width=600, height=400)
graph_canvas.pack(fill="both", expand=True)


# Clears the Placeholder Text for Distance and Time Entry

def clear_distance_placeholder(event):
    if distance_entry.get() == "Distance":
        distance_entry.delete(0, tk.END)
        distance_entry.config(foreground="#F8F8FF")

def restore_distance_placeholder(event):
    if distance_entry.get() == "":
        distance_entry.insert(0, "Distance")
        distance_entry.config(foreground="#888888")

#Bindings
distance_entry.bind("<FocusIn>", clear_distance_placeholder)
distance_entry.bind("<FocusOut>", restore_distance_placeholder)

def clear_time_placeholder(event):
    if time_entry.get() == "Time":
        time_entry.delete(0, tk.END)
        time_entry.config(foreground="#F8F8FF")

def restore_time_placeholder(event):
    if time_entry.get() == "":
        time_entry.insert(0, "Time")
        time_entry.config(foreground="#888888")

#Bindings
time_entry.bind("<FocusIn>", clear_time_placeholder)
time_entry.bind("<FocusOut>", restore_time_placeholder)


# Add Building Button
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

    width = graph_canvas.winfo_width()
    height = graph_canvas.winfo_height()

    # makes it so nodes don't accidentally overlap
    #radius - determines distance between the nodes
    radius = 60
    max_attempts = 50

    for _ in range(max_attempts):
        x2 = random.randint(50, width - 50)
        y2 = random.randint(50, height - 50)
        overlap = False
    
        for (x1, y1) in node_positions.values():
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            if distance < radius * 2:
                overlap = True
                break
    
        if not overlap:
            break
    else:
    # if it uses all attempts, it places the node regardless of it overlaps
        x2 = random.randint(50, width - 50)
        y2 = random.randint(50, height - 50)

    node_positions[name] = (x2, y2)

    for combo in comboboxes:
        values = list(combo.cget("values"))
        if "" in values:
            values.remove("")
        if name not in values:
            values.append(name)
            combo.configure(values=values)

    draw_nodes()
    entry.delete(0, "end")


def draw_nodes():
    # Clears the canvas
    graph_canvas.delete("all")
    radius = 20

    # Create Edges
    for edge_key, edge_data in edges.items():
        n1, n2 = edge_key
        x1, y1 = node_positions[n1]
        x2, y2 = node_positions[n2]

        # Determines edge color
        is_in_path = False
        if len(highlighted_path) > 1:
            for i in range(len(highlighted_path) - 1):
                if (highlighted_path[i] == n1 and highlighted_path[i+1] == n2) or \
                   (highlighted_path[i] == n2 and highlighted_path[i+1] == n1):
                    is_in_path = True
                    break
        
        if edge_data['closed']:
            color = "red"
            width = 4
        elif is_in_path:
            color = "green"
            width = 4
        elif not edge_data['accessible']:
            color = "orange"
            width = 4
        else:
            color = "black"
            width = 4
        
        graph_canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
        
        # Draw weight labels
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        label = f"Distance:{edge_data['distance']} Time:{edge_data['time']}"
        graph_canvas.create_text(mid_x, mid_y - 10, text=label, 
                               fill="blue", font=("Arial", 9))

    # Draw nodes 
    for building, (x, y) in node_positions.items():
        # Highlight if in path
        if building in highlighted_path:
            fill_color = "green"
            outline_color = "green"
            outline_width = 3
        else:
            fill_color = "#676386"
            outline_color = "#F8F8FF"
            outline_width = 2
        
        graph_canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=fill_color, outline=outline_color, width=outline_width
        )
        graph_canvas.create_text(x, y, text=building, fill="white", 
                                font=("Segoe UI Black", 10))



def create_edge():
    a = from_combo_box.get().strip()
    b = to_combo_box.get().strip()

    if not a or not b:
        messagebox.showerror("Error", "Select two buildings!")
        return
    
    if a == b:
        messagebox.showerror("Error", "Select two unique buildings!")
        return

    dist_val = distance_entry.get().strip()
    time_val = time_entry.get().strip()
        
        # if placeholder, assign random number for distance and time
    if dist_val == "Distance" or not dist_val:
        messagebox.showerror("Error", "Please enter a valid distance!")
        return
    if time_val == "Time" or not time_val:
        messagebox.showerror("Error", "Please enter a valid time!")
        return
    try:
        distance = int(dist_val)
        time = int(time_val)
        # Non-positive values
        if distance <= 0 or time <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Distance and time must be positive numbers!")
        return
    
    if b not in graph[a]:
        graph[a].append(b)
    if a not in graph[b]:
        graph[b].append(a)

    accessible = accessibility_var.get() == 1
    edge_key = tuple(sorted([a, b]))
    edges[edge_key] = {
        'distance': distance,
        'time': time,
        'accessible': accessible,
        'closed': False
    }
    draw_nodes()

def randomize_weights():
    if not edges:
        messagebox.showinfo("Error", "No edges to randomize!")
        return
    
    for edge_key in edges:
        edges[edge_key]['distance'] = random.randint(1, 50)
        edges[edge_key]['time'] = random.randint(1, 50)
    draw_nodes()

def clear_graph():
    global graph, node_positions, edges, highlighted_path
    graph = {}
    node_positions = {}
    highlighted_path = []
    edges = {}
    
    for combo in comboboxes:
        combo.configure(values=[""])
    
    graph_canvas.delete("all")
    
def toggle_edge_closure(event):
    x, y = event.x, event.y
    
    for edge_key, edge_data in edges.items():
        n1, n2 = edge_key
        x1, y1 = node_positions[n1]
        x2, y2 = node_positions[n2]
        
        # Calculate midpoint
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        # Check if click is near midpoint
        distance_to_mid = math.sqrt((x - mid_x)**2 + (y - mid_y)**2)
        
        if distance_to_mid < 30:
            edge_data['closed'] = not edge_data['closed']
            draw_nodes()
            return

def run_bfs():
    start = start_combo_box.get().strip()
    end = end_combo_box.get().strip()
    
    if not start or not end:
        messagebox.showerror("Error", "Select start and end buildings!")
        return
    
    if start not in graph or end not in graph:
        messagebox.showerror("Error", "Invalid building selection!")
        return
    
    accessible_only = accessibility_only_var.get() == 1
    respect_closures = edge_closure_var.get() == 1
    
    dist, parent, order = bfs_shortest_paths(graph, start, accessible_only, respect_closures)
    path = reconstruction_path(parent, start, end)
    
    if not path:
        messagebox.showinfo("No Path", f"No path found from {start} to {end}")
        return
    
    global highlighted_path
    highlighted_path = path
    draw_nodes()

def run_dfs():
    start = start_combo_box.get().strip()
    end = end_combo_box.get().strip()
    
    # No buildings selected
    if not start or not end:
        messagebox.showerror("Error", "Select start and end buildings!")
        return
    
    # Invalid selection
    if start not in graph or end not in graph:
        messagebox.showerror("Error", "Invalid building selection!")
        return
    
    accessible_only = accessibility_only_var.get() == 1
    respect_closures = edge_closure_var.get() == 1
    
    path, order = dfs_path(graph, start, end, accessible_only, respect_closures)
    
    # No path found
    if not path:
        messagebox.showinfo("No Path", f"No path found from {start} to {end}")
        return
    
    global highlighted_path
    highlighted_path = path
    draw_nodes()

# Binds the commands to the GUI
add_button.configure(command=add_building)
change_button.configure(command=create_edge)
randomize_button.configure(command=randomize_weights)
clear_button.configure(command=clear_graph)
BFS_button.configure(command=run_bfs)
DFS_button.configure(command=run_dfs)
graph_canvas.bind("<Button-1>", toggle_edge_closure)

app.mainloop()