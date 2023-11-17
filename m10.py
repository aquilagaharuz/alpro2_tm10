from flask import Flask, render_template, request, jsonify, redirect, url_for
import csv
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='template')

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/biodata/')
def biodata():
    return render_template('biodata.html')

@app.route('/cv/')
def cv():
    return render_template('cv.html')

@app.route('/portofolio/')
def portofolio():
    return render_template('portofolio.html')

@app.route('/daftarmatkultsd/')
def hobby():
    return render_template('matkul.html')

todos = []

@app.route('/todolist')
def todolist():
    return render_template('todolist.html')

@app.route('/add_todo', methods=['POST'])
def add_todo():
    data = request.get_json()
    new_todo = data['todo'].strip()

    if new_todo:
        todos.append(new_todo)
        return jsonify({'success': True, 'todos': todos})
    else:
        return jsonify({'success': False, 'message': 'Please enter a task!'})

@app.route('/delete_todo/<int:index>', methods=['DELETE'])
def delete_todo(index):
    if index < len(todos):
        del todos[index]
        return jsonify({'success': True, 'todos': todos})
    else:
        return jsonify({'success': False, 'message': 'Todo not found!'})

@app.route('/fibonacci/')
def fibonacci_submit():
    return render_template('fibonacci.html', num=num)

@app.route("/csvtojson/", methods=["GET", "POST"])
def csv_to_json():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]

        if file.filename == "":
            return "No selected file"

        allowed_extensions = {"csv"}
        if "." not in file.filename or file.filename.rsplit(".", 1)[1].lower() not in allowed_extensions:
            return "Invalid file type. Please upload a CSV file."

        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        json_data = convert_csv_to_json(file_path)

        return jsonify(json_data)

    return render_template("csvtojson.html")

def convert_csv_to_json(file_path):
    with open(file_path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        json_data = [row for row in csv_reader]
        
    return json_data

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/calculate', methods=['POST'])
def calculate_bmi():
    if request.method == 'POST':
        name = request.form['name']
        weight = float(request.form['weight'])
        height = float(request.form['height'])

        bmi_value, bmi_category = calculate_bmi_value(weight, height)

        return "<h1>Hi {0}, your BMI is {1}. You're {2}</h1>".format(name, bmi_value, bmi_category)

def calculate_bmi_value(weight, height):
    bmi_value = round(weight / (height ** 2), 2)
    bmi_category = categorize_bmi(bmi_value)
    return bmi_value, bmi_category

def categorize_bmi(bmi_value):
    if bmi_value < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi_value < 24.9:
        return 'Normal weight'
    elif 25 <= bmi_value < 29.9:
        return 'Overweight'
    else:
        return 'Obesity'