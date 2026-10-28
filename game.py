import pygame
from pygame.locals import *
import sys
import os
from random import shuffle
import random
from sqlite3 import *
# from appJar import gui 
from SQL import * 
from interface import *
from appjarGui import app 


##########################
########## GAME ##########
##########################


def startGame(cols=13,rows=13,difficulty="Hard"): 
    global cop_path, cop_step

    cop_path=[]
    cop_step=0

    # Setting tile size, height and width of maze
    RES=WIDTH,HEIGHT=800,800
    TILE=55

    #character size 
    #48 
    sprite_size_x=48
    sprite_size_y=48

    # Creating the display
    pygame.init()
    sc =pygame.display.set_mode(RES)
    pygame.display.set_caption("Cops N Robbers")
    clock= pygame.time.Clock()
    surface=pygame.display.get_surface()
    start_ticks=pygame.time.get_ticks() 

    ##########################
    ####### Kruskal's ########    
    ########################## 

    #defining a single cell
    class Cell:

        def __init__(self,x,y):
            self.x=x
            self.y= y
            self.walls ={'top': True, 'right': True, 'bottom': True, 'left': True} 
            self.visited= False
            self.neighbours=[]

        def draw(self,offset_x,offset_y):
            #drawing the maze at the offsets
            x =self.x*TILE+offset_x
            y =self.y*TILE+offset_y

            #drawing all edges of the cell
            if self.visited:
                pygame.draw.rect(sc,pygame.Color('#1e1e1e'),(x,y,TILE,TILE))

            if self.walls['top']:
                pygame.draw.line(sc,pygame.Color('#1e4f5b'),(x,y),(x+TILE,y),3)

            if self.walls['right']:
                pygame.draw.line(sc,pygame.Color('#1e4f5b'),(x+TILE,y),(x+TILE,y+TILE),3)

            if self.walls['bottom']:
                pygame.draw.line(sc, pygame.Color('#1e4f5b'),(x +TILE,y + TILE),(x,y+TILE),3)

            if self.walls['left']:
                pygame.draw.line(sc,pygame.Color('#1e4f5b'),(x, y+ TILE),(x,y),3)


    #union-find (disjoint set) implementation
    class UnionFind:

        def __init__(self,n):
            self.parent=list(range(n))

        def find(self,u):

            if self.parent[u] !=u:
                self.parent[u]=self.find(self.parent[u])

            return self.parent[u]

        def union(self,u,v):
            root_u =self.find(u)
            root_v =self.find(v)

            if root_u !=root_v:
                self.parent[root_v]=root_u

                return True
            
            return False

    #create cells
    grid_cells=[]

    for row in range(rows):
        #create a cell object for each cell in the grid
        for col in range(cols):
            #create a cell object for each cell in the grid
            grid_cells.append(Cell(col,row))

    # Create walls by leaving the outermost walls intact
    for col in range(cols):
        grid_cells[col].walls['top'] =True  # Top row walls
        grid_cells[(rows -1)*cols +col].walls['bottom']=True  # Bottom row walls

    for row in range(rows):
        grid_cells[row *cols].walls['left']=True  # Left column walls
        grid_cells[row *cols+(cols -1)].walls['right']=True  # Right column walls

    #create edges
    edges = []

    for col in range(cols):

        for row in range(rows):
            index=col+row* cols

            if col<cols -1:  #right
                edges.append((index,index+1)) 

            if row<rows -1:  #down
                edges.append((index,index+cols)) 

    #shuffle edges to randomize
    shuffle(edges)

    removed_walls=[]

    uf=UnionFind(len(grid_cells))

    #generate maze using kruskal's algorithm
    for u,v in edges:

        if uf.union(u,v):
            #remove the wall between cells
            current_cell= grid_cells[u]
            next_cell =grid_cells[v]

            if current_cell.x==next_cell.x: 

                if current_cell.y < next_cell.y:
                    current_cell.walls['bottom']=False
                    next_cell.walls['top']=False

                else:
                    current_cell.walls['top']=False
                    next_cell.walls['bottom']=False

            else: 

                if current_cell.x < next_cell.x:
                    current_cell.walls['right']=False
                    next_cell.walls['left']=False

                else:
                    current_cell.walls['left']=False
                    next_cell.walls['right']=False

                removed_walls.append((u,v))

    #adding cycles/extra paths
    if difficulty=="Easy":
        extra_paths=20
    elif difficulty=="Hard":
        extra_paths=50  #number of additional cycles

    #shuffle all edges again
    extra_walls=edges[:] 
    shuffle(extra_walls)

    #extra walls more mutiple paths
    for u, v in extra_walls:

        if extra_paths <= 0:
            break

        if (u,v) not in removed_walls:  #only remove walls that werent removed before
            current_cell=grid_cells[u]
            next_cell=grid_cells[v]

            if current_cell.x==next_cell.x:  #vertical connection
                current_cell.walls['bottom']=False
                next_cell.walls['top']=False

            else:  #horizontal connection
                current_cell.walls['right']=False
                next_cell.walls['left']=False

            extra_paths -=1  #reduce count of extra paths

    #define start and end points
    start_cell=grid_cells[0]  #top left corner
    end_cell=grid_cells[(rows -1)*cols+(cols -1)]  #bottom right corner

    #calculate offsets to center the maze
    maze_width=cols* TILE
    maze_height=rows* TILE
    offset_x=(WIDTH -maze_width)//2
    offset_y=(HEIGHT -maze_height)//2  

    class Player(pygame.sprite.Sprite):
        #spawning player
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.images=[]

            for i in range (1,5):
                img=pygame.image.load(os.path.join("images","robber.png")).convert_alpha()
                img=pygame.transform.scale(img,(sprite_size_x,sprite_size_y))
                self.images.append(img)

            self.image=self.images[0]
            self.rect=self.image.get_rect()

        #update/animating the player
        def update(self):
            self.image=self.images[(pygame.time.get_ticks()//100)%len(self.images)]
                
    player=Player() #spawns player
    playerSpeed=4  
    player.rect.x =offset_x 
    player.rect.y =offset_y 
    player_list=pygame.sprite.Group()
    player_list.add(player)

    class Cop(pygame.sprite.Sprite):
        #spawning Cop
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.imgs=[]

            for i in range(1,5):
                im=pygame.image.load(os.path.join("images","cop.png")).convert_alpha()
                im=pygame.transform.scale(im,(sprite_size_x,sprite_size_y))
                self.imgs.append(im)

            self.image=self.imgs[0]
            self.rect=self.image.get_rect()

            self.visible=True 
            self.cooldown_time=10000
            self.hidden_since=None

        #update/animating the cop
        def update(self):
            if self.visible:
                self.img=self.imgs[(pygame.time.get_ticks()//100)%len(self.imgs)]
            else:
                self.img=pygame.Surface((0,0))

    #creates group to store cops
    cop_list =pygame.sprite.Group()

    if difficulty=="Hard":
        #cop that pathfinds
        cop=Cop() #spawns cop
        cop_x=offset_x  #cops x coordinate
        cop_y=15*50-offset_y  #cops y coordinate    
        cop.rect.x=cop_x #assigning x and y coords to the cop
        cop.rect.y=cop_y 
        cop_list.add(cop)  #adds cop to group

        
        #cops for random movement
        cop2=Cop()
        cop2_x=542
        cop2_y=210
        cop2.rect.x=cop2_x 
        cop2.rect.y=cop2_y 

        #center of maze
        middle=374

        cop3=Cop()
        cop3_x=middle 
        cop3_y=middle 
        cop3.rect.x=cop3_x
        cop3.rect.y=cop3_y 

        #374 706
        cop4=Cop()
        cop4_x=208
        cop4_y=540
        cop4.rect.x=cop4_x
        cop4.rect.y=cop4_y

        #adds cops to group
        cop_list.add(cop2,cop3,cop4)

    #returns neighbouring cells that have no walls between them
    def getNeighbours(cell, grid_cells, cols, rows):

        neighbours = []
        x, y = cell.x, cell.y

        #           Right,  Left,  Up,  Down
        directions=[(-1,0),(1,0),(0,-1),(0,1)]

        for dx,dy in directions:
            nx,ny= x + dx, y + dy
            if 0<=nx<cols and 0<=ny<rows:
                neighbour_cell=grid_cells[ny*cols+nx]
                if not wallBetween(cell, neighbour_cell):
                    neighbours.append(neighbour_cell)

        return neighbours

    def wallBetween(cell1,cell2):

        if cell1.x == cell2.x:  #same column checks vertical walls
            if cell1.y < cell2.y:
                return cell1.walls['bottom'] or cell2.walls['top']
            else:
                return cell1.walls['top'] or cell2.walls['bottom']
            
        elif cell1.y == cell2.y:  #same row checks horizontal walls
            if cell1.x < cell2.x:
                return cell1.walls['right'] or cell2.walls['left']
            else:
                return cell1.walls['left'] or cell2.walls['right']
            
        return False

    ##########################
    ###### A* Algorithm ######
    ########################## 

    #push and pop functions for A* algorithm
    #pushes the item into the queue in order of f-cost
    def pushAStar(queue,item):
        #item = (f_cost, index)
        f, idx = item
        inserted = False
        
        for i in range(len(queue)):
            if f < queue[i][0]:
                queue.insert(i, item)
                inserted = True
                break

        if not inserted:
            queue.append(item)

    #pops the item with the lowest f-cost from the queue
    def popAStar(queue):
        if queue:
            return queue.pop(0)
        return None

    #A* algorithm
    def aStar(start_cell, end_cell, grid_cells, cols, rows):
        start_idx = start_cell.y * cols + start_cell.x
        end_idx = end_cell.y * cols + end_cell.x

        #g-cost h-cost f-cost for each cell
        g_cost = {i: float('inf') for i in range(len(grid_cells))}
        h_cost = {i: float('inf') for i in range(len(grid_cells))}
        f_cost = {i: float('inf') for i in range(len(grid_cells))}
        
        g_cost[start_idx] = 0
        h_cost[start_idx] = mDistance(start_cell, end_cell)
        f_cost[start_idx] = h_cost[start_idx]

        #priority queue to explore the node with the lowest f-cost
        open_list = []
        pushAStar(open_list, (f_cost[start_idx], start_idx))

        #dictionary to store the best path
        came_from = {i: None for i in range(len(grid_cells))}

        while open_list:
            _, current_idx = popAStar(open_list)
            current_cell = grid_cells[current_idx]

            if current_idx == end_idx:
                #goal reached
                break  

            #check the neighbours
            for neighbour in getNeighbours(current_cell, grid_cells, cols, rows):
                neighbour_idx = neighbour.y * cols + neighbour.x
                tentative_g_cost = g_cost[current_idx] + 1  #assuming uniform cost (1)

                if tentative_g_cost < g_cost[neighbour_idx]:
                    came_from[neighbour_idx] = current_idx
                    g_cost[neighbour_idx] = tentative_g_cost
                    h_cost[neighbour_idx] = mDistance(neighbour, end_cell)
                    f_cost[neighbour_idx] = g_cost[neighbour_idx] + h_cost[neighbour_idx]
                    pushAStar(open_list, (f_cost[neighbour_idx], neighbour_idx))

        #reconstruct the path by tracing back from the goal
        path = []
        current_idx = end_idx
         
        while current_idx is not None:
            path.insert(0, grid_cells[current_idx])
            current_idx = came_from[current_idx]

        return path

    #Manhattan Distance Heuristic 
    def mDistance(cell1, cell2):
        return abs(cell1.x - cell2.x) + abs(cell1.y - cell2.y)

    #function to move cop smoothly along its path
    def updateCopPath():
        global cop_step,cop_path

        #get start and player position on grid
        cop_start_index=(cop.rect.y//TILE)* cols +(cop.rect.x//TILE)
        player_index=(player.rect.y//TILE)* cols +(player.rect.x//TILE)

        if 0<= cop_start_index <len(grid_cells) and 0 <=player_index <len(grid_cells):
            cop_start=grid_cells[cop_start_index]
            player_position=grid_cells[player_index]

            #recalc the path if needed
            if not cop_path or cop_path[-1]!=player_position:
                cop_path=aStar(cop_start,player_position,grid_cells,cols,rows)
                cop_step=1

    #cops movement towards the target
    def moveCopSmoothly():
        global cop_step,cop_path

        #ensure theres a valid path and steps to follow
        if cop_path and cop_step <len(cop_path):
            next_cell=cop_path[cop_step]

            target_x=offset_x + next_cell.x *TILE 
            target_y=offset_y + next_cell.y *TILE 

            #calc difference between current position and target position
            diff_x=target_x - cop.rect.x
            diff_y=target_y - cop.rect.y

            move_speed=0.05

            if abs(diff_x) <1 and abs(diff_y) <1:
                cop.rect.x=target_x
                cop.rect.y=target_y
                cop_step +=1

            else:
                next_x=cop.rect.x +diff_x *move_speed 
                next_y=cop.rect.y +diff_y *move_speed 

                if detectCollision(next_x, next_y, is_cop=True):
                    #try moving all directions
                    directions=[
                        (next_x+1,next_y), #right
                        (next_x-1,next_y), #left
                        (next_x,next_y+1), #down
                        (next_x,next_y-1)  #up
                    ]

                    moved=False
                    for direction in directions:
                        new_x,new_y=direction
                        if not detectCollision(new_x,new_y,is_cop=True):
                            cop.rect.x=new_x
                            cop.rect.y=new_y
                            moved=True
                            break

                    if not moved:
                        cop.rect.x=next_x
                        cop.rect.y=next_y
                else:
                    cop.rect.x=next_x
                    cop.rect.y=next_y

            if abs(diff_x) <1 and abs(diff_y) <1:
                cop.rect.x=target_x
                cop.rect.y=target_y
                cop_step +=1

    def moveCopRandomly():
        x=(cop2.rect.x -offset_x)//TILE
        y=(cop2.rect.y -offset_y)//TILE

        current_cell=grid_cells[y*cols+x]

        directions={
            'left':(-1,0),
            'right':(1,0),
            'up':(0,-1),
            'down':(0,1)
        }

        valid_directions=[]

        #check which directions are valid
        for dx,dy in directions.values():
            nx, ny=x+dx,y+dy
            if 0<=nx <cols and 0<=ny<rows:
                neighbour_cell=grid_cells[ny*cols+nx]
                if not wallBetween(current_cell,neighbour_cell):
                    test_rect=cop2.rect.copy()
                    test_rect.x +=dx*TILE
                    test_rect.y +=dy*TILE
                    if not detectCollision(test_rect.x,test_rect.y): #,walls
                        valid_directions.append((dx, dy))

        if valid_directions:
            dx,dy=random.choice(valid_directions)
            cop2.rect.x +=dx*TILE
            cop2.rect.y +=dy*TILE 

    def moveCopRandomly2():
        x=(cop3.rect.x -offset_x)//TILE
        y=(cop3.rect.y -offset_y)//TILE

        current_cell=grid_cells[y*cols+x]

        directions={
            'left':(-1,0),
            'right':(1,0),
            'up':(0,-1),
            'down':(0,1)
        }

        valid_directions=[]

        #check which directions are valid
        for direction,(dx,dy) in directions.items():
            nx, ny=x+dx,y+dy
            if 0<=nx <cols and 0<=ny<rows:
                neighbour_cell=grid_cells[ny*cols+nx]
                if not wallBetween(current_cell,neighbour_cell):
                    test_rect=cop3.rect.copy()
                    test_rect.x +=dx*TILE
                    test_rect.y +=dy*TILE 
                    if not detectCollision(test_rect.x,test_rect.y):
                        valid_directions.append((dx,dy))

        if valid_directions:
            dx,dy=random.choice(valid_directions)
            cop3.rect.x +=dx*TILE
            cop3.rect.y +=dy*TILE 

    def moveCopRandomly3():
        x=(cop4.rect.x -offset_x)//TILE
        y=(cop4.rect.y -offset_y)//TILE

        current_cell=grid_cells[y*cols+x]

        directions={
            'left':(-1,0),
            'right':(1,0),
            'up':(0,-1),
            'down':(0,1)
        }

        valid_directions=[]

        #check which directions are valid
        for direction,(dx,dy) in directions.items():
            nx, ny=x+dx,y+dy
            if 0<=nx <cols and 0<=ny<rows:
                neighbour_cell=grid_cells[ny*cols+nx]
                if not wallBetween(current_cell,neighbour_cell):
                    test_rect=cop4.rect.copy()
                    test_rect.x +=dx*TILE
                    test_rect.y +=dy*TILE 
                    if not detectCollision(test_rect.x,test_rect.y):
                        valid_directions.append((dx,dy))

        if valid_directions:
            dx,dy=random.choice(valid_directions)
            cop4.rect.x +=dx*TILE
            cop4.rect.y +=dy*TILE 

    class Coin(pygame.sprite.Sprite):
        #spawning coin
        def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            #load coin image
            self.image=pygame.image.load(os.path.join("images","coin.png")).convert_alpha()
            self.image=pygame.transform.scale(self.image,(25,25)) #resize Coin
            self.rect=self.image.get_rect()
            self.rect.x=offset_x+x*TILE  #position of coin on screen
            self.rect.y=offset_y+y*TILE

    def generateCoins(num_coins):
        coin_group=pygame.sprite.Group()
        valid_cells=[]

        for cell in grid_cells:
            #skips walls and the start and end cells
            if cell==start_cell or cell==end_cell:
                continue

            if len(getNeighbours(cell,grid_cells,cols,rows))>0:
                valid_cells.append(cell)

        shuffle(valid_cells)

        for i in range(min(num_coins,len(valid_cells))):
            cell=valid_cells[i]
            coin=Coin(cell.x,cell.y)
            coin_group.add(coin)
        
        return coin_group
    
    #generate coins in the maze
    #if difficulty is easy, generate 20 coins
    if difficulty=="Easy": 
        coin_group=generateCoins(20)
    #if the difficulty's hard, genereate 30
    elif difficulty=="Hard":
        coin_group=generateCoins(30)
     
    BUFFERSIZE=1 

    #detect if a player/cop collides with the wall
    def detectCollision(x,y,is_cop=False):
        
        if is_cop and difficulty=="Easy":
            return False  

        if is_cop and difficulty == "Hard":
            if not cop_list:
                return False 
            
            try:
                cop= list(cop_list)[0]  #get the first cop in the group
            except IndexError:
                return False
            bufferRect=pygame.Rect(x-BUFFERSIZE,y-BUFFERSIZE,cop.rect.width+2*BUFFERSIZE,cop.rect.height+2*BUFFERSIZE)
        else:
            bufferRect=pygame.Rect(x,y,player.rect.width,player.rect.height)

        for cell in grid_cells:
            cell_rect = pygame.Rect(offset_x + cell.x * TILE, offset_y + cell.y * TILE, TILE, TILE)

            #check if the player or cops buffer zone is colliding with the walls
            if cell.walls['top'] and bufferRect.colliderect(pygame.Rect(cell_rect.left, cell_rect.top - 2, TILE, 2)):
                return True
            
            if cell.walls['bottom'] and bufferRect.colliderect(pygame.Rect(cell_rect.left, cell_rect.bottom, TILE, 2)):
                return True
            
            if cell.walls['left'] and bufferRect.colliderect(pygame.Rect(cell_rect.left - 2, cell_rect.top, 2, TILE)):
                return True
            
            if cell.walls['right'] and bufferRect.colliderect(pygame.Rect(cell_rect.right, cell_rect.top, 2, TILE)):
                return True
            
        return False

    def playerMovement():
        keys=pygame.key.get_pressed()
        #uses WASD keys to move the player
        if keys[pygame.K_w]:
            #checks for collisions
            if not detectCollision(player.rect.x, player.rect.y -playerSpeed):
                player.rect.y-=playerSpeed
        if keys[pygame.K_a]:
            if not detectCollision(player.rect.x -playerSpeed, player.rect.y):
                player.rect.x-=playerSpeed
        if keys[pygame.K_s]:
            if not detectCollision(player.rect.x, player.rect.y +playerSpeed):
                player.rect.y+=playerSpeed
        if keys[pygame.K_d]:
            if not detectCollision(player.rect.x +playerSpeed, player.rect.y):
                player.rect.x+=playerSpeed

        # coord=f"Player Coordinates: ({player.rect.x},{player.rect.y})"
        # print(coord)

    def scoreDisplay():
        #display the score on the screen
        font=pygame.font.SysFont("Arial",24)
        score_text=font.render(f"Score:{score}",True,pygame.Color("black"))
        sc.blit(score_text,(10,10))

    player_has_moved=False

    def timeBar():
        #allows me to use time_string2 outside the function
        global time_string2 

        
        if not timeBarVisible:
            return 
        #only start the timer if the player has moved
        if not player_has_moved or start_ticks is None :
            ms=0 
        elif timerRunning:
            ms=pygame.time.get_ticks()-start_ticks 
        else:
            ms=end_time-start_ticks

        #seconds, minutes and milliseconds 
        mins=ms//60000
        secs=(ms%60000)//1000
        millisecs=(ms%1000)

        #formatting the time string and displaying it on the screen 
        font=pygame.font.SysFont("Arial",24)
        time_string=f"Time:{mins:02}:{secs:02}.{millisecs:03}"
        time_string2=f"{mins:02}:{secs:02}.{millisecs:03}"
        timer_text=font.render( time_string,True,pygame.Color("black"))
        text_rect=timer_text.get_rect()
        text_rect.topright=(sc.get_width()-10,10)
        sc.blit(timer_text,text_rect)

    #track players score
    score=0 

    #index for cop movement along path
    cop_step = 0  
    #store path
    cop_path=[]

    #flags for timer 
    timerRunning=False  
    start_ticks=None 
    end_time=None
    timeBarVisible=True  

    start_x=offset_x+start_cell.x *TILE +10
    start_y=offset_y+start_cell.y *TILE + 10
    end_x=offset_x+end_cell.x *TILE +10
    end_y=offset_y+end_cell.y *TILE +10

    ##########################
    ####### Main loop ########
    ##########################

    #main loop for the game
    #running variable to keep the game running until the player quits 
    running=True
    while running:
        sc.fill(pygame.Color('#a6d5e2'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False

            #checks for collisions
            collided_coins=pygame.sprite.spritecollide(player,coin_group,True) #True removes the coin
            for coin in collided_coins:
                score+=1

            #stops game when player collides with any cop
            player_rect=pygame.Rect(player.rect.x,player.rect.y,player.rect.width,player.rect.height)
            for Cop in cop_list: 
                if player_rect.colliderect(Cop.rect): 
                    pygame.time.wait(2000)
                    running=False
                    pygame.quit()
                    app.showSubWindow("Game Over")
                    return 

            #defines the end goal
            end_Rect=pygame.Rect(end_x,end_y,TILE,TILE)

            #stops game when player collides with end goal 
            #stores the time taken and score in the corresponding database
            #and shows the game over screen 
            if player.rect.colliderect(end_Rect):
                pygame.time.wait(2000)

                running=False 
                Username=app.getEntry("Username: ")  
                PlayerTime=end_time-start_ticks
                PlayerTime=time_string2 
                Score=score

                #store players info in corresponding table in database 
                #after game has been won
                if difficulty=="Easy":
                    addEasyLB(Username,PlayerTime,Score)
                elif difficulty=="Hard":
                    addHardLB(Username,PlayerTime,Score)

                #after the informations been stored show the game over subwindow
                pygame.quit()
                app.showSubWindow("Game Over ")

                return 
                
            #allows the player to move around the maze 
            playerMovement()

            #checks if the player has moved
            #if player has moved and the player is not at the start position
            #timer starts running 
            if not player_has_moved and (player.rect.x!=offset_x or player.rect.y!=offset_y):
                player_has_moved=True
                start_ticks=pygame.time.get_ticks()
                timerRunning=True 
            
            #if the player collides with the end goal, stop the timer
            #and show the game over screen 
            if player.rect.colliderect(end_Rect):
                if timerRunning:
                    end_time=pygame.time.get_ticks()
                    timerRunning=False

            #when the hard difficulty is selected, the cop functions are called 
            if difficulty=="Hard" and player_has_moved:
                #path finding cop movment functions
                updateCopPath()
                moveCopSmoothly() 
 
                #every 500ms, the random movement cop functions are called
                #to move the cops randomly
                if pygame.time.get_ticks()%500<20:
                    moveCopRandomly()
                    moveCopRandomly2() 
                    moveCopRandomly3()

        #draw the maze with the offsets
        for cell in grid_cells:
            cell.draw(offset_x,offset_y)

        #calculate the start and end points with offsets 
        start_x=offset_x+start_cell.x *TILE +10
        start_y=offset_y+start_cell.y *TILE + 10
        end_x=offset_x+end_cell.x *TILE +10
        end_y=offset_y+end_cell.y *TILE +10

        #draw start and end points with offsets
        pygame.draw.rect(sc,pygame.Color('green'),(start_x,start_y,TILE -20,TILE -20))  # Start point
        pygame.draw.rect(sc,pygame.Color('red'),(end_x,end_y,TILE -20,TILE -20))  # End point
        
        #draws the player, coins and cops 
        coin_group.update()
        coin_group.draw(sc)
        cop_list.update()
        cop_list.draw(sc)
        player_list.update()
        player_list.draw(sc)

        #calls the functions to display the timer and score 
        timeBar()
        scoreDisplay()

        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit() 