#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
import time
#this is commented because i have a problem regarding installing ultralytics
#from ultralytics import YOLO
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16,Int16MultiArray

def checkval(vel,high,low):
    if vel < low:
      vel = low
    elif vel > high:
      vel = high
    else:
      vel = vel
    return vel

def ultracallback(msg):
    #i amassuming the distances are in cm
    robot.setfwd(msg.data[0])
    robot.setright(msg.data[1])
    robot.setleft(msg.data[2])


def yawcallback(msg):
    robot.setyaw(msg.data*3.14/180)

class pid:
    def __init__(self,kp,ki,kd):
        self.kp=kp
        self.ki=ki
        self.kd=kd
        self.prev_error=0
        self.integral=0
    def calc(self,err,dt):
        self.integral+=err*dt
        if dt ==0:
            d=0
        else:
            d=(err-self.prev_error)/dt
            self.prev_error=err
        output=(self.kp)*err+(self.ki)*(self.integral)+(self.kd)*d
        return output
    def reset(self):
        self.integral=0
        self.prev_error=0

        
    
class bot:
    letters=[]
    def __init__(self):
        self.right=0
        self.left=0
        self.fwd=0
        self.yaw=0
        self.image=None
        #the pid values need optimization of course
        self.anglepid=pid(1.0,0,0.2)
        self.movepid=pid(1.0,0,0.2)

    def getyaw(self):
        return self.yaw
    
    def getright(self):
        return self.right
    
    def getleft(self):
        return self.left
    
    def getfwd(self):
        return self.fwd
    
    def setright(self,x):
        self.right=x

    def setfwd(self,x):
        self.fwd=x

    def setleft(self,x):
        self.left=x

    def setyaw(self,x):
        self.yaw=x

    def orient(self,val):
        prevtime=time.time()
        while not rospy.is_shutdown() and abs(self.getyaw() - val) > 0.05:
            timenow=time.time()
            dt=timenow-prevtime
            move=self.anglepid.calc(val-self.getyaw(),dt)
            prevtime=timenow
            cmd=Twist()
            cmd.angular.z=checkval(move,2,-2)
            #warning:ni dont know the maximum values for the robot these are random values
            pub.publish(cmd)
            rate.sleep()
        self.anglepid.reset()

    def movebot(self,val):
        prevtime=time.time()
        while not rospy.is_shutdown() and not 0.98*val<self.getfwd()<0.99*val:
            timenow=time.time()
            dt=timenow-prevtime
            move=self.movepid.calc(val-self.getfwd(),dt)
            prevtime=timenow
            cmd=Twist()
            cmd.linear.x=checkval(move,1,0)
            #warning:ni dont know the maximum values for the robot these are random values
            pub.publish(cmd)
            rate.sleep()
        self.movepid.reset()
    
    def scan(self):
        #put whichever device or way the robot uses to take images in the videocapure()parameter instead of zero
        cap = cv2.VideoCapture(0)
        ret,frame= cap.read()
        if ret==True:
            self.image=frame
        right=False
        left=False
        
        #it should plug the image in both models
        #check the color around the letter based on it add the letter to the list
        #it should  also return a direction
   
   
        if left==True:
            return "left"
        elif right==True:
            return "right"
        else:
            return None

robot=bot()
rospy.init_node("robot")
rate=rospy.Rate(50)
sub1=rospy.Subscriber("/ultrasonics",Int16MultiArray,ultracallback)
sub2=rospy.Subscriber("/yaw",Int16,yawcallback)
pub=rospy.Publisher("/cmd_vel",Twist,queue_size=10)
robot.movebot(robot.getfwd()-10)
#the loop stops at the exit suppousing that the exit is clear and there are no waalls or obstacales in front of it
while not rospy.is_shutdown() and robot.getfwd()<280:
    direction=robot.scan()
    if direction=="left":
        robot.orient(robot.getyaw()+3.14*0.5)
    elif direction=="right":
        robot.orient(robot.getyaw()+3.14*1.5)
    else:
        if robot.getleft()>robot.getright():
            robot.orient(robot.getyaw()+3.14*0.5)
        elif robot.getleft()<robot.getright():
            robot.orient(robot.getyaw()+3.14*0.5)
        else:
            continue
    robot.movebot(robot.getfwd()-10)
    rate.sleep()

for letter in bot.letters:
    rospy.loginfo(letter)



