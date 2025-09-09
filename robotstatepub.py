#!/usr/bin/env python
import rospy
#you cant publish to /tf normally you need to use a function from Transformbroadcaster from this library
import tf
import numpy as np
#to read the msgs from /joint_state
from sensor_msgs.msg import JointState
#this library has a useful function for transforming rotation matrices to quatrenions
import tf.transformations as tr


#dont forget to add rospy.spin() in the end of the code

#rotation matrix functions
def rot_y(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c,0,s,0],
                     [0,1,0,0],
                     [-s,0,c,0],
                     [0,0,0,1]])

def rot_z(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c,-s,0,0],
                     [s,c,0,0],
                     [0,0,1,0],
                     [0,0,0,1]])
#translation matrix
def transl(x,y,z):
    return np.array([[1,0,0,x],
                     [0,1,0,y],
                     [0,0,1,z],
                     [0,0,0,1]])


names=[]
positions=[]




def callback(jobstate):
     for i in range(0,len(jobstate.name)):
          names[i]=jobstate.name[i]
          positions[i]=jobstate.position[i]
          
    
 

rospy.init_node("robotstate")
sub=rospy.Subscriber("/joint_states",JointState,callback)
broad=tf.TransformBroadcaster()
#maps every joint name to its position which eases dealing with the without confusing them
my_dict = dict(zip(names, positions))
#creates rotation matrices 
#i still dont know wether to multiply it by the rotation matrix of the original oriantation of the urdf file or not
# the @ is the multiplication of the parent with child matrices parent@child
my_dict["front_left_wheel"]=rot_y(my_dict["front_left_wheel"])
my_dict["rear_left_wheel"]=rot_y(my_dict["front_left_wheel"])
my_dict["front_right_wheel"]=rot_y(my_dict["front_left_wheel"])
my_dict["rear_right_wheel"]=rot_y(my_dict["front_left_wheel"])
my_dict["armbase_to_link1"]=rot_z(my_dict["armbase_to_link1"])
my_dict["link12"]=my_dict["armbase_to_link1"]@rot_y(my_dict["link12"])



T_base_front_left = transl(0.15, 0.15, -0.05)
T_base_front_right = transl(0.15, -0.15, -0.05)
T_base_rear_left = transl(-0.15, 0.15, -0.05)
T_base_rear_right = transl(-0.15, -0.15, -0.05)

T_armbase_link1 = transl(0, 0, 0.1)
T_link1_link2 = transl(0, 0, 0.5)  
T_base_armbase= transl(0,0,0.5)
T_link1_link2=T_base_armbase@T_armbase_link1@T_link1_link2
T_armbase_link1=T_base_armbase@T_armbase_link1


for key,val in my_dict.items():
    q = tr.quaternion_from_matrix(my_dict[key])
    my_dict[key]=q

broad.sendTransform(T_base_front_left, my_dict["front_left_wheel"], rospy.Time.now(), "front_left_wheel", "base_link")
broad.sendTransform(T_base_front_right, my_dict["front_right_wheel"], rospy.Time.now(), "front_right_wheel", "base_link")
broad.sendTransform(T_base_rear_left, my_dict["rear_left_wheel"], rospy.Time.now(), "rear_left_wheel", "base_link")
broad.sendTransform(T_base_rear_right, my_dict["rear_right_wheel"], rospy.Time.now(), "rear_right_wheel", "base_link")
broad.sendTransform(T_armbase_link1, [0,0,0,0], rospy.Time.now(), "armbase", "base_link")
broad.sendTransform(T_armbase_link1, my_dict["armbase_to_link1"], rospy.Time.now(), "link1", "armbase")
broad.sendTransform(T_link1_link2, my_dict["link12"], rospy.Time.now(), "link2", "link1")

rospy.spin()