the restaurant code is mostly done 
but i haven't tested it because i didn't have the customer code
the reception sevice should receive a name from the customer and if there is less than 3 active customers it will add his name to the customers list which is in a separate file 
and is also accessed and modified by most of the files around it something like a global variable
the service should return a message and a bool and based on the bool the menu appears to the customer
the customer then sends a delivery bool andlist including strings each of lenght 5 the first 3 are used to determine the name of the object ,the th 4th is used to set the size of the object and the last is actually a number used to determine the topping
after the service finishes all the processes related to the order it will return the total time cost and full order 
the name of that service changes dynamically with the username, of course the the customer code will save the username also to use it to access the service, to allow multiple customer to send on the same service at the same time without confliction between messages
the program then loops on the customers list assigning the name variable to the service and initiating it
after that comes the action file wich uses mostly the same idea but in the end it will remove the user name form the list when his order is ready
the feeder file contains the classes the main of which is the food class which all other classes inherit from it adds the object to a list after initiatin them to use that list later in the search method using the first 3 letters of the objects name 
each of the sub classes have a unique class variable in the form of a list containing the topings
the customer also should be an object from the customer class having the attributes name and order and methods intoduce name and order but that's part of the customers code
we though about creating the restaurant as a class that take the food list as an attribute 
but it was going to take more time so we left that for last

