import tkinter as tk
from PIL import Image, ImageTk
from queue import Queue, LifoQueue, PriorityQueue

# Define your code here
start_state = (0, False, False)
goal_state = (1, True, True)

ACTIONS = [
    ('Move chair', 1),
    ('Climb onto chair', 1),
    ('Use stick', 1),
    ('Climb down from chair', 1)
]

def heuristic(state):
    monkey_pos, has_chair, has_banana = state
    goals = 2
    if monkey_pos == 1 and has_chair:
        goals -= 1
    if monkey_pos == 1 and has_chair and has_banana:
        goals -= 1
    return goals

def bfs():
    
    frontier = Queue()
    frontier.put(start_state)

    total_moves = 0

    visited = set()
    visited.add(start_state)

    while not frontier.empty():       
        current_state = frontier.get()

        if current_state == goal_state:
            return total_moves
        for action, _ in ACTIONS:
            new_state = sequence_of_moves(current_state, action)

            if new_state not in visited:
                frontier.put(new_state)
                visited.add(new_state)

       
        total_moves += 1

    return -1 

def dfs():
    
    frontier = LifoQueue()
    frontier.put(start_state)

    total_moves = 0

    visited = set()
    visited.add(start_state)

    while not frontier.empty():
        current_state = frontier.get()

        if current_state == goal_state:
            return total_moves
        for action, _ in ACTIONS:
            new_state = sequence_of_moves(current_state, action)
            if new_state not in visited:
                frontier.put(new_state)
                visited.add(new_state)
        total_moves += 1

    return -1

    

def ucs():
    
    frontier = PriorityQueue()
    frontier.put((0, start_state))
    total_moves = 0

    cost_uptill = {start_state: 0}

    while not frontier.empty():
        current_cost, current_state = frontier.get()

        if current_state == goal_state:
            return total_moves

        for action, cost in ACTIONS:
            new_state = sequence_of_moves(current_state, action)
            new_cost = cost_uptill[current_state] + cost

            if new_state not in cost_uptill or new_cost < cost_uptill[new_state]:
                cost_uptill[new_state] = new_cost
                frontier.put((new_cost, new_state))

        total_moves += 1

    return -1
   
   

def best_fs():
    
    frontier = PriorityQueue()
    frontier.put((heuristic(start_state), start_state))

    total_moves = 0

    visited = set()
    visited.add(start_state)

    while not frontier.empty():

        _, current_state = frontier.get()

        if current_state == goal_state:
            return total_moves

        for action, _ in ACTIONS:
            new_state = sequence_of_moves(current_state, action)
            if new_state not in visited:
                frontier.put((heuristic(new_state), new_state))
                visited.add(new_state)

        total_moves += 1

    return -1 

def a_star():
    
    frontier = PriorityQueue()
    frontier.put((heuristic(start_state), 0, start_state))


    total_moves = 0

  
    cost_uptill = {start_state: 0}

    while not frontier.empty():

        _, current_cost, current_state = frontier.get()

        if current_state == goal_state:
            return total_moves

        for action, cost in ACTIONS:
            new_state = sequence_of_moves(current_state, action)
            new_cost = cost_uptill[current_state] + cost

            if new_state not in cost_uptill or new_cost < cost_uptill[new_state]:
                cost_uptill[new_state] = new_cost
                priority = new_cost + heuristic(new_state)
                frontier.put((priority, new_cost, new_state))

        total_moves += 1

    return -1 

    

def sequence_of_moves(state, action):
    
    monkey_pos, has_chair, has_banana = state
    if action == 'Move chair':
        return (1 - monkey_pos, has_chair, has_banana)
    elif action == 'Climb onto chair':
        return (monkey_pos, True, has_banana)
    elif action == 'Use stick':
        return (monkey_pos, has_chair, True)
    elif action == 'Climb down from chair':
        return (monkey_pos, False, has_banana)
    else:
        raise ValueError('Invalid action')



window = tk.Tk()


output_frame = tk.Frame(window)
output_frame.pack(side=tk.RIGHT)


output_label = tk.Label(output_frame, text="")
output_label.pack()


image_frame = tk.Frame(window)
image_frame.pack(side=tk.LEFT)


image = Image.open("img-o63vpeExCjN6mcfvKszygMMZ.png")
image = image.resize((600, 400))  
photo = ImageTk.PhotoImage(image)


image_label = tk.Label(image_frame, image=photo)
image_label.pack()


def show_output():
    
    output = f"Total Moves Required for :\n\n\n\nBreadth First Search: {bfs()}\n\nDepth First Search: {dfs()}\n\nUniform Cost Search: {ucs()}\n\nBest First Search: {best_fs()}\n\nA* Algorithm: {a_star()}"
    output_label.config(text=output)

button = tk.Button(window, text="Generate Output", command=show_output)
button.pack()


window.mainloop()
