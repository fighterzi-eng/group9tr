#!/usr/bin/env python3
import rospy
from scripts.feeder import *
from res_pkg_test2.srv import start ,startResponse
from res_pkg_test2.srv import order ,orderResponse
customers=[]
#i had an idea to deal with multiple customer the base of the idea is that ros uses the service or server name to connect
#to it so it going to be changed for each customer it going to be the customer s name
#but this idea will require both service to be running in paralell
#i removed the idea of creating a restaurant class because after some thought it felt pointless
#i mean why should we create a class for one or no objects , that is going to overcompicate the code needlesly
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
    #its commented bec idont know wether to use it or not
    #rospy.spin()

#the restaurant is going to recieve a listof strings
#each string is going to contain 5 letters the first 3 are the objects name first 3 letter,4th is the size(s,m,l)
#and the last one is going to be a number that is used to referto the topping 
def ordhand(req,name):
    cost=0
    tm=0
    order=""
    #there may be problems in importing
    for l in req.ordering:
        meal=food.search()
        meal.setsize(l[3])
        meal.settoping(l[4])
        cost+=meal.total_price()
        tm+=meal.timing_process()
        order+=meal.getfullname()
    if req.delivery==True:
        tm+=50
        cost+=30
    ret=orderResponse()
    ret.order=name+order
    ret.time=tm
    ret.price=cost
    #note i thimk the name should be removed after the order is delivered(after the action is completed)
    #but i will leave it here for now
    return ret
def ordsrv(name):
    rospy.init_node("cashier")
    s=rospy.service(name,order,ordhand)
    rospy.loginfo("ordertaker ready")



    #checks for deliverystate if true increase price and assign delivery time to a value
    #returns the final total price,time and the full order with the name
    #removes the user name from the list
    


