from ultralytics import YOLO
import os 
import cv2 
import time
import mysql.connector

model = YOLO('./model/custom_modeln1.pt')
dir = './/images'
num_images = 1
capture_interval = 10  # in seconds
image_resolution = (1280, 720)
capacity = 200




#DATABASE CREDENTIALS
host = "sql12.freesqldatabase.com"
user = "sql12676621"
password = "1IAzS1vLys"
database = "sql12676621"

#CONNECTING THE DATABASE
try:
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if conn.is_connected():
        print("Connected to the database")

    # Now, you can create a cursor to execute SQL queries
    cursor = conn.cursor()

except mysql.connector.Error as e:
    print("Error connecting to the database:", e)

trains = []

def get_trains(directory):
    first_directory_processed = False
    for root,dirs,files in os.walk(directory):
        if not first_directory_processed:
            first_directory_processed = True
            continue  
        if root.endswith("c3") or root.endswith("c1") or root.endswith("c2") or root.endswith("c4")or root.endswith("c5")or root.endswith("c6")or root.endswith("c7")or root.endswith("c8")or root.endswith("c9")or root.endswith("c91")or root.endswith("c92")or root.endswith("c93"):
            pass
        else:
            trains.append(root)
get_trains("./images")





t_ids = [90002,90004,90012,90020,90022]
              

#DICTIONARY CONTAINING TRAINS AS KEY AND LIST OF COACH OCCUPANCY AS VALUE
trains_occ = {i: [] for i in t_ids} 

def dataupload(trainocc):
    q=1
    for key,values in trainocc.items():
        for value in values:
            cn ='c'+str(q) 
                    
            query = f'UPDATE occupancydata SET {cn} = %s WHERE id = %s'
            cursor.execute(query, (value, key))
            conn.commit()
            q+=1
            if q>12:
                q=1 
                



def capture_images(path, num_images, interval,resolution):
    for i in range(num_images):
        while True:
            peoples = 0
            
        
            #ret0, frame0 = cap0.read()

            #cap1 = cv2.VideoCapture('')
            #ret1, frame1 = cap1.read()
            
            cap2 = cv2.VideoCapture('http://192.168.137.137:8080/video')  #webcam 2
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
                traverse_images_directory(trains[0],next(iter(trains_occ)))
                
                #print(trains_occ)
                

            time.sleep(interval)
    
    #cap0.release()

    #cap1.release()
    cap2.release()
    # cap3.release()
    # cap4.release()
    cv2.destroyAllWindows()

def traverse_images_directory(dir,key):
    global trains_occ
    peoples = 0 
    first_directory_processed = False
    for root, dirs, files in os.walk(dir):
        if not first_directory_processed:
            first_directory_processed = True
            continue  
        for file in files:
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                # Process the image file
                image_path = os.path.join(root, file)
                results = model(image_path,line_thickness=1,show=True)
                cv2.waitKey()
                peoples = peoples + len(results[0])
                
    
        if peoples>capacity:
            occupancy=100
        else:
            occupancy=(peoples/capacity)*100
            
        print(key)
        trains_occ[key].append(occupancy)
   
    
    dataupload(trains_occ)
    print(trains_occ)
    trains_occ = {}
    trains_occ = {i: [] for i in t_ids} 
    cv2.destroyAllWindows()
                


# Call the function to capture images
capture_images(dir, num_images, capture_interval,image_resolution)
