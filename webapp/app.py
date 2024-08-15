import os
from ultralytics import YOLO
from flask import Flask, render_template, Response,jsonify,request,session
import cv2
import mysql.connector
import time


directory = "images"


#DATABASE CREDENTIALS
host = "sql12.freesqldatabase.com"
user = "sql12648724"
password = "u1M8PhqYWc"
database = "sql12648724"

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
        if root.endswith("c3") or root.endswith("c1") or root.endswith("c2") or root.endswith("c4")or root.endswith("c5")or root.endswith("c6")or root.endswith("c7")or root.endswith("c8")or root.endswith("c9")or root.endswith("c91")or root.endswith("c92"):
            pass
        else:
            trains.append(root)
            #print(root)
            

            
#FUNCTION TO APPLY AND ALGO ON IMAGES AND GET DATA

def traverse_images_directory(directory):
    capacity = 200
    coach_num = 1
    first_directory_processed = False
    for root, dirs, files in os.walk(directory):
        peoples = 0
        if not first_directory_processed:
            first_directory_processed = True
            continue  
        for file in files:
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                # Process the image file
                image_path = os.path.join(root, file)
                results = model(image_path,line_thickness=1,show=True)
                peoples = peoples+len(results[0])
                #cv2.waitKey(0)
        occupancy = (peoples/capacity)*100
        if occupancy<=100:
            occupancy=occupancy
        else:
            occupancy=100
        
        occupancy_coaches.append(occupancy)
           
        print(f'the occupancy of coach{coach_num} is {occupancy}%')
        coach_num+=1 
       
    cv2.destroyAllWindows()




app = Flask(__name__)

model = YOLO('model//custom_model.pt')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect',methods=['POST'])
def detect():
    global occupancy_coaches
    occupancy_coaches=[]
    
    i=0
    q=1
    get_trains(directory)
    t_ids = [90002] #90004,90012,90020,90022]
    n = len(trains)
    trains_occ = {i: '' for i in t_ids}         
    
    
    
    
    #INSERTING TRAINS AS PRIMARY KEY IN THE DATABASE
    for key in trains_occ:
        cursor.execute(f'INSERT IGNORE INTO occupancydata (id) VALUES (%s)', (key,))
        conn.commit()
    for key in trains_occ:
        train = trains[i]
        i+=1
        traverse_images_directory(train)
        for occ_stat in occupancy_coaches:
            cn='c'+str(q)
            print(cn)
            query = f'UPDATE occupancydata SET {cn} = %s WHERE id = %s'
            cursor.execute(query, (occ_stat, key))
            conn.commit()
            query = f'UPDATE occupancydata SET {cn} = %s WHERE id = %s'
            cursor.execute(query, (occ_stat, key))
            conn.commit()
            q+=1
            if q>12:
                q=1
        
        trains_occ[key] = occupancy_coaches.copy()
        occupancy_coaches = []
    
    
    
      
    
    
    #CODE TO DELETE PHOTOS
    #first_directory_processed = False
    #for root, dirs, files in os.walk(directory):
        
     #   if not first_directory_processed:
      #      first_directory_processed = True
       #     continue 
        #for file in files:

         #   if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
          #      file_path = os.path.join(root, file)
           ##    os.remove(file_path)
    return render_template('index.html', occupancy_coaches=occupancy_coaches)


camera = cv2.VideoCapture('http://192.168.0.154:8080/video')

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')






@app.route('/capture',methods=['POST'])
def capture():
    num_images = 1
    interval = 60  # in seconds
    resolution = (640, 640)
    directory = "images"
    path = directory

    while True:
        for i in range(num_images):
            
            cap0 = cv2.VideoCapture(0)
            ret0, frame0 = cap0.read()

            cap1 = cv2.VideoCapture('http://192.168.0.154:8080/video') #webcam 1
            ret1, frame1 = cap1.read()
            
            cap2 = cv2.VideoCapture('http://192.168.0.194:8080/video')  #webcam 2
            ret2, frame2 = cap2.read()
            
            #cap3 = cv2.VideoCapture('http://192.168.0.199:8080/video')  #webcam 3
            #ret3,frame3 = cap3.read() 

            # cap4 = cv2.VideoCapture('http://192.168.0.240:8080/video')  #webcam 4
            # ret4,frame4 = cap4.read() 


            if  ret0:

                frame0 = cv2.resize(frame0, resolution)
                frame1 = cv2.resize(frame1, resolution)
                frame2 = cv2.resize(frame2, resolution)
                #frame3 = cv2.resize(frame3, resolution)
                #frame4 = cv2.resize(frame4, resolution)


                image_path0 = os.path.join(path, f"90002/c1/captured_image_{i+1}_cam0.jpg")
                cv2.imwrite(image_path0, frame0)

                image_path1 = os.path.join(path, f"90002/c2/captured_image_{i+1}_coach_1.jpg")
                cv2.imwrite(image_path1, frame1)

                image_path2 = os.path.join(path, f"90002/c3/captured_image_{i+1}_coach_2.jpg")
                cv2.imwrite(image_path2, frame2)

                #image_path3 = os.path.join(path, f"90002/coach_4/captured_image_{i+1}_coach_3.jpg")
                #cv2.imwrite(image_path3, frame3)

                

                print(f"Images captured successfully!")
                
            
            detect()
            cap0.release()
            #cap1.release()
            #cap2.release()
            #cap3.release()
            #cap4.release()
            time.sleep(interval)
   


if __name__ == "__main__":
    app.run(debug=True)
