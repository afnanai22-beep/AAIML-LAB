from collections import deque

EMPTY, DIRTY, OBSTACLE = 0, 1, -1
DIRS = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}

class Grid:
    def __init__(self, w, h, obs, dirt):
        self.w, self.h = w, h
        self.g = [[EMPTY]*w for _ in range(h)]
        for x, y in obs: self.g[y][x] = OBSTACLE
        for x, y in dirt: self.g[y][x] = DIRTY

    def display(self, pos):
        for y in range(self.h):
            print(" ".join("A" if (x,y)==pos else "X" if self.g[y][x]==OBSTACLE else "D" if self.g[y][x]==DIRTY else "." for x in range(self.w)))
        print()

    def dirt_left(self): return [(x,y) for y in range(self.h) for x in range(self.w) if self.g[y][x]==DIRTY]

class Agent:
    def __init__(self, env, x, y): self.env, self.x, self.y = env, x, y

    def bfs(self):
        start = (self.x,self.y)
        q, seen = deque([(start,[])]), {start}
        while q:
            (cx,cy), path = q.popleft()
            if self.env.g[cy][cx]==DIRTY and (cx,cy)!=start: return path
            for d,(dx,dy) in DIRS.items():
                nx,ny=cx+dx,cy+dy
                if 0<=nx<self.env.w and 0<=ny<self.env.h and self.env.g[ny][nx]!=OBSTACLE and (nx,ny) not in seen:
                    seen.add((nx,ny)); q.append(((nx,ny), path+[d]))

    def act(self):
        if self.env.g[self.y][self.x]==DIRTY: self.env.g[self.y][self.x]=EMPTY; print(f"Cleaned {self.x},{self.y}"); return
        path=self.bfs()
        if path: d=path[0]; dx,dy=DIRS[d]; self.x+=dx; self.y+=dy; print(f"Move {d} to {self.x},{self.y}")
        else: print("No dirt left.")

def main():
    env=Grid(6,6,[(1,1),(2,2),(3,1),(4,4)],[(0,0),(5,5),(2,4),(3,3)])
    agent=Agent(env,0,5)
    for _ in range(50):
        env.display((agent.x,agent.y)); agent.act()
        if not env.dirt_left(): print("All clean!"); break

if __name__=="__main__": main()
