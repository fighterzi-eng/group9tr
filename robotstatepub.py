#!/usr/bin/env python3
import rospy
#you cant publish to /tf normally you need to use a function from Transformbroadcaster from this library
import tf
import numpy as np
#to read the msgs from /joint_state
from sensor_msgs.msg import JointState
#this library has a useful function for transforming homogenous transformation matrices to quatrenions
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






def callback(jobstate):
    my_dict = dict(zip(jobstate.name, jobstate.position))
    T_base_front_left  = transl( 0.15,  0.15, -0.05) @ rot_y(my_dict["front_left_wheel_joint"])
    T_base_front_right = transl( 0.15, -0.15, -0.05) @ rot_y(my_dict["front_right_wheel_joint"])
    T_base_rear_left   = transl(-0.15,  0.15, -0.05) @ rot_y(my_dict["rear_left_wheel_joint"])
    T_base_rear_right  = transl(-0.15, -0.15, -0.05) @ rot_y(my_dict["rear_right_wheel_joint"])
    T_base_armbase= transl(0,0,0.5)
    T_armbase_link1 = transl(0, 0, 0.1)@ rot_z(my_dict["armbase_to_link1"])
    T_link1_link2 = transl(0, 0, 0.5)@rot_y(my_dict["link1_to_link2"])  
    T_link1_link2=T_base_armbase@T_armbase_link1@T_link1_link2
    T_armbase_link1=T_base_armbase@T_armbase_link1





    broad.sendTransform(T_base_front_left[:3, 3] , tr.quaternion_from_matrix(T_base_front_left), rospy.Time.now(), "front_left_wheel", "base_link")
    broad.sendTransform(T_base_front_right[:3, 3] , tr.quaternion_from_matrix(T_base_front_right), rospy.Time.now(), "front_right_wheel", "base_link")
    broad.sendTransform(T_base_rear_left[:3, 3] , tr.quaternion_from_matrix(T_base_rear_left), rospy.Time.now(), "rear_left_wheel", "base_link")
    broad.sendTransform(T_base_rear_right[:3, 3] , tr.quaternion_from_matrix(T_base_rear_right), rospy.Time.now(), "rear_right_wheel", "base_link")
    broad.sendTransform(T_base_armbase[:3, 3] , [0,0,0,1], rospy.Time.now(), "armbase", "base_link")
    broad.sendTransform(T_armbase_link1[:3, 3] , tr.quaternion_from_matrix(T_armbase_link1), rospy.Time.now(), "link1", "armbase")
    broad.sendTransform(T_link1_link2[:3, 3] , tr.quaternion_from_matrix(T_link1_link2) ,rospy.Time.now(), "link2", "link1")

          
    
 

rospy.init_node("robotstate")
sub=rospy.Subscriber("/joint_states",JointState,callback)
broad=tf.TransformBroadcaster()

rospy.spin()