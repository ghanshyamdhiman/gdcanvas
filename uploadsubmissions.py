
import requests
import time
import pandas as pd
import openpyxl
import json
import mysql.connector
from urllib.parse import urlparse
from urllib.parse import parse_qs



print ("Getting Started OK")

time.sleep(0.25)

def connect_to_db():
    host = "ghanshyamdhiman.com"  
    user = "zo4t10a9m2s_GDUser"        
    password = "Gsd@97001"    
    database = "zo4t10a9m2s_GSTest"   

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
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
        if(workflow_state == "submitted"):
            cursor.execute(sql, record_data)
            conn.commit()

def initialize(end_point):
    CANVAS_API_URL = "https://canvas.true-education.org/api/v1"
    CANVAS_API_TOKEN = "16479~zu8TB4WvxVcry6TcLhvJYUWnRrMN6uTLPnxcRXACYW8ZKNtWem4M9EFvTJAaPD6k"

    url = f'{CANVAS_API_URL}/{end_point}'
    headers = {'Authorization': f'Bearer {CANVAS_API_TOKEN}'}
    response = requests.get(url, headers=headers)
    return response

def get_data(content_name, per_page, page_no):
    response = initialize(f'{content_name}/?per_page={per_page}&page_no={page_no}')
    total_pages = no_of_pages(response)
    print(f'No of Pages : {total_pages}')
    time.sleep(1.0)
    json_list = []
    merged_dict = {}
    while(page_no <= total_pages):
        response = initialize(f'{content_name}/?per_page={per_page}&page_no={page_no}')
        if response.status_code == 200:
            output = response.json()
            print(output)
            json_list.append(output)
            #merged_dict.update(output)
            print(f' Json Array Length: {len(json_list)}')
            time.sleep(2.0)
        else:
            print(f"Status code: {response.status_code}, Response: {response.text}")

        page_no += 1
        print(f'Page No : {page_no}')
        time.sleep(0.1)

    merged_json = json.dumps(merged_dict, indent=4)
    print(merged_json)
    #return merged_json

def get_assignments_list():
    json_data = get_data("courses", 5, 1)
    for item in json_data:
        course_id = item['id]']
        print(f'Course ID : {course_id}')
        time.sleep(1.25)
        #course_id = list(item.values())[0]
        #get_submissions_list(course_id)

def get_submissions_list(course_id):
    json_data = get_data(f'courses/{course_id}/assignments',5,1)
    for item in json_data:
        assignment_id = list(item.values())[0]
        upload_submissions_to_database(course_id, assignment_id)

def upload_submissions_to_database(course_id, assignment_id):
    json_data = get_data(f'courses/{course_id}/assignments/{assignment_id}/submissions',5,1)
    conn = connect_to_db()
    #insert_record(conn, json_data)
    print(f'{course_id}_{assignment_id} Completed')
    time.sleep(0.11)


def no_of_pages(response):
    total_pages = 1
    link_header = response.headers.get('Link', None)
    if link_header:
        links = link_header.split(',')
        link_dict = {}
        
        for link in links:
            section = link.split(';')
            url = section[0].strip()[1:-1]
            rel = section[1].strip().split('=')[1][1:-1]
            link_dict[rel] = url
        
        last_page_url = link_dict.get('last', None)
        
        if last_page_url:
            parsed_url = urlparse(last_page_url)
            page_number = parse_qs(parsed_url.query).get('page', None)
            
            if page_number:
                total_pages = int(page_number[0])
                print("Total number of pages:", total_pages)
    else:
        print("No pagination found.")

    return total_pages

get_assignments_list()

time.sleep(0.25)

print ("Execution Ended")
