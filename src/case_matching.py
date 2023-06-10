from enum import IntEnum
import re

class condition(IntEnum):
    DOSE_NOT_MATCH = 0
    MATCH = 1
    IGNORE = 2
    TAGS = 3

def match_age(p_age: str, case: str, overview=False):
    # Ignore
    if case == "any":
        return condition.IGNORE, ""
    
    # Dosage overview
    if overview:
        return condition.TAGS, case

    # Convert Age of patient to number
    patient_age = int(re.findall(r"[-+]?(?:\d*\.*\d+)", p_age)[0])
    if 'month' in p_age:
        patient_age *= 0.01

    # Preprocessing
    case_ = case
    if '>' in case:
        case_ = case.split('<')[1] + '~'
    elif '<' in case:
        case_ = case.replace('>', '~')

    # Precise Age
    if '~' in case_:
        m_age, M_age = case_.split('~')
        min_age, max_age = 0.0, 250.0

        if 'month' in m_age:
            min_age = int(re.findall(r"[-+]?(?:\d*\.*\d+)", m_age)[0]) * 0.01
        elif m_age == '':
            min_age = 0.0
        else:
            min_age = int(re.findall(r"[-+]?(?:\d*\.*\d+)", m_age)[0])

        if 'month' in M_age:
            max_age = int(re.findall(r"[-+]?(?:\d*\.*\d+)", M_age)[0]) * 0.01
        elif M_age == '':
            max_age = 250.0
        else:
            max_age = int(re.findall(r"[-+]?(?:\d*\.*\d+)", M_age)[0])

        if patient_age <= max_age and patient_age >= min_age:
            return condition.MATCH, case
    
    else: # class
        if (patient_age < 18 and case == 'pediatric') or \
            (patient_age >= 18  and patient_age < 75 and case == 'adult') or \
            (patient_age >= 75 and case == "elderly"):
            return condition.MATCH, case

    return condition.DOSE_NOT_MATCH, ""

def match_gender(p_gender: str, case: str, overview=False) -> int:
    # Ignore
    if case == 'any':
        return condition.IGNORE, ""
    
    # Dosage overview
    if overview:
        return condition.TAGS, case
    
    # Match
    if case == p_gender:
        return condition.MATCH, p_gender
    return condition.DOSE_NOT_MATCH, ""

def match_renal_impairment(p_r_i: str, case: list[str], overview=False) -> int:
    # Ignore
    if len(case) == 0:
        return condition.IGNORE, ""
    
    ret = case[0]+" renal impairment" if case[0] != 'ESRD' else 'ESRD'
    for d in case[1:]:
        ret += f", {d} renal impairment" if d != 'ESRD' else ', ESRD'

    # Dosage overview
    if overview:
        return condition.TAGS, ret

    # Match
    if p_r_i in case:
        return condition.MATCH, ret
    return condition.DOSE_NOT_MATCH, ""

def match_hepatic_impairment(p_h_i: str, case: list[str], overview=False) -> int:
    # Ignore
    if len(case) == 0:
        return condition.IGNORE, ""
    
    ret = case[0]+" hepatic impairment"
    for d in case[1:]:
        ret += f", {d} hepatic impairment"
    
    # Dosage overview
    if overview:
        return condition.TAGS, ret

    # Match
    if p_h_i in case:
        return condition.MATCH, ret
    return condition.DOSE_NOT_MATCH, ""

def match_special_disease(p_sd: list[str], case: list[str], overview=False) -> int:
    # Ignore
    if len(case) == 0:
        return condition.IGNORE, ""
    
    ret = case[0]
    for d in case[1:]:
        ret += f", {d}"

    # Dosage overview
    if overview:
        return condition.TAGS, ret
    
    # Match
    p_list = p_sd.sort()
    case_list = case.sort()
    
    if p_list == case_list:
        return condition.MATCH, ret
    return condition.DOSE_NOT_MATCH, ""

def match_weight(p_w: str, case: str, overview=False) -> int:
    # Ignore
    if 'any' in case:
        return condition.IGNORE, ''
    
    # Dosage overview
    if overview:
        return condition.TAGS, case

    KG_2_LB = 2.2
    KG_2_G = 1000.0

    # Convert Age of patient to number
    patient_weight = float(re.findall(r"[-+]?(?:\d*\.*\d+)", p_w)[0])
    if 'lb' in case:
        patient_age *= KG_2_LB
    if 'g' in case and 'kg' not in case:
        patient_weight *= KG_2_G

    # Preprocessing
    case_ = ''
    for ch in case:
        if not ch.isalpha():
            case_ += ch
    if '>' in case:
        case_ = case_.split('>')[1] + '~'
    elif '<' in case:
        case_ = '~' + case_.split('<')[1]

    # Precise Age
    if '~' in case_:
        m_w, M_w = case_.split('~')
        min_w, max_w = 0.0, 250.0

        if m_w == '':
            min_w = 0.0
        else:
            min_w = float(re.findall(r"[-+]?(?:\d*\.*\d+)", m_w)[0])

        if M_w == '':
            max_w = 1000.0
        else:
            max_w = float(re.findall(r"[-+]?(?:\d*\.*\d+)", M_w)[0])

        if patient_weight <= max_w and patient_weight >= min_w:
            return condition.MATCH, f"{min_w}~{max_w}"
    
    return condition.DOSE_NOT_MATCH, ""