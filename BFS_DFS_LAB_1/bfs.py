from pyMaze import maze, COLOR, agent

def BFS(m):
    start = (m.rows, m.cols)
    explored = [start]
    frontier = [start]
    bfsPath = {}

    while len(frontier) > 0:
        currCell = frontier.pop(0)
        if currCell == (1, 1):
            break
        for direction in m.maze_map[currCell]:
            if m.maze_map[currCell][direction] == 1:
                if direction == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                elif direction == 'S':
                    childCell = (currCell[0] + 1, currCell[1])
                elif direction == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                elif direction == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                if childCell not in explored:
                    frontier.append(childCell)
                    explored.append(childCell)
                    bfsPath[childCell] = currCell

    fwdPath = {}
    cell = (1, 1)
    while cell != start:
        if cell not in bfsPath:
            break
        fwdPath[bfsPath[cell]] = cell
        cell = bfsPath[cell]
    return fwdPath

m = maze(10, 10)
m.CreateMaze(saveMaze=False, theme=COLOR.fav)

path = BFS(m)

a = agent(m, footprints=True, filled=True, shape='arrow', color=COLOR.red)
m.tracePath({a: path}, delay=100)

print(m.maze_map)

m.enableArrowKey(a)
m.enableWASD(a)

m.run()
