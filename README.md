# Real-Time Face Attendance using OpenCV and Firebase
This project is a real-time face attendance system implemented using OpenCV, face recognition, cvzone, and Firebase integration. The system captures video from a webcam, detects faces in real-time, and recognizes known faces by comparing their face encodings. The attendance data is stored and updated in a Firebase Realtime Database, and student images are stored in Firebase Storage.

# Features
Real-time face detection and recognition using OpenCV and the face_recognition library.
Overlaying webcam feed on a graphical background.
Displaying student information and images for recognized faces.
Updating attendance data in the Firebase Realtime Database.
Integrating with Firebase Storage to retrieve student images.
# Prerequisites
Before running the project, ensure you have the following dependencies installed:

Python (version 3.7 or higher)
OpenCV (version 4.5.3 or higher)
face_recognition (version 1.3.0 or higher)
cvzone (version 1.5.0 or higher)
firebase_admin (version 5.0.0 or higher)
You also need to set up a Firebase project and obtain the following:

Firebase service account key file (serviceAccountKey.json)
Firebase Realtime Database URL
Firebase Storage Bucket URL
Installation
Clone or download the project repository.

Install the required Python dependencies using pip:

bash
Copy code
pip install opencv-python
pip install face_recognition
pip install cvzone
pip install firebase_admin
Place the serviceAccountKey.json file in the project directory.

Update the Firebase configuration in the script:

python
Copy code
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-firebase-database-url',
    'storageBucket': 'your-firebase-storage-bucket'
})
Ensure you have the necessary resources in the Resources folder:

Background image (background.png)
Mode images for different states (Modes/)
Encoded face data file (EncodeFile6.pkl)
Usage
Run the script using the following command:

bash
Copy code
python face_attendance.py
The webcam feed will appear along with the attendance system interface.

The system will detect and recognize faces in real-time. If a recognized face is detected, the corresponding student information and image will be displayed on the screen.

The attendance data will be updated in the Firebase Realtime Database based on the last attendance time of the recognized student.

Press 'q' to exit the program.

Contributing
Contributions to this project are welcome. You can contribute by submitting bug reports, feature requests, or pull requests. For major changes, please open an issue first to discuss the proposed changes.

License
This project is licensed under the MIT License.

Acknowledgements
The face_recognition library: https://github.com/ageitgey/face_recognition
The cvzone library: https://github.com/cvzone/cvzone
Firebase: https://firebase.google.com/
Contact
If you have any questions or suggestions, please feel free to contact me at amritanshus367@gmail.com.com.
