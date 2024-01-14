from ultralytics import YOLO
import os 
import cv2 
import time
import mysql.connector

model = YOLO('./model/custom_modeln1.pt')
dir = './/images'
num_images = 1
capture_interval = 5  # in seconds
image_resolution = (1280, 720)
capacity = 200




def capture_images(path, num_images, interval,resolution):
    for i in range(num_images):
        while True:
            peoples = 0
 
 
            cap2= cv2.VideoCapture('http://192.168.137.132:8080/video')  #webcam 2
            ret2, frame2 = cap2.read()
            
            #cap3 = cv2.VideoCapture('http://192.168.137.137:8080/video')  #webcam 3
            #ret3,frame3 = cap3.read() 

            # cap4 = cv2.VideoCapture('http://192.168.0.240:8080/video')  #webcam 4
            # ret4,frame4 = cap4.read() 

            if  ret2 :


                #frame0 = cv2.resize(frame0, resolution)

                #frame1 = cv2.resize(frame1, resolution)
                frame2 = cv2.resize(frame2, resolution)
                #frame3 = cv2.resize(frame3, resolution)
                #frame4 = cv2.resize(frame4, resolution)


                #image_path0 = os.path.join(path, f"coach_1/captured_image_{i+1}_cam0.jpg")
                #cv2.imwrite(image_path0, frame0)

                #image_path1 = os.path.join(path, f"coach_1/captured_image_{i+1}_coach_1.jpg")
                #cv2.imwrite(image_path1, frame1)

                image_path2 = os.path.join(path, f"90002/c1/captured_image_{i+1}_coach_2.jpg")
                cv2.imwrite(image_path2, frame2)
                print(image_path2)

                #image_path3 = os.path.join(path, f"90002/c3/captured_image_{i+1}_coach_3.jpg")
                #cv2.imwrite(image_path3, frame3)

                # image_path4 = os.path.join(path, f"coach_4/captured_image_{i+1}_coach_4.jpg")
                # cv2.imwrite(image_path4, frame4)

                print(f"Images {i+1} captured successfully!")

                i = 0
                # for key in trains_occ:
                #     traverse_images_directory(trains[i])
                #     i+=1
                results = model(image_path2,line_width=1,show=True)                
                
                #print(trains_occ)
                

            time.sleep(interval)
    
    #cap0.release()

    #cap1.release()
    cap2.release()
    # cap3.release()
    # cap4.release()
    cv2.destroyAllWindows()

capture_images(dir, num_images, capture_interval,image_resolution)