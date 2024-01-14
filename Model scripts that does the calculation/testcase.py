import cv2
from ultralytics import YOLO
import mysql.connector
import os

model = YOLO(".//model//custom_modeln1.pt")
capacity = 30 
trains = []

video_path = "D://01projectmain//vid1234.mp4"
output_folder = 'D://01projectmain//saved_images'


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


# Function to extract frames from a video at regular intervals
def extract_frames(video_path, output_folder, interval_seconds=10):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get the frames per second (fps) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calculate the frame interval based on the desired seconds
    frame_interval = int(fps * interval_seconds)

    # Initialize a variable to keep track of the current frame
    current_frame = 0
    i=0

    while True:
        peoples =0 
        # Read the next frame
        ret, frame = cap.read()

        # Break the loop if the video is finished
        if not ret:
            break

        # Save the frame every frame_interval frames, overwriting the previous frame
        if current_frame % frame_interval == 0:
            frame_filename = f"{output_folder}//frame.jpg"
           
            cv2.imwrite(frame_filename, frame)
            results = model(frame_filename,line_thickness=1,show=True)
            peoples = len(results[0])
            print(peoples)
            if peoples > capacity:
                occupancy =100
            else:
                occupancy = (peoples/capacity)*100
            
            print(f'{occupancy}%')
            query = f'UPDATE occupancydata SET c1 = %s WHERE id = %s'
            cursor.execute(query, (round(occupancy,1), 90002))
            conn.commit()
            


            cv2.waitKey()

        current_frame += 1

    
    cap.release()



extract_frames(video_path, output_folder, interval_seconds=20)
