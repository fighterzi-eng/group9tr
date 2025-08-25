#!/usr/bin/env python3
import rospy
from res_pkg_test2.msg import timeAction,timeActionGoal,timeActionResult,timeActionFeedback
import actionlib
from customers import customers
#this action is supposed to take the total time from the customer as a goal

def ordertrk(goal):
    feedback=timeActionFeedback
    result=timeActionResult
    start=0
    while start<goal:
        l=goal-start
        if l>50:
            feedback.state="we have just begun ,please be patient"
        elif l<30:
            feedback.state="we are in the middle of the preperation process,it should be ready soon"
        elif l<10:
            feedback.state="it will be ready in 10 minutes"
        actionlib.server.publish_feedback(feedback)
        start+=10
    result.success=True
    result.message="thank you for visiting us ,please enjoy your meal"
    actionlib.set_succeeded(result)
def feedbck(name):
    rospy.init_node("ordertrack")
    server=actionlib.SimpleActionServer(name,timeAction,ordertrk,False)
    server.start()

if __name__=="__main__":
     for name in customers:
         feedbck(name)
         customers.remove(name)

     rospy.spin()





