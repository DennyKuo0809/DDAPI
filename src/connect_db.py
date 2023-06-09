from pymongo.mongo_client import MongoClient
import json

def dosage_search(medicine):
    client = MongoClient("mongodb+srv://dbuser:dbuserpassword@cluster0.uidhxdw.mongodb.net/?retryWrites=true&w=majority")
    db = client['drugdb']
    collection = db['drugcollection']
    count = collection.count_documents({'name':medicine})
    if count==0:
        print("Not found!")
        return {}
    dosages = collection.find({'name':medicine})
    return dosages[0]

def save_to_db(formatted_text: str):
    pass



def insert_json():
    client = MongoClient("mongodb+srv://dbuser:dbuserpassword@cluster0.uidhxdw.mongodb.net/?retryWrites=true&w=majority")
    db = client['drugdb']
    collection = db['drugcollection']
    current_dir = os.getcwd()  # 获取当前目录路径
    files = os.listdir(current_dir)  # 获取当前目录下的所有文件和文件夹
    json_files = [file for file in files if file.endswith('.json')]
    for json_file in json_files:
        drug_name = json_file.split(".")[0]
        with open(json_file) as f: #檔名
            data = json.load(f)
            if not collection.find_one({'name':drug_name}):
                collection.insert_one({'name':drug_name, 'structure':data['structure'],'interested_keys':data['interested_keys']})
                print(f"Insert {drug_name}.json.")
            else:
                print(f"{drug_name} already in db.")