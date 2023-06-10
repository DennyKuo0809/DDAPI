import connect_db
import case_matching

class DD_cache:
    def __init__(self, ):
        self.drug_name = ""
        self.structure = []
        self.interested_keys = [
            'age', 
            'gender', 
            'renal_impairment', 
            'hepatic_impairment',
            'special_disease',
            'weight'
        ]
        self.matching_funcs = {
            'age': case_matching.match_age,
            'gender': case_matching.match_gender,
            'renal_impairment': case_matching.match_renal_impairment,
            'hepatic_impairment': case_matching.match_hepatic_impairment,
            'special_disease': case_matching.match_special_disease,
            'weight': case_matching.match_weight
        }
    
    def set_name(self, drug_name: str):
        self.drug_name = drug_name
        ### TODO: connect DB and get data
        data_ = connect_db.dosage_search(drug_name)
        self.structure = data_['structure']

    def clear(self, ):
        self.drug_name = ""
        self.structure = []
        self.interested_keys = []

    def get_interested_keys(self, ) -> list[str]:
        print(self.interested_keys)
        return self.interested_keys
    
    def get_structure(self, ) -> list[dict]:
        return self.structure
    
    def get_options(self, ) -> dict:
        options = {}
        for k in self.interested_keys:
            options[k.replace("_", " ")] = list(self.structure[0][k].keys())
        return options
    
    def overview(self) -> dict:
        instruction = []
        for case in self.structure:
            match_ = True
            condition_str = ""
            for k in self.interested_keys:
                case_parameter = case[k] if k != 'weight' else case['weight']+case['weight_unit']
                match_, match_str = self.matching_funcs[k]("", case_parameter, overview=True)
                if match_ != case_matching.condition.IGNORE:
                    if condition_str == "":
                        condition_str += match_str
                    else:
                        condition_str += f", {match_str}"
            instruction.append(
                {
                    'condition': condition_str,
                    'dosage': case['dosage'],
                    'max_dose': case['max_dose'],
                    'recommend': case['recommend']
                }
            )
          
        return instruction
    
    def match_case(self, p_info: dict) -> dict:
        instruction = []
        at_least_one = False
        for case in self.structure:
            match_ = True
            condition_str = ""
            for k in self.interested_keys:
                case_parameter = case[k] if k != 'weight' else case['weight']+case['weight_unit']
                match_, match_str = self.matching_funcs[k](p_info[k], case_parameter)
                if match_ == case_matching.condition.DOSE_NOT_MATCH:
                    break
                if match_ == case_matching.condition.MATCH:
                    if condition_str == "":
                        condition_str += match_str
                    else:
                        condition_str += f", {match_str}"
            if not match_:
                continue
            else:
                instruction.append(
                    {
                        'condition': condition_str,
                        'dosage': case['dosage'],
                        'max_dose': case['max_dose'],
                        'recommend': case['recommend']
                    }
                )
            
        return instruction