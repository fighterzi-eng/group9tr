#!/usr/bin/env python3
import rospy
from res_pkg_test2.srv import start , startRequest,startResponse
from res_pkg_test2.srv import order ,orderRequest,orderResponse
customers=[]

def starthand(req):
    if len(customers)>3:

         l=startResponse()
         l.state=False
         l.message="sorry ,all workers are busy please try again later"
         return l
    else:

        customers.append(req.usrname)
        l=startResponse()
        l.state=True
        l.message="hell0"+req.usrname+"how can i help u"
        return l

def startsrv():
    rospy.init_node("reception")
    s=rospy.service("reception",start,starthand)
    rospy.loginfo("can i have ur name")
    #rospy.spin()


def ordhand(req,name):
    for l in req.ordering:
        #searchforfood(l[0:3]) returnss object
        #sets the size and topping
        #calculates the cost and time
        #ads them to the final cost and time

    #checks for deliverystate if true increase price and assign delivery time to a value
    #returns the final total price,time and the full order with the name
    #removes the user name from the list
    


