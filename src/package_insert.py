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
    
if __name__ == "__main__":
    print(type(get_dose_NL("Adderall")))