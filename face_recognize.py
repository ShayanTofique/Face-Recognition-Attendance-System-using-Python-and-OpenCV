import cv2
import face_recognition
import numpy as np
import csv
from datetime import datetime
import time

known_faces = []
known_names = []

# student data 
student1_images = [
    "student_images/student1_1.jpg",
    # "student_images/student1_2.jpg",
    # "student_images/student1_3.jpg",

    # will add more images for student1 as needed
]

for image_path in student1_images:
    known_faces.append(face_recognition.load_image_file(image_path))
    known_names.append("Shayan Tofique ES 46")

# student2_images = [
#     "student_images/student2_1.jpg",
#     # "student_images/student2_2.jpg",
#     # "student_images/student2_3.jpg",'

#   # will add more images for student1 as needed
# ]

# for image_path in student2_images:
#     known_faces.append(face_recognition.load_image_file(image_path))
#     known_names.append("Hamza Khalid ES 16")

# obtaining the face encoding
known_faces_encodings = [face_recognition.face_encodings(img)[0].flatten() for img in known_faces]

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Create the CSV file for attendance
csv_file = open("attendance.csv", mode='a', newline='')
csv_writer = csv.writer(csv_file)

# Write headers only if the file is empty
if csv_file.tell() == 0:
    csv_writer.writerow(['Name  ', '  Time'])

# Set the delay time (in seconds)
delay_time = 5

# Initialize a dictionary to track if attendance has been marked for each person
attendance_marked = {name: False for name in known_names}

while True:
    # Capture each frame from the webcam
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Error: Could not capture frame from webcam.")
        break

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # After obtaining the face encoding
        # print(f"Known Face Encodings Shape: {known_faces_encodings[0].shape}")
        # print(f"Face Encoding to Check Shape: {face_encoding.shape}")

        face_encoding = face_encoding.flatten()

        # Face comparison
        matches = face_recognition.compare_faces(known_faces_encodings, face_encoding)

        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]

            if not attendance_marked[name]:
                print(f"Attendance Marked: {name}")

                # Draw a green rectangle around the face for recognized faces
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Draw the name below the face
                font = cv2.FONT_HERSHEY_DUPLEX
                text_size = cv2.getTextSize(name, font, 0.5, 1)[0]
                cv2.rectangle(frame, (left, bottom - text_size[1] - 10), (right, bottom), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

                # Mark attendance in CSV
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                csv_writer.writerow([name, current_time])

                # Set the flag to indicate attendance has been marked
                attendance_marked[name] = True
        else:
            # If face is not recognized, draw a red rectangle around the face and display "Unknown"
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            text_size = cv2.getTextSize('Unknown', font, 0.5, 1)[0]
            cv2.rectangle(frame, (left, bottom - text_size[1] - 10), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, 'Unknown', (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the CSV file
csv_file.close()

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
