import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import*



model=YOLO('yolov8s.pt')



def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)
        

cv2.namedWindow('Result')
cv2.setMouseCallback('Result', RGB)

cap=cv2.VideoCapture('veh1.mp4')


my_file = open("label.txt", "r")
data = my_file.read()
class_list = data.split("\n") 
#print(class_list)

count=0

tracker=Tracker()

cy1=322
cy2=443
offset=25

while True:    
    ret,frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    if count < 60:
        continue
    frame=cv2.resize(frame,(1020,500))
   
    # Draw lines first
    cv2.line(frame,(149,cy1),(689,cy1),(0,255,255),3)
    cv2.line(frame,(149,cy2),(689,cy2),(0,255,255),3)

    results=model.predict(frame)
 #   print(results)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
#    print(px)
    list=[]
             
    for index,row in px.iterrows():
#        print(row)
 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        if c in ['car', 'truck', 'bus', 'motorcycle']:
            list.append([x1,y1,x2,y2,c])
    bbox_id=tracker.update(list)
    for bbox in bbox_id:
        x3,y3,x4,y4,id,vtype=bbox
        cx=int(x3+x4)//2
        cy=int(y3+y4)//2
        cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
        cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),2)
           


    cv2.imshow("Result", frame)
    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()