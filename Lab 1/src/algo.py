from queue import PriorityQueue
from utils import G, Coord, Dist, Cost
import json
import math

def path_cost(path):
    total_cost = 0
    for i in range(1, len(path)):
        total_cost += Cost[f'{path[i-1]},{path[i]}']
    return total_cost

def get_graph(fp='../data/G.json'):
    f = open(fp)
    return json.load(f)

def path_dist(path):
    total_dist = 0
    for i in range(1, len(path)):
        total_dist += Dist[f'{path[i-1]},{path[i]}']
    return total_dist

def calc_hn(cur_node, target):
    x1, y1 = Coord[cur_node]
    x2, y2 = Coord[target]
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def UCS(graph, source, target):
    visited = set()
    # priority queue of score, path. Lower scores are higher on priority.
    queue = PriorityQueue()
    queue.put((0, [source], 0))
    while not queue.empty():
        # get the highest priority path
        candidate = queue.get()
        cur_node = candidate[1][-1]
        visited.add(cur_node)
        if cur_node == target:
            return candidate
        # add all the edges to the priority queue
        for node in graph[cur_node]:
            if node in visited:
                continue
            # create a new path with the node from the edge
            new_path = list(candidate[1]) + [node]
            # add distance and new path to queue.
            queue.put((candidate[0] + Dist[f'{cur_node},{node}'], 
                       new_path, 
                       candidate[2]+Cost[f'{cur_node},{node}']))
    return None, None, None

def A_star(graph, source, target):
    # tracks the A* score of visited nodes
    visited = {}
    # priority queue of score, path. Lower scores are higher on priority.
    queue = PriorityQueue()
    queue.put((0, [source], 0))
    while not queue.empty():
        # get the highest priority path
        candidate = queue.get()
        cur_node = candidate[1][-1]
        
        visited[cur_node] = candidate[0]
        if cur_node == target:
            return candidate
        # add all the edges to the priority queue
        for node in graph[cur_node]:
            # if node has been visited, only skip if its recorded A* score is <= current calculated score
            if node in visited and visited[node] <= candidate[0]+Dist[f'{cur_node},{node}']+calc_hn(node, target):
                continue
            # create a new path with the node from the edge
            new_path = list(candidate[1]) + [node]
            # add distance and new path to queue
            queue.put((candidate[0] + Dist[f'{cur_node},{node}'] + calc_hn(node,target), 
                       new_path, 
                       candidate[2]+Cost[f'{cur_node},{node}']))
    return None, None, None

def yens_ksp(graph, func, source, target, budget, K=5, A=None, terminate=False):
    if not A:
        A = [func(graph, source, target)[1]]
    B = PriorityQueue() #Queue of candidate paths

    for k in range(1, K):
        for i in range(len(A[k-1]) - 1):
            G = get_graph() #New graph for each iteration
            spur_node = A[k-1][i]
            root_path = A[k-1][:i]
            for path in A:
                if len(path) - 1 > i and root_path == path[:i]:
                    # remove edge connecting root path to spur node from Graph, if edge isn't
                    # already deleted
                    if path[i+1] in G[path[i]]:
                        G[path[i]].remove(path[i+1])
            _, spur_path, _ = func(G, spur_node, target)
            # if there exists a path from spur node to target
            if spur_path:
                found_in_B = False
                for paths in B.queue:
                    # if path exists then dont add total_path info in.
                    if paths[1]==spur_path:
                        found_in_B = True
                        break
                # path is new to B, add it in
                if not found_in_B:
                    total_path = root_path + spur_path
                    B.put((path_dist(total_path), total_path, path_cost(total_path)))
        # since B is already sorted, we first try to find whether shortest paths in B
        # satisfy our budget constraint. If not, find the shortest path and add to A.
        if terminate:
            return A[0], None, None
        while B:
            dist, path, cost = B.get()
            # this is a k-th version of shortest path
            if path not in A:
                if cost <= budget:
                    return path, dist, cost
                A.append(path)
    return A, None, None