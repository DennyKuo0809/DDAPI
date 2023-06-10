from flask import Flask, render_template, request
from dosage_cache import *
from connect_3rd_party import *
from connect_db import *
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    global DDC
    global patients_data
    patients = patients_data.keys()
    if request.method == 'POST':
        DDC.set_name(request.form['drug_name'])
        instruction = DDC.overview()
        return render_template('index.html', 
                                phase='show_dosage', 
                                drug_name=request.form['drug_name'],
                                dosage=instruction,
                                info={},
                                patients=patients)
    else: # Fetch drug name
        return render_template('index.html', 
                               phase='fetch_drug_name', 
                               drug_name="", 
                               dosage=[],
                               info={},
                               patients=patients)


@app.route('/patient/<name>', methods=['GET', 'POST'])
def patient_info(name):
    global patients_data
    global DDC
    d = patients_data[name]
    patients = patients_data.keys()

    if request.method == 'POST':
        DDC.set_name(request.form['drug_name'])
        instruction = DDC.match_case(d)
        return render_template('patient.html', 
                                phase='show_dosage', 
                                drug_name=request.form['drug_name'],
                                dosage=instruction,
                                info=d,
                                patients=patients)
    else: # Fetch drug name
        return render_template('patient.html', 
                               phase='fetch_drug_name', 
                               drug_name="", 
                               dosage=[],
                               info=d,
                               patients=patients)

@app.route('/add_medicine', methods=['GET', 'POST'])
def db():
    patients = patients_data.keys()
    if request.method == 'POST':
        form_name = request.form['form_name']

        if form_name == 'generate-prompt':
            FDA_instruction = get_dose_NL(request.form['drug_name'])
            prompt = generate_prompt(request.form['drug_name'], FDA_instruction)
            return render_template('db.html', 
                                    phase='show_prompt', 
                                    drug_name=request.form['drug_name'],
                                    FDA_instruction=FDA_instruction,
                                    prompt=prompt,
                                    patients=patients)
        elif form_name == 'save-to-db':
            print(request.form.keys())
            save_to_db(request.form['drug_name'], request.form['gpt-4-result'])
            return render_template('db.html', 
                               phase='fetch_drug_name', 
                               drug_name="",
                               FDA_instruction="",
                               prompt="",
                               patients=patients)
    else: # Fetch drug name
        return render_template('db.html', 
                               phase='fetch_drug_name', 
                               drug_name="",
                               FDA_instruction="",
                               prompt="",
                               patients=patients)

if __name__ == "__main__":
    global DDC
    global patients_data

    DDC = DD_cache()
    path_to_patient = "data/patients.json"
    with open(path_to_patient, 'r') as f:
        patients_data = json.load(f)
        for name in patients_data.keys():
            patients_data[name]['name'] = name
            s_d = ""
            for d_ in patients_data[name]["special_disease"]:
                s_d += d_ + ", "
            patients_data[name]["special_disease"] = s_d[:-2]

    app.run()