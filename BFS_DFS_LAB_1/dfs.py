from pyMaze import maze, COLOR, agent

def DFS(m):
    start = (m.rows, m.cols)
    explored = [start]
    frontier = [start]
    dfsPath = {}

    while frontier:
        currCell = frontier.pop()
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
                    explored.append(childCell)
                    frontier.append(childCell)
                    dfsPath[childCell] = currCell

    if (1, 1) not in dfsPath:
        return {}

    fwdPath = {}
    cell = (1, 1)
    while cell != start:
        fwdPath[dfsPath[cell]] = cell
        cell = dfsPath[cell]
    return fwdPath



m = maze(10,10)
m.CreateMaze(saveMaze = False, theme=COLOR.fav)
 
path = DFS(m)

a=agent(m, footprints=True, filled=True, shape ='arrow', color = COLOR.red)
m.tracePath({a: path}, delay=100)

print(m.maze_map)

m.enableArrowKey(a)
m.enableWASD(a)

m.run() 