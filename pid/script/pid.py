#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist,PoseStamped,Pose
import time
import math
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry

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

        
def checkval(vel,high,low):
    if vel < low:
      vel = low
    elif vel > high:
      vel = high
    else:
      vel = vel
    return vel


def goalcallback(msg):
   global goalx
   global goaly
   global goalangle
   goalx=msg.pose.position.x
   goaly=msg.pose.position.y
   orientation=msg.pose.orientation 
   _,_,yaw=euler_from_quaternion([orientation.x,orientation.y,orientation.z,orientation.w])
   goalangle=yaw


def currentcallback(msg):
   global currentx,currenty,currentangle
   currentx=msg.pose.pose.position.x
   currenty=msg.pose.pose.position.y
   orientation=msg.pose.pose.orientation 
   _,_,yaw=euler_from_quaternion([orientation.x,orientation.y,orientation.z,orientation.w])
   currentangle=yaw

   




rospy.init_node("pid")
goalx=0
goaly=0
goalangle=0
currentx=0
currenty=0
currentangle=0
sub=rospy.Subscriber("/move_base_simple/goal",PoseStamped,goalcallback)
sub2=rospy.Subscriber("/odom",Odometry,currentcallback)
pub=rospy.Publisher("/cmd_vel",Twist,queue_size=10)
pidx=pid(2,0,0.15)
pidy=pid(2,0,0.15)
pidangle=pid(4,0,0.3)


rate = rospy.Rate(10)
last_time=time.time()
while not rospy.is_shutdown():
    if goalx==0 and goaly==00:
          rate.sleep()
          continue
    dt = time.time()-last_time
    last_time = time.time()
    dx = goalx -currentx
    dy = goaly-currenty
    angle_error = goalangle -currentangle
    # Normalize angle [-pi, pi]
    angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))
    y=pidy.calc(dy,dt)
    x=pidx.calc(dx,dt)
    angle=pidangle.calc(angle_error,dt)

          
    linear_cmd =math.sqrt(x**2+y**2)
    angular_cmd =angle

           
    if dx < 0.01 and dy <0.01 and angle <0.1:
        linear_cmd = 0.0
        angular_cmd = 0.0


           
    cmd = Twist()
    cmd.linear.x = checkval(linear_cmd,0.4,-0.4)
    cmd.angular.z = checkval(angular_cmd,1.82,-1.82)
    pub.publish(cmd)

    rate.sleep()
