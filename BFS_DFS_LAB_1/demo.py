from pyMaze import maze, COLOR, agent
m = maze(10,10)
m.CreateMaze(saveMaze = False, theme=COLOR.fav)
 
a=agent(m, footprints=True, filled=True, shape ='arrow', color = COLOR.red)

m.enableArrowKey(a)
m.enableWASD(a)

# m.tracePath({a:m.path},delay = 100, kill=True)

m.run() 