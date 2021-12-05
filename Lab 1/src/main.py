import algo
from utils import G, Coord, Dist, Cost, MAX_BUDGET
from algo import UCS, yens_ksp, A_star
if __name__ == "__main__":
    print("Task 1 (UCS):")
    _, path1, _   = UCS(G, '1', '50')
    print('Shortest path:', '->'.join(node for node in path1) + '.')
    print(f'Shortest distance: {algo.path_dist(path1)}.')
    print(f'Total energy cost: N/A.')

    print("\nTask 2 (Using Yen's algorithm with UCS, takes ~3minutes):")
    path2, _, _ = yens_ksp(G, UCS, '1', '50', MAX_BUDGET)
    print('Shortest path:', '->'.join(node for node in path2) + '.')
    print(f'Shortest distance: {algo.path_dist(path2)}.')
    print(f'Total energy cost: {algo.path_cost(path2)}')

    print("\nTask 3 (Using Yen's algorithm with UCS, takes ~7minutes):")
    print("We terminate the search early as the algorithm had been run for several hours and yielded no results. We elaborate further on this behaviour in our report.")
    path3, _, _ = yens_ksp(G, A_star, '1', '50', MAX_BUDGET, terminate=True)
    print('Shortest path:', '->'.join(node for node in path2) + '.')
    print(f'Shortest distance: {algo.path_dist(path3)}.')
    print(f'Total energy cost: {algo.path_cost(path3)}')