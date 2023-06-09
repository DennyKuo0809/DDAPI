import argparse
import requests
import sys


def get_dose_NL(drug_name: str, output_path=None) -> str:
    try:
        print(f"[Info] Drug name: {drug_name}.", file=sys.stderr)
        # Get drug code
        url = f'https://api.fda.gov/drug/ndc.json?search=brand_name:{drug_name}&limit=1'
        response = requests.get(url)
        data = response.json()
        ndc = data['results'][0]['product_ndc']
        

        # Get Dosage
        url = f'https://api.fda.gov/drug/label.json?search=openfda.product_ndc:"{ndc}"&limit=1'
        response = requests.get(url)
        data = response.json()
        dose = data['results'][0]['dosage_and_administration'][0]
        if output_path is not None:
            print(f"[Info] Write to {output_path}.", file=sys.stderr)
            with open(output_path, 'w') as f:
                f.write(dose)
                f.write('\n')
        return dose
    except FileNotFoundError:
        print(f"[Error] File or directory dosen't exist.", file=sys.stderr)
        return ""
    except:
        print(f"[Info] Cannot get message of {output_path} from openFDA.", file=sys.stderr)
        return ""
    
def generate_prompt(drug_name: str, dosage_info: str) -> str:
    prompt_content = f"""Between >>> and <<< is a drug dosage information of {drug_name} for different situations. I need you to extract the column info for different situtation.
    Use array of json object to answer my question. The columns and their definitions are as follow:
    | drug | age | gender | renal_impairment | hepatic_impairment | special_disease | weight | dosage | max_dose | recommend |
    - age:
        - type: TEXT
        - content:
            if the age range is provided, use the format "<min>~<max>" to represent. <min> and <max> are arabic number representing the minimum and the maximum age seperately, for example: "13~17"
            if the age range is not provided, fill in "pediatric" or "adult" or "elderly" depending on your self judge
            if there is no any information about age, fill in "any" to represent
    - gender:
        - type: TEXT
        - content: fill in "male" or "female" or "any" if the gender is not specifically mentioned
    - renal_impairment
        - type: TEXT array
        - content: the possible element are mild/moderate/severe/ESRD, the array can contain multiple severity, leave it an empty array [] if it has nothing to do with renal impairment
    - hepatic_impairment
        - type: TEXT array
        - content: the possible element are mild/moderate/severe, the array can contain multiple severity, leave it an empty array [] if it has nothing to do with hepatic impairment
    - special_disease
        - type: TEXT array
        - content: the possible element are ADHD/MDD/GAD/PD/PTSD/debilitated, put the special disease into the array if the dosage information is for the patient with that special disease
    - weight:
        - type: TEXT
        - content:
            if the weight range is provided, use the format "<min>~<max>" to represent. <min> and <max> are arabic number representing the minimum and the maximum weight seperately, for example: "48~71"
            if there is no any information about weight, fill in "any" to represent
    - weight_unit:
        - type: TEXT
        - content: the unit of the weight, for example "lb". fill in "N/A" if the information is not provided
    - dosage:
        - type: TEXT
        - content: the dosage information for this situation, should always have content
    - max_dosage:
        - type: TEXT
        - content: the maximum dosage information for this situation, leave it "N/A" if no proper information
    - recommend:
        - type: TEXT
        - content: fill in other recommendation that can be shown in the above informations
    >>>{dosage_info}<<<
    """
    return prompt_content

if __name__ == "__main__":
    drug_name = "Adderall"
    print(generate_prompt(drug_name, get_dose_NL(drug_name)))