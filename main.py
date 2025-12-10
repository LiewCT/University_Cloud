from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *   # remain custom import

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb
)

output = {}
table = 'student'


# ===============================
# Home Page
# ===============================
@app.route("/", methods=['GET'])
def home():
    return render_template('AddStudent.html')   # change HTML file name later


# ===============================
# About Page
# ===============================
@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')    # Should render HTML file, not URL


# ===============================
# Add Student Record
# ===============================
@app.route("/addstudent", methods=['POST'])
def add_student():
    student_id = request.form['student_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    course = request.form['course']
    year = request.form['year']
    student_image = request.files['student_image']

    insert_sql = "INSERT INTO student VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if student_image.filename == "":
        return "Please select an image file"

    try:
        # Insert DB Record
        cursor.execute(insert_sql, (student_id, first_name, last_name, course, year))
        db_conn.commit()
        full_name = f"{first_name} {last_name}"

        # Upload Image to S3
        file_name_in_s3 = "student-" + str(student_id) + "-image"
        s3 = boto3.resource('s3')

        try:
            print("Record inserted... Uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=file_name_in_s3, Body=student_image)

            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = bucket_location['LocationConstraint']

            if s3_location is None:
                s3_location = ""
            else:
                s3_location = "-" + s3_location

            object_url = f"https://s3{s3_location}.amazonaws.com/{custombucket}/{file_name_in_s3}"

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    return render_template('AddStudentOutput.html', name=full_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
