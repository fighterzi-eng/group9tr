import cv2
import numpy as np
import random
import time
#these variables should change depending on the difficulty and accesability
side =300
rtime=1
n=3
img =cv2.imread("test.jpg")
sized=cv2.resize(img,None,fx=n*side/img.shape[1],fy=n*side/img.shape[0])
class square:
    ids=[]
    squares=[]
    def __init__(self,id,x,y,side,wack=None):
        self.side=side
        self.id=id
        self.x=x
        self.y=y
        square.ids.append(id)
        square.squares.append(self)
        cv2.rectangle(sized,(x,y),(x+side,y+side),(255,0,0))
    @staticmethod
    def find(id):
        for sq in square.squares:
            if sq.id==id:
                return sq
            
    def select(self,image):
        cv2.rectangle(image,(self.x+100,self.y+100),(self.x+200,self.y+200),(255,0,0),-1)

    def mole(self,image):
        cv2.rectangle(image,(self.x,self.y),(self.x+self.side,self.y+self.side),(0,0,255),-1)

    def wackset(self,state):
        self.wack=state
    @staticmethod    
    def move(start,dir):
        sx=int(str(start)[0])
        sy=int(str(start)[1])
        if dir=="up":
            if sy==1:
                return start
            y=sy-1
          
            position=int(str(sx)+str(y))
            
            return position
        elif dir=="down":
            if sy==n:
                return start
            y=sy+1
          
            position=int(str(sx)+str(y))
            
            return position
        elif dir=="left":
            if sx==1:
                return start
            x=sx-1
           
            position=int(str(x)+str(sy))
            
            return position
        elif dir=="right":
            if sx==n:
                return start
            x=sx+1
            
            position=int(str(x)+str(sy))
            
            return position
    @staticmethod
    def wack_reset():
        for sq in square.squares:
            sq.wackset(False)
    def wackstate(self):
        return self.wack








score=0
def grid(side):
    for k in range(0,int(sized.shape[1]/side)):
        for i in range(0,int(sized.shape[0]/side)):
            square(int(str(k+1)+str(i+1)),k*side,i*side,side)

grid(side)

for l in range(0,5):
    frame=np.copy(sized)
    ran=random.choice(square.ids)
    x=square.find(ran)
    x.mole(frame)
    
    dt=0
    start=11
    
    starttime=time.time()
    
    while dt<rtime:
        moleim=np.copy(frame)
        #should change depending on the gesture
        wack=True     
        position=square.move(start,random.choice(["up","down","right","left"]))
        start=position
        
        selected=square.find(position)
        selected.wackset(wack)
        selected.select(moleim)
        cv2.imshow("frame",moleim)
        cv2.waitKey(40)
        dt=time.time()-starttime
        if start==ran and selected.wackstate()==True:
            print("wack")
            #increases score
            score+=10
            break
    square.wack_reset()
        


print(score)
   
    
