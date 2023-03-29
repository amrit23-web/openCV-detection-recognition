import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendencerealtime-4116b-default-rtdb.firebaseio.com/'
})

ref = db.reference('Students')

data = {
    '36':{
    'name':'Arif Alam',
    'major':'data science',
    'starting_year':2020,
    'total_attendance':4,
    'standing':'G',
    'year':3,
    'last_attendance_time':"2023-03-27 00:54:34"
    },
    '37':{
    'name':'Elon Musk',
    'major':'Robotics',
    'starting_year':2010,
    'total_attendance':9,
    'standing':'G',
    'year':4,
    'last_attendance_time':"2023-03-27 00:54:34"
    },
    '38':{
    'name':'Lena',
    'major':'data analytics',
    'starting_year':2015,
    'total_attendance':8,
    'standing':'B',
    'year':3,
    'last_attendance_time':"2023-03-27 00:54:34"
    },
    '25':{
    'name':'Amritanshu Sharma',
    'major':'data science',
    'starting_year':2020,
    'total_attendance':8,
    'standing':'G',
    'year':3,
    'last_attendance_time':"2023-03-27 00:54:34"
    },
    '06':{
    'name':'Adiba',
    'major':'data science',
    'starting_year':2020,
    'total_attendance':8,
    'standing':'G',
    'year':3,
    'last_attendance_time':"2023-03-27 00:54:34"
    },
    '12':{
    'name':'Aditya Raj',
    'major':'data science',
    'starting_year':2020,
    'total_attendance':4,
    'standing':'G',
    'year':3,
    'last_attendance_time':"2023-03-27 00:54:34"
    }
}

for key, value in data.items():
    ref.child(key).set(value)