from enum import IntEnum

class condition(IntEnum):
    DOSE_NOT_MATCH = 0
    MATCH = 1
    IGNORE = 2
    TAGS = 3

def match_age(p_age: str, case: dict, all_case=False):
    p_age_ = int(p_age) if p_age != "" else -1
    min_age = int(case["min"])
    max_age = int(case["max"])

    # Ignore
    if min_age == 0 and \
        max_age == 0 and \
        not case["pediatric"] and \
        not case["adult"] and \
        not case["elderly"]:
        return condition.IGNORE, ""
    
    if all_case:
        if min_age != 0 or max_age != 0:
            return condition.TAGS, f"{min_age}-{max_age}"
        else:
            tag_list = ""
            for key in ['pediatric', 'adult', 'elderly']:
                if case[key]:
                    tag_list += key + ", "
            return condition.TAGS, tag_list[:-2]
    
    # Precise Age
    if min_age != 0 or max_age != 0:
        if min_age <= p_age_ and max_age >= p_age_:
            return condition.MATCH, f"{min_age}-{max_age}"
        return condition.DOSE_NOT_MATCH, ""
    # Group
    if p_age_ < 18 and case["pediatric"]:
        return condition.MATCH, "pediatric"
    if p_age_ >= 18 and case["adult"]:
        return condition.MATCH, "adult"
    if p_age_ >= 75 and case["elderly"]:
        return condition.MATCH, "elderly"
    
    return condition.DOSE_NOT_MATCH, ""

def match_gender(p_gender: str, case: dict, all_case=False) -> int:
    if all_case:
        if not case['male'] and not case['female']:
            return condition.IGNORE, ""
        else:
            tag_list = ""
            for key in ['male', 'female']:
                if case[key]:
                    tag_list += key + ", "
            return condition.TAGS, tag_list[:-2]
        
    if case[p_gender]:
        return condition.MATCH, p_gender
    return condition.DOSE_NOT_MATCH, ""

def match_renal_impairment(p_r_i: str, case: dict, all_case=False) -> int:
    if not case["mild"] and \
        not case["moderate"] and \
        not case["severe"] and \
        not case["ESRD"]:
         return condition.IGNORE, ""
    
    if all_case:
        tag_list = ""
        for key in ['mild', 'moderate', 'severe', 'ESRD']:
            if case[key]:
                tag_list += key + " renal impairment, "
        return condition.TAGS, tag_list[:-2]
    
    if case[p_r_i]:
        if p_r_i == "ESRD":
            return condition.MATCH, f"ESRD"
        return condition.MATCH, f"{p_r_i} renal impairment"
    
    return condition.DOSE_NOT_MATCH, ""

def match_hepatic_impairment(p_h_i: str, case: dict, all_case=False) -> int:
    
    if not case["mild"] and \
        not case["moderate"] and \
        not case["severe"]:
        return condition.IGNORE, ""
    
    if all_case:
        tag_list = ""
        for key in ['mild', 'moderate', 'severe']:
            if case[key]:
                tag_list += key + " hepatic impairment, "
        return condition.TAGS, tag_list[:-2]
    
    if case[p_h_i]:
        return condition.MATCH, f"{p_h_i} hepatic impairment"
    
    return condition.DOSE_NOT_MATCH, ""

def match_special_disease(p_sd: list[str], case: dict, all_case=False) -> int:
    if all_case:
        intereted_list = case.keys()
    else:
        intereted_list = p_sd

    d_list = ""
    for v in intereted_list:
        if case[v]:
            if d_list == "":
                d_list += v
            else:
                d_list += f", {v}"
    if d_list != "":
        return condition.MATCH, d_list
    else:
        return condition.IGNORE, ""

def match_weight(p_w: str, case: dict, all_case=False) -> int:
    kg_to_lb = 2.2

    min_weight = float(case["min"])
    max_weight = float(case["max"])
    p_w_ = float(p_w[:-2]) if p_w != "" else -1

    if 'lb' in case['unit']:
        p_w_ *= kg_to_lb

    if min_weight == 0 and max_weight == 0:
        return condition.IGNORE, ""
    
    if all_case:
        return condition.TAGS, f"{min_weight}-{max_weight} {case['unit']}"
    
    if min_weight <= p_w_ and max_weight >= p_w_:
        return condition.MATCH, f"{min_weight}-{max_weight} {case['unit']}"
    
    return condition.DOSE_NOT_MATCH, ""