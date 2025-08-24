class food:
    items=[]
    # Topic refar list of speciacl topic uniqe for each class 
    def __int__(self, name , Cooking_Time , price ,Toping=None , size=None ):
        self.name = name
        self.Cooking_Time = Cooking_Time
        self.price  = price
        food.items.append(self)
        

    def total_price(self):
        total_price = self.price
        if  self.size == 's':
            total_price = total_price*0.6
        elif self.size == 'm':
            total_price = total_price*0.8
        elif self.size == 'l':
            total_price = total_price
        if self.Toping == 0:
            return  total_price
        else:
            return total_price +10
    def timing_process(self):
         Tp =  self.Cooking_Time
         if  self.size == 's':
            total_price = total_price
         elif self.size == 'm':
            total_price = total_price+5
         elif self.size == 'l':
            total_price = total_price+10
         if self.Toping == 0:
            return   Tp 
    def getname(self):
        return self.name
    def setsize(self,x):
        self.size=x
    def settoping(self,n):
        self.toping=int(n)
    def search(h):
        for item in food.items:
            if item.name[0:3]==h:
                return item
    

    
class main_dish(food):
     
     def __int__(self,name , Cooking_Time , price ,Toping , size ):
         super ().__init__(self, name , Cooking_Time , price ,Toping , size)
         

     list_of_Toping = ["none" ,"cheese" , "sauce", "extra beef"]
     def getfullname(self):
         x = super ().GetName(self)+"size: "+self.size+"with "+main_dish.list_of_Toping[self.Toping]
         return x 
class desert(food):
     def __int__(self,name , Cooking_Time , price ,Toping , size ):
         super ().__init__(self, name , Cooking_Time , price ,Toping , size)

     list_of_Toping = ["none" ,"cherrys" , "extra cream", "exta chocolat"]
     def getfullname(self):
         x = super ().GetName(self)+"size: "+self.size+"with "+desert.list_of_Toping[self.Toping]
         return x 
class snacks(food):
     def __int__(self,name , Cooking_Time , price ,Toping , size ):
         super ().__init__(self, name , Cooking_Time , price ,Toping , size)

     list_of_Toping = ["none" ," cheese sauce" , "ketchup", "hot sauce"]
     def getfullname(self):
         x = super ().GetName(self)+"size: "+self.size+"with "+snacks.list_of_Toping[self.Toping]
         return x 
