#!/usr/bin/env python3
import rospy
from scripts.feeder import food,main_dish,desert,snacks
from res_pkg_test2.srv import order ,orderResponse
from customers import customers

#i had an idea to deal with multiple customer the base of the idea is that ros uses the service or server name to connect
#to it so it going to be changed for each customer it going to be the customer s name
#i removed the idea of creating a restaurant class because after some thought it felt pointless
#i mean why should we create a class for one or no objects , that is going to overcompicate the code needlesly




#the restaurant is going to recieve a listof strings and delivery bool
#each string is going to contain 5 letters the first 3 are the objects name first 3 letter,4th is the size(s,m,l)
#and the last one is going to be a number that is used to referto the topping 
def ordhand(req):
    cost=0
    tm=0
    order=""
   
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
    ret.order=order
    ret.time=tm
    ret.price=cost
    #note i thimk the name should be removed after the order is delivered(after the action is completed)
    #but i will leave it here for now
    return ret


def create_order_service(username):
    rospy.service(username,order,ordhand)
    rospy.loginfo("order service ready")

  

if __name__=="__main__":
    rospy.init_node("cashier")
    for n in customers:
        create_order_service(n)
    rospy.spin()
    #the action is going to be in a seperate node(later ,for nowlets check that what we have here works)



  
    


