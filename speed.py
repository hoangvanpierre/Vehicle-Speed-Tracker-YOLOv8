import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import *
import time
from math import dist
import csv


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

vh_down={}
counter=[]


vh_up={}
counter1=[]

vh_speed={}

fps = 30

# Create and initialize CSV file
f = open('vehicle_data.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(['Vehicle_ID', 'Vehicle_Type', 'Direction', 'Speed_KmH'])

while True:    
    ret,frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 2 != 0:
        continue
    if count < 60:
        continue
    frame=cv2.resize(frame,(1020,500))
   
    # Draw Lines First
    cv2.line(frame,(149,cy1),(689,cy1),(0,255,255),3)
    cv2.putText(frame, 'Len', (152,320), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0,0,0), 4)
    cv2.putText(frame, 'Len', (152,320), cv2.FONT_HERSHEY_COMPLEX, 0.9, (255,255,255), 1)
    cv2.line(frame,(149,cy2),(689,cy2),(0,255,255),3)
    cv2.putText(frame, 'Xuong', (152,442), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0,0,0), 4)
    cv2.putText(frame, 'Xuong', (152,442), cv2.FONT_HERSHEY_COMPLEX, 0.9, (255,255,255), 1)

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
        
        cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
        cv2.putText(frame, str(id), (x3,y3), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,0), 3)
        cv2.putText(frame, str(id), (x3,y3), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255,255,255), 1)

        # Persistent Speed Display
        if id in vh_speed:
            cv2.putText(frame, str(int(vh_speed[id]))+'Km/h', (x4,y4), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0,0,0), 4)
            cv2.putText(frame, str(int(vh_speed[id]))+'Km/h', (x4,y4), cv2.FONT_HERSHEY_COMPLEX, 0.9, (255,255,255), 1)

        if cy1<(cy+offset) and cy1 > (cy-offset):
           vh_down[id]=count
        if id in vh_down:
          
           if cy2<(cy+offset) and cy2 > (cy-offset):
             elapsed_time=(count - vh_down[id]) / fps
             if counter.count(id)==0:
                counter.append(id)
                distance = 30 # calibrated meters
                a_speed_ms = distance / elapsed_time
                a_speed_kh = a_speed_ms * 3.6
                vh_speed[id] = a_speed_kh
                cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                
                # Write to CSV
                writer.writerow([id, vtype, 'L1 to L2', int(a_speed_kh)])

                
        #####going UP#####     
        if cy2<(cy+offset) and cy2 > (cy-offset):
           vh_up[id]=count
        if id in vh_up:

           if cy1<(cy+offset) and cy1 > (cy-offset):
             elapsed1_time=(count - vh_up[id]) / fps
             if counter1.count(id)==0:
                counter1.append(id)      
                distance1 = 30 # calibrated meters
                a_speed_ms1 = distance1 / elapsed1_time
                a_speed_kh1 = a_speed_ms1 * 3.6
                vh_speed[id] = a_speed_kh1
                cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                
                # Write to CSV
                writer.writerow([id, vtype, 'L2 to L1', int(a_speed_kh1)])

           

    d=(len(counter))
    u=(len(counter1))
    cv2.putText(frame, 'Xuong:'+str(d), (60,90), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0,0,0), 4)
    cv2.putText(frame, 'Xuong:'+str(d), (60,90), cv2.FONT_HERSHEY_COMPLEX, 0.9, (255,255,255), 1)

    cv2.putText(frame, 'Len:'+str(u), (60,130), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0,0,0), 4)
    cv2.putText(frame, 'Len:'+str(u), (60,130), cv2.FONT_HERSHEY_COMPLEX, 0.9, (255,255,255), 1)
    cv2.imshow("Result", frame)
    if cv2.waitKey(1)&0xFF==27:
        break

# Write summary and close file
writer.writerow([])
writer.writerow(['Summary'])
writer.writerow(['Total L1 to L2', len(counter)])
writer.writerow(['Total L2 to L1', len(counter1)])
f.close()

cap.release()
cv2.destroyAllWindows()