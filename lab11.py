import os
import time
from collections import deque

EMPTY, DIRTY, OBSTACLE = 0, 1, -1
DIRS = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}

class Grid:
    def __init__(self, w, h, obs, dirt):
        self.w, self.h = w, h
        self.g = [[EMPTY]*w for _ in range(h)]
        for x,y in obs: self.g[y][x]=OBSTACLE
        for x,y in dirt: self.g[y][x]=DIRTY

    def display(self, pos):
        os.system('cls' if os.name == 'nt' else 'clear')
        for y in range(self.h):
            row = ""
            for x in range(self.w):
                if (x,y)==pos: row += "A "
                elif self.g[y][x]==OBSTACLE: row += "X "
                elif self.g[y][x]==DIRTY: row += "D "
                else: row += ". "
            print(row)
        print()

    def dirt_left(self):
        return any(DIRTY in row for row in self.g)

class Agent:
    def __init__(self, env,x,y): self.env,self.x,self.y=env,x,y

    def bfs(self):
        start=(self.x,self.y)
        q,seen=deque([(start,[])]),{start}
        while q:
            (cx,cy),path=q.popleft()
            if self.env.g[cy][cx]==DIRTY and (cx,cy)!=start: return path
            for d,(dx,dy) in DIRS.items():
                nx,ny=cx+dx,cy+dy
                if 0<=nx<self.env.w and 0<=ny<self.env.h and self.env.g[ny][nx]!=OBSTACLE and (nx,ny) not in seen:
                    seen.add((nx,ny))
                    q.append(((nx,ny),path+[d]))

    def step(self):
        if self.env.g[self.y][self.x]==DIRTY:
            self.env.g[self.y][self.x]=EMPTY
        else:
            path=self.bfs()
            if path:
                d=path[0]
                dx,dy=DIRS[d]
                self.x+=dx;self.y+=dy

def main():
    env=Grid(6,6,[(1,1),(2,2),(3,1),(4,4)],[(0,0),(5,5),(2,4),(3,3)])
    agent=Agent(env,0,5)

    while True:
        env.display((agent.x,agent.y))
        agent.step()
        time.sleep(0.8)  # Slower delay for animation
        if not env.dirt_left():
            env.display((agent.x,agent.y))
            print("✅ All dirt cleaned!")
            break

if __name__=="__main__": main()
