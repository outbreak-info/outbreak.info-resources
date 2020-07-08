from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
import os
import db
import re
from datetime import datetime

def remove_html_tags(text):
    """Remove html tags from a string"""
    if text is not None:
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
    else:
        return ""

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/find_user', methods=['POST'])
def find_user():
    user_email = request.form['email']
    user_name = ""
    if "name" in request.form:
        user_name = request.form["name"]

    id = db.get_user(user_email, user_name)
    return redirect(url_for('dataset_browser', user_id = id))

@app.route('/dataset_browser', methods=['POST', 'GET'])
def dataset_browser():
    if 'user_id' in request.args:
        user_id = int(request.args['user_id'])
    else:
        user_id = int(request.form['user_id'])
    dataset_ids = db.get_available_dataset_ids_for_user(user_id)

    name = ""
    description = ""
    keywords = ""
    dataset_id = ""

    if "dataset_id" in request  .args:
        dataset_id = request.args["dataset_id"]
        name, description, keywords = db.get_dataset_details(dataset_id)

    return render_template('dataset_browser.html', dataset_ids = dataset_ids, 
        user_id = user_id, dataset_id = dataset_id, dataset_name = name,
        dataset_description = remove_html_tags(description), dataset_keywords = keywords,
        display_classifications = False, categories = None)

@app.route("/definitions.html")
def definitions():
    return render_template("definitions.html")

@app.route("/classify_dataset")
def classify_dataset():
    user_id = int(request.args['user_id']) 
    dataset_id = request.args["dataset_id"]
    dataset_ids = db.get_available_dataset_ids_for_user(user_id)

    name, description, keywords = db.get_dataset_details(dataset_id)

    categories = db.get_categories()

    return render_template('dataset_browser.html', dataset_ids = dataset_ids, 
        user_id = user_id, dataset_id = dataset_id, dataset_name = name,
        dataset_description = remove_html_tags(description), dataset_keywords = keywords,
        display_classifications = True, categories = categories)

@app.route("/save_classifications", methods=['POST'])
def save_classifications():
    enough_info = request.form["enough_info"]
    user_id = request.form["user_id"]
    dataset_id = request.form["dataset_id"]
    choice_1 = request.form["choice_1"]
    choice_2 = request.form["choice_2"]
    choice_3 = request.form["choice_3"]
    choice_4 = request.form["choice_4"]
    choice_5 = request.form["choice_5"]
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    db.save_classification(user_id, int(dataset_id), now, bool(enough_info),
        int(choice_1), int(choice_2), int(choice_3), int(choice_4), int(choice_5)) 

    return redirect(url_for('thankyou', user_id = user_id))


@app.route("/thankyou.html")
def thankyou():
    return render_template("thankyou.html", user_id = request.args["user_id"])