
import requests
import time
import pandas as pd
import openpyxl
import json
import mysql.connector



def connect_to_db():
    # Connection details
    host = "ghanshyamdhiman.com"  # Your domain name
    user = "zo4t10a9m2s_GDUser"        # Your MySQL username
    password = "Gsd@97001"    # Your MySQL password
    database = "zo4t10a9m2s_GSTest"    # Your database name

    try:
        # Establish the connection
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Create a cursor object
        cursor = conn.cursor()

        # Check connection
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        print("Connected to database:", db_name)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def insert_record(conn, data):
    cursor = conn.cursor()
    sql = "INSERT INTO submissions (assignment_name, submitted_at, student_id, student_name) VALUES (%s, %s, %s, %s)"
    required_data = json.loads(data)
    for item in required_data:
        assignment_name = data['assignment_id']
        submitted_at = data['submitted_at']
        student_id = data['user_id']
        student_name = data['id']
        record_data = (assignment_name, submitted_at, student_id, student_name)
        print(record_data)
    cursor.execute(sql, record_data)
    conn.commit()
    print(cursor.rowcount, "record inserted.")

print ("Started OK")

time.sleep(0.25)

def initialize(end_point):
    CANVAS_API_URL = "https://canvas.true-education.org/api/v1"
    CANVAS_API_TOKEN = "16479~zu8TB4WvxVcry6TcLhvJYUWnRrMN6uTLPnxcRXACYW8ZKNtWem4M9EFvTJAaPD6k"

    url = f'{CANVAS_API_URL}/{end_point}'
    headers = {'Authorization': f'Bearer {CANVAS_API_TOKEN}'}
    response = requests.get(url, headers=headers)
    return response

def get_data(content_name, per_page, page_no):
    response = initialize(f'{content_name}/?per_page={per_page}&page_no={page_no}')
    if response.status_code == 200:
        output = response.json()
        return output
    else:
        print(f"Status code: {response.status_code}, Response: {response.text}")

def print_to_excel(json_data, file_name):
     df = pd.DataFrame(json_data)
     df.to_excel(file_name, index=False)

def get_my_courses():
    json_data = get_data("courses", 100, 1)
    file_name = "courses.xlsx"
    print_to_excel(json_data, file_name)

def get_all_courses_modules():
    json_data = get_data("courses", 100, 1)
    for item in json_data:
        course_id = list(item.values())[0]
        print(course_id)
        time.sleep(0.15)
        get_my_modules(course_id)

def get_courses_assignments_submissions_list():
    json_data = get_data("courses", 100, 1)
    for item in json_data:
        course_id = list(item.values())[0]
        print(course_id)
        time.sleep(0.15)
        get_submissions_list(course_id)

def get_assignments_list():
    json_data = get_data("courses", 100, 1)
    for item in json_data:
        course_id = list(item.values())[0]
        print(course_id)
        time.sleep(0.15)
        get_my_assignments(course_id)

def get_my_modules(course_id):
    json_data = get_data(f'courses/{course_id}/modules',100,1)
    file_name = f'module_{course_id}.xlsx'
    print_to_excel(json_data, file_name)

def get_my_assignments(course_id):
    json_data = get_data(f'courses/{course_id}/assignments',100,1)
    file_name = f'assignment_{course_id}.xlsx'
    print_to_excel(json_data, file_name)

def get_submissions_list(course_id):
    json_data = get_data(f'courses/{course_id}/assignments',100,1)
    for item in json_data:
        assignment_id = list(item.values())[0]
        print(assignment_id)
        time.sleep(0.15)
        get_my_submissions(course_id, assignment_id)

def get_my_submissions(course_id, assignment_id):
    json_data = get_data(f'courses/{course_id}/assignments/{assignment_id}/submissions',100,1)
    file_name = f'submissions_{assignment_id}.xlsx'
    print_to_excel(json_data, file_name)

def upload_submissions_to_database(course_id, assignment_id):
    json_data = get_data(f'courses/{course_id}/assignments/{assignment_id}/submissions',100,1)
    conn = connect_to_db()
    insert_record(conn, json_data)


#get_my_courses()
get_all_courses_modules()
#get_assignments_list()
#get_courses_assignments_submissions_list()

#upload_submissions_to_database(411, 63610)

time.sleep(0.25)

print ("Execution Ended")
