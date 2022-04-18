import os #Imports os, must be imported before pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #Hides the pygame start message
import pygame       #imports the pygame library
import math         #imports the math library
import sys          #imports sys library

pygame.init() #starts pygame
pygame.display.set_caption("Raycaster") #names the window
clock=pygame.time.Clock()

width=1024 #Sets the screen width
height=512 #Sets the screen height

pi=float(3.1415926535) #pi
p2=float(pi/2)
p3=float(3*pi/2)
dr=float(0.0174533) #one degree in radians

mapX=int(8) #map x position
mapY=int(8) #map y position
mapS=int(64) #size of cubes on map

map=[ #A 0 is empty space, 1 is a red wall, 2 is a green wall, 3 is a blue wall
    1,1,1,1,1,1,1,1,
    1,0,0,0,0,0,0,1,
    1,0,0,2,0,0,0,1,
    1,0,0,0,0,0,0,1,
    1,0,0,0,0,0,0,1,
    1,0,0,3,0,0,0,1,
    1,0,0,0,0,0,0,1,
    1,1,1,1,1,1,1,1
    ]

screen = pygame.display.set_mode((width,height)) #sets screen size

def draw2D():
    y=-1 #ensures y will equal zero when the loop starts to mimic loops in c
    while y<mapY-1:
        y+=1
        x=-1 #ensures x will equal zero when the loop starts to mimic loops in c
        while x<mapX-1:
            x+=1
            if(map[(y*mapX+x)]>0): color3f=(255,255,255) 
            else: color3f=(0,0,0)
            xo=x*mapS
            yo=y*mapS
            pygame.draw.polygon(surface=screen,color=color3f,points=[ #draws the 4 points of the polygon
                [xo+1,yo+1],
                [xo+1,yo+mapS-1],
                [xo+mapS-1,yo+mapS-1],
                [xo+mapS-1,yo+1]]
                ,width=0)

def dist(ax,ay,bx,by,ang):
    return math.sqrt((bx-ax)*(bx-ax)+(by-ay)*(by-ay))
    
def drawRays():
    global r, mx, my, mp, dof #integers
    global rx, ry, ra, xo, yo #floats
    global pa, mapX, mapY

    ra=pa-(dr*30)
    if(ra<0): ra+=2*pi
    if(ra>2*pi): ra-=2*pi

    r=-1
    while r<60:
        r+=1
        
        #Check Horizontal Lines
        dof=0
        disH=float(1000000); hx=px; hy=py
        try: aTan=float(-1/math.tan(float(ra)))
        except: aTan=float("nan")

        if(ra>pi): ry=((int(py)>>6)<<6)-0.0001; rx=(py-ry)*aTan+px; yo=-64; xo=-yo*aTan #looking up
        if(ra<pi): ry=((int(py)>>6)<<6)+64;     rx=(py-ry)*aTan+px; yo= 64; xo=-yo*aTan #looking down
        if(ra==0 or ra==pi): rx=px; ry=py; dof=8 #looking straight left or right
        while(dof<8):
            mx=int(rx)>>6; my=int(ry)>>6; mp=my*mapX+mx
            if (mp>0 and mp<mapX*mapY and map[mp]>0): hx=rx; hy=ry; disH=dist(px,py,hx,hy,ra); mh=map[mp]; dof=8 
            else: rx+=xo; ry+=yo; dof+=1

        #Check Vertical Lines
        dof=0
        disV=float(1000000); vx=px; vy=py
        nTan=float(-math.tan(float(ra)))
        if(ra>p2 and ra<p3): rx=((int(px)>>6)<<6)-0.0001; ry=(px-rx)*nTan+py; xo=-64; yo=-xo*nTan #looking left
        if(ra<p2 or  ra>p3): rx=((int(px)>>6)<<6)+64;     ry=(px-rx)*nTan+py; xo= 64; yo=-xo*nTan #looking right
        if(ra==0 or  ra==pi):rx=px; ry=py; dof=8 #looking straight up or down
        while(dof<8):
            mx=int(rx)>>6; my=int(ry)>>6; mp=my*mapX+mx
            if (mp>0 and mp<mapX*mapY and map[mp]>0): vx=rx; vy=ry; disV=dist(px,py,vx,vy,ra); mv=map[mp]; dof=8
            else: rx+=xo; ry+=yo; dof+=1

        wc=[[(229.5,0,0),(178.5,0,0)],[(0,229.5,0),(0,178.5,0)],[(0,0,229.5),(0,0,178.5)]]
        if(disV<disH): rx=vx; ry=vy; disT=disV; color3f=wc[mv-1][0]  #vertical wall hit
        if(disH<disV): rx=hx; ry=hy; disT=disH; color3f=wc[mh-1][1]  #horizontal wall hit
        pygame.draw.line(surface=screen,color=(color3f),width=1,start_pos=(px,py),end_pos=(rx,ry)) #draws ray from player
        
        #Draw 3D Walls
        ca=pa-ra
        if(ra<0): ra+=2*pi
        if ra>2*pi: ra-=2*pi
        disT=disT*math.cos(ca) #counter fisheye

        lineH=float((mapS*320)/disT) #line height
        if(lineH>320): lineH=320

        lineO=float(160-lineH/2)     #line offset
        pygame.draw.line(surface=screen,color=(color3f),width=8,start_pos=(r*8+530,lineO),end_pos=(r*8+530,lineH+lineO)) #renders a wall

        ra+=dr
        if(ra<0): ra+=2*pi
        if(ra>2*pi): ra-=2*pi
        

def buttons(): #checks what keys are currently pressed, and moves player
    global px, py, pa, pdx, pdy
    for event in pygame.event.get(): #ensures player can always close pygame
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed() #grabs list of pressed keys
    if keys[pygame.K_a]:
        pa-=0.1
        if pa<0: pa+=pi*2
        pdx=(math.cos(pa)*5)
        pdy=(math.sin(pa)*5)

    if keys[pygame.K_d]:
        pa+=0.1
        if pa>2*pi:
            pa-=2*pi
        pdx=(math.cos(pa)*5)
        pdy=(math.sin(pa)*5)

    if keys[pygame.K_w]: px+=pdx; py+=pdy

    if keys[pygame.K_s]: px-=pdx; py-=pdy


def drawPlayer(): #draws the player on screen
    global width,height
    global screen
    global px, py, pdx, pdy, pa
    pls=4 #player size
    pygame.draw.polygon(surface=screen,color=(255,255,0),points=[[px-pls,py-pls],[px-pls,py+pls],[px+pls,py+pls],[px+pls,py-pls]],width=0) #draws player
    pygame.draw.line(surface=screen,color=(255,255,0),width=3,start_pos=(px,py),end_pos=(px+pdx*5,py+pdy*5)) #draws player direction

def initG(): #inits values
    global px, py, pdx, pdy, pa
    screen.fill((76.5,76.5,76.5))
    pa=0
    px=300
    py=300
    pdx=(math.cos(pa)*5)
    pdy=(math.sin(pa)*5)

initG()
while True: #main loop
    screen.fill((76.5,76.5,76.5))
    buttons()
    draw2D()
    drawRays()
    drawPlayer()
    clock.tick(30) #limit excecution speed
    pygame.display.update() #Updates the screen