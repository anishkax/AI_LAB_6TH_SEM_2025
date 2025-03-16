from pyMaze import maze, COLOR, agent, textLabel
from queue import PriorityQueue

def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)

def aStar(m):
    start = (m.rows, m.cols)
    end = (1, 1)
    g_score = {cell: float('inf') for cell in m.grid}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in m.grid}
    f_score[start] = h(start, end)
    open = PriorityQueue()
    open.put((f_score[start], h(start, end), start))
    came_from = {}
    aPath = {}

    while not open.empty():
        currCell = open.get()[2]
        if currCell == end:
            break
        for direction in 'NESW':
            if m.maze_map[currCell][direction]:
                if direction == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                elif direction == 'S':
                    childCell = (currCell[0] + 1, currCell[1])
                elif direction == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                elif direction == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
               
                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + h(childCell, (1, 1))
               
                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score, h(childCell, (1, 1)), childCell))
                    aPath[childCell] = currCell

    fwdpath = {}
    cell = (1, 1)
    while cell != start:
        fwdpath[aPath[cell]] = cell
        cell = aPath[cell]
    return fwdpath

if __name__ == '__main__':
    m = maze(10, 10)
    m.CreateMaze(saveMaze=True, theme=COLOR.fav)
    path = aStar(m)

    a = agent(m, footprints=True, filled=True, shape='arrow', color=COLOR.red)
    m.tracePath({a: path}, delay=100, kill=True)
    l = textLabel(m, 'A Star Path Length', len(path) + 1)

    m.run()
