import cv2
import numpy as np
for i in range(0,17):
    photo=cv2.imread(str(i+1)+".jpg")
    img=cv2.resize(photo,None,fx=900/photo.shape[1],fy=900/photo.shape[0])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 1)
    edges = cv2.Canny(blur, threshold1=190, threshold2=240)
   



    contours , hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)



    for contour in contours:
        area=cv2.contourArea(contour)
  
        if not 50<area <1000:
            continue

        approx = cv2.approxPolyDP(contour, 0.039* cv2.arcLength(contour, True), True)
        #cv2.drawContours(edges, [contour], 0, (255), 1)


        x, y , w, h = cv2.boundingRect(approx)

 
        if len(approx) == 4 :
            cv2.putText(img, "square", (x, y), cv2.FONT_HERSHEY_PLAIN, 0.75, (255), 1, cv2.LINE_AA)
           
        elif len(approx)==3:
            cv2.putText(img, "triangle", (x, y), cv2.FONT_HERSHEY_PLAIN, 0.75, (255), 1, cv2.LINE_AA)
            
        elif 7<len(approx)<10 :
            
            cv2.putText(img, "cross", (x, y), cv2.FONT_HERSHEY_PLAIN, 0.75, (255), 1, cv2.LINE_AA)
            
        else:
           
            cv2.putText(img, "circle "+str(len(approx)), (x, y), cv2.FONT_HERSHEY_PLAIN, 0.75, (255), 1, cv2.LINE_AA)



        cv2.imshow("test",img)
        cv2.waitKey(500)
       
        
        
   
            

