import cv2
import numpy as np
import random
side =300
n=3
img =cv2.imread("test.jpg")
sized=cv2.resize(img,None,fx=n*side/img.shape[1],fy=n*side/img.shape[0])
print(sized.shape)
class square:
    ids=[]
    squares=[]
    def __init__(self,id,x,y,side):
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



def grid(side):
    for k in range(0,int(sized.shape[1]/side)):
        for i in range(0,int(sized.shape[0]/side)):
            square(int(str(k)+str(i)),k*side,i*side,side)

grid(side)

for l in range(0,30):
    frame=np.copy(sized)
    x=square.find(random.choice(square.ids))
    
    x.mole(frame)
   
    cv2.imshow("frame",frame)
    cv2.waitKey(1000)
