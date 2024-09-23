import requests
import time

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

def print_courses():
    courses = get_data("courses", 10, 1)
    if courses:
        for course in courses:
            print(f'Course id : {course['id']}    Course Name : {course['name']}')
            time.sleep(0.15)

def print_sections(course_id):
    sections = get_data(f'courses/{course_id}/sections', 25,1)
    if sections:
        for section in sections:
            print(f'Section id : {section['id']}    Section Name : {section['name']}')
            time.sleep(0.15)

course_id = '537'
print_sections(course_id)
