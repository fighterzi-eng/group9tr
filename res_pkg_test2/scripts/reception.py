#!/usr/bin/env python3
import rospy
from res_pkg_test2.srv import start ,startResponse
from customers import customers
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
    

    

if __name__=="__main__":
    rospy.init_node("reception")
    s=rospy.service("reception",start,starthand)
    rospy.loginfo("can i have ur name")
    rospy.spin()
    
