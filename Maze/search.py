# search.py
# ---------------
# Created by Yaya Wihardi (yayawihardi@upi.edu) on 15/03/2020

# Fungsi search harus me-return path.
# Path berupa list tuples dengan format (row, col)
# Path merupakan urutan states menuju goal.
# maze merupakan object dari Maze yang merepresentasikan keadaan lingkungan
# beberapa method dari maze yang dapat digunakan:

# getStart() : return tuple (row, col) -> mendapatkan initial state
# getObjectives() : return list of tuple [(row1, col1), (row2, col2) ...] -> mendapatkan list goal state
# getNeighbors(row, col) : input posisi, return list of tuple [(row1, col1), (row2, col2) ...]
#                          -> mendapatkan list tetangga yg mungkin (expand/sucessor functiom)
# isObjective(row, col) : return true/false -> goal test function

import heapq
from copy import deepcopy
import queue
jalur = []


def cek(isFound, parent, initial_state, goal_state):
    if(not isFound):
        return
    findPath(parent, goal_state, initial_state)


def findPath(parent, curr_Node, initial_state):
    if(curr_Node == initial_state):
        jalur.append(curr_Node)
        return
    findPath(parent, parent[curr_Node], initial_state)
    jalur.append(curr_Node)


def bfs(maze, initial_state):
    fringe = queue.Queue()
    explored = []
    parent = {}
    fringe.put(initial_state)

    while not fringe.empty():
        currpath = fringe.get()
        row = currpath[0]
        col = currpath[1]
        if maze.isObjective(row, col):
            return (True, parent)
        if currpath not in explored:
            for item in maze.getNeighbors(row, col):
                if item in explored:
                    continue
                fringe.put(item)
                parent[item] = currpath
            explored.append(currpath)
    return (False, parent)


def search(maze):
    initial_state = maze.getStart()
    goal_state = maze.getObjectives()[0]
    cekFound, Parent = bfs(maze, initial_state)
    cek(cekFound, Parent, initial_state, goal_state)
    if(not cekFound):
        return
    else:
        return jalur

# master search


def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)


def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    queue = []
    visited = set()
    queue.append([maze.getStart()])
    while queue:
        cur_path = queue.pop(0)
        cur_row, cur_col = cur_path[-1]
        if (cur_row, cur_col) in visited:
            continue
        visited.add((cur_row, cur_col))
        if maze.isObjective(cur_row, cur_col):
            return cur_path, len(visited)
        for item in maze.getNeighbors(cur_row, cur_col):
            if item not in visited:
                queue.append(cur_path + [item])
    return [], 0


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    stack = []
    visited = set()
    stack.append([maze.getStart()])
    while stack:
        cur_path = stack.pop(-1)
        cur_row, cur_col = cur_path[-1]
        if (cur_row, cur_col) in visited:
            continue
        visited.add((cur_row, cur_col))
        if maze.isObjective(cur_row, cur_col):
            return cur_path, len(visited)
        for item in maze.getNeighbors(cur_row, cur_col):
            if item not in visited:
                stack.append(cur_path + [item])
    return [], 0


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    pq = queue.PriorityQueue()
    visited = set()
    result_row, result_col = maze.getObjectives()[0]
    start_row, start_col = maze.getStart()
    # pq item - tuple: (distance, path list)
    cost = abs(start_row-result_row) + abs(start_col - result_col)
    pq.put((cost, [maze.getStart()]))
    while not pq.empty():
        cur_path = pq.get()[1]
        cur_row, cur_col = cur_path[-1]

        for item in maze.getNeighbors(cur_row, cur_col):
            item_row, item_col = item[0], item[1]
            if maze.isObjective(item_row, item_col):
                visited.add(item)
                cur_path += [item]
                return cur_path, len(visited)

            if item not in visited:
                visited.add(item)
                cost = abs(item[0] - result_row) + abs(item[1] - result_col)
                pq.put((cost, cur_path + [item]))
    return [], 0

# ====================================== PART 2 ===============================================
# astar for part 1&2
# self-built data structure


class ctor:
    def __init__(self, row, col, cost, tcost):
        self.row = row
        self.col = col
        self.position = (row, col)
        self.sofarcost = 0
        self.cost = cost  # heuristic
        self.tcost = tcost  # f = g + h（total）
        self.prev = None
        self.not_visited = []
        self.objective_left = []

    def __lt__(self, other):
        return self.tcost < other.tcost


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    num_of_state = 0
    if len(maze.getObjectives()) == 1:
        start_1 = maze.getStart()
        end_1 = maze.getObjectives()[0]
        return cost_sofar(maze, start_1, end_1)

    start = maze.getStart()
    goals_left = maze.getObjectives()
    goals_left.insert(0, start)
    edge_list = {}
    heuristic_list = {}
    # building graph for mst
    for i in goals_left:
        for j in goals_left:
            if i != j:
                construct_path = cost_sofar(maze, i, j)[0]
                edge_list[(i, j)] = construct_path
                heuristic_list[(i, j)] = len(construct_path)
                num_of_state += 10
    not_visited_list = {}
    visited = {}
    cur_path = queue.PriorityQueue()
    mst_weights = get_MST(maze, goals_left, heuristic_list)
    start_r, start_c = maze.getStart()
    start_state = ctor(start_r, start_c, 0, mst_weights)
    start_state.not_visited = maze.getObjectives()

    cur_path.put(start_state)
    not_visited_list[(start_r, start_c)] = len(start_state.not_visited)

    while len(goals_left):
        cur_state = cur_path.get()
        if not cur_state.not_visited:
            break
        for n in cur_state.not_visited:
            n_row, n_col = n
            n_cost = cur_state.cost + \
                heuristic_list[(cur_state.position, n)] - 1
            next_state = ctor(n_row, n_col, n_cost, 0)
            next_state.prev = cur_state
            next_state.not_visited = deepcopy(cur_state.not_visited)
            if n in next_state.not_visited:
                next_state.not_visited.remove(n)
            visited[(n_row, n_col)] = 0
            not_visited_list[n] = len(next_state.not_visited)
            mst_weights = get_MST(maze, cur_state.not_visited, heuristic_list)
            next_state.tcost = n_cost + mst_weights
            a = len(goals_left) - 1
            if a:
                next_state.tcost += len(next_state.not_visited)
            cur_path.put(next_state)
    ret_path1 = print_path(maze, edge_list, cur_state, visited)
    return ret_path1, num_of_state


def print_path(maze, path, state, visited):
    ret_path = []
    goals_list = []
    while state:
        goals_list.append(state.position)
        state = state.prev
    total_dot = len(goals_list)-1
    for i in range(total_dot):
        ret_path += path[(goals_list[i], goals_list[i+1])][:-1]
    start = maze.getStart()
    ret_path.append(start)
    ret_path[::-1]
    return ret_path


def get_MST(maze, goals, heuristic_list):
    # Prim
    if not len(goals):
        return 0
    start = goals[0]
    visited = {}
    visited[start] = True
    MST_edges = []
    mst_weights = 0
    while len(visited) < len(goals):
        qe = queue.PriorityQueue()
        for v in visited:
            for n in goals:
                if visited.get(n) == True:
                    continue
                new_edge = (v, n)
                new_cost = heuristic_list[new_edge]-2
                qe.put((new_cost, new_edge))
        add_edge = qe.get()
        MST_edges.append(add_edge[1])
        mst_weights += add_edge[0]
        visited[add_edge[1][1]] = True
    return mst_weights


def cost_sofar(maze, start, end):
    pq = queue.PriorityQueue()
    visited = {}
    result_row, result_col = end
    start_row, start_col = start
    cost = abs(start_row-result_row) + abs(start_col - result_col)
    pq.put((cost, [(start_row, start_col)]))
    while not pq.empty():
        cur_path = pq.get()[1]
        cur_row, cur_col = cur_path[-1]
        if (cur_row, cur_col) in visited:
            continue
        cur_cost = abs(cur_row - result_row) + \
            abs(cur_col - result_col) + len(cur_path) - 1
        visited[(cur_row, cur_col)] = cur_cost
        if (cur_row, cur_col) == (result_row, result_col):
            return cur_path, len(visited)
        for item in maze.getNeighbors(cur_row, cur_col):
            new_cost = abs(item[0] - result_row) + \
                abs(item[1] - result_col) + len(cur_path) - 1
            if item not in visited:
                pq.put((new_cost, cur_path + [item]))
            else:
                # if a node that’s already in the explored set found, test to see if the new h(n)+g(n) is smaller than the old one.
                if visited[item] > new_cost:
                    visited[item] = new_cost
                    pq.put((new_cost, cur_path + [item]))
    return [], 0


# ====================================== extra credit ===============================================
# astar for extra_credit

def shortest(maze, start, end):
    queue = []
    visited = set()
    queue.append([start])
    while queue:
        cur_path = queue.pop(0)
        cur_row, cur_col = cur_path[-1]
        if (cur_row, cur_col) in visited:
            continue
        visited.add((cur_row, cur_col))
        if (cur_row, cur_col) == end:
            return len(cur_path)
        for item in maze.getNeighbors(cur_row, cur_col):
            if item not in visited:
                queue.append(cur_path + [item])
    return 0


def update_pq(maze, objectives, start):
    ret = queue.PriorityQueue()
    for item in objectives:
        cost = shortest(maze, (start[0], start[1]), (item[0], item[1]))
        ret.put((cost, item))
    return ret


def astar_ec(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    cur_pq = queue.PriorityQueue()
    visited = {}
    num_states_visited = set()
    objectives = maze.getObjectives()
    objectives_pq = update_pq(maze, objectives, maze.getStart())
    cur_cost, cur_goal = objectives_pq.get()
    cur_pq.put((cur_cost, [maze.getStart()]))

    while not cur_pq.empty():
        cur_path = cur_pq.get()[1]
        cur_row, cur_col = cur_path[-1]
        if (cur_row, cur_col) in visited:
            continue
        shortest_path = shortest(
            maze, (cur_row, cur_col), (cur_goal[0], cur_goal[1]))
        cur_cost = shortest_path + len(cur_path) - 1
        visited[(cur_row, cur_col)] = cur_cost
        num_states_visited.add((cur_row, cur_col))
        if (cur_row, cur_col) in objectives:
            objectives.remove((cur_row, cur_col))
            if len(objectives) == 0:
                return cur_path, len(num_states_visited)
            else:
                objectives_pq = update_pq(maze, objectives, (cur_row, cur_col))
                cur_cost, cur_goal = objectives_pq.get()
                cur_pq = queue.PriorityQueue()
                cur_pq.put((cur_cost, cur_path))
                visited.clear()
                continue
        for item in maze.getNeighbors(cur_row, cur_col):
            shortest_path = shortest(
                maze, (item[0], item[1]), (cur_goal[0], cur_goal[1]))
            new_cost = shortest_path + len(cur_path) - 1
            if item not in visited:
                cur_pq.put((new_cost, cur_path + [item]))
            else:
                # if a node that’s already in the explored set found, test to see if the new h(n)+g(n) is smaller than the old one.
                if visited[item] > new_cost:
                    visited[item] = new_cost
                    cur_pq.put((new_cost, cur_path + [item]))
    return [], 0
