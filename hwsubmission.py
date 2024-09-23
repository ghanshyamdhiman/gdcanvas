
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
    sql = "INSERT INTO submissions (student_id, assignment_id, submitted_at, workflow_state,submission_id) VALUES (%s, %s, %s, %s, %s)"
    for item in data:
        student_id = item['user_id']
        assignment_id = item['assignment_id']
        submitted_at = item['submitted_at']
        workflow_state = item['workflow_state']
        submission_id = item['id']
        record_data = (student_id, assignment_id, submitted_at, workflow_state,submission_id)
        print(record_data)
        cursor.execute(sql, record_data)
        conn.commit()
        print(cursor.rowcount, "record inserted.")
        time.sleep(0.25)

print ("Started OK")

time.sleep(0.25)

def initialize(end_point):
    CANVAS_API_URL = "https://canvas.true-education.org/api/v1"
    CANVAS_API_TOKEN = "16479~L9ANQNTzAJcAUEZMrMPKffDcTDuRX6PBRCQLtZv3VPa34uAwxARQQxBnamYxuK9P"

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

def upload_submissions_to_database(course_id, assignment_id):
    json_data  = get_data(f'courses/{course_id}/assignments/{assignment_id}/submissions',100,1)
    conn = connect_to_db()
    insert_record(conn, json_data)

upload_submissions_to_database(411, 63610)

time.sleep(0.25)

print ("Execution Ended")
