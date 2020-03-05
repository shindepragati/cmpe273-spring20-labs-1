import time
from flask import Flask, escape, request,jsonify

app = Flask(__name__)


DB={
    'students':{},
    'classes':{'student':[]}
}


@app.route('/')
def add():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

 # Save the student name with id as timestamp in DB['students']
@app.route('/students/',methods=['POST'])          
def create_new_student():
    req = request.json 
    name=req["name"]
    did=time.time()
   
    DB['students'].update({did : name})
    response = jsonify(
        id=did,
        name=name
    )
    
    print(DB)
    return response 

 # Get the student details for the given id
@app.route('/students/<id>',methods=['GET'])
def fetch_student_details(id):
    data = DB['students']
    for i in data.keys():
        print(i)
        if float(id)==i:
            str = jsonify(
            id=id,
            name=data[i])
            break
        else:
            str="Student Details Not Found"

    response = str       

    return response 

# Save the class name with id as timestamp in DB['classes']
@app.route('/classes/',methods=['POST'])
def add_class():
    #print(request.get_json()) 
    req = request.json 
    name=req["name"]
    did=time.time()
   
    DB['classes'].update({did : name})
    response = jsonify(
        id=did,
        name=name
    )
    
    print(DB)
    return response 

# Get the class details for the given id
@app.route('/classes/<id>',methods=['GET'])
def fetch_classes_details(id):
    data = DB['classes']
    for i in data.keys():
        print(i)
        if float(id)==i:
            str = jsonify(
            id=id,
            name=data[i])
            break
        else:
            str="classes Details Not Found"      
    
    response = str
    return response 

# Patch two request - 1. create id for the class name 2. get the specificd student details from DB['students'] and add to the list 'student' in DB['classes']
@app.route('/classes/<s_id>/<c_name>',methods=['PATCH'])
def add_student_to_class(s_id,c_name):
    stud_data = DB['students']
    class_data = DB['classes']
    for i in class_data.keys():
        if class_data[i]==c_name:
            temp_class=class_data[i]
            temp_c_id=i

    for i in stud_data.keys():
        if float(s_id)==i:
            temp_stud_id=stud_data[i]
            class_id=temp_c_id
           # name="CMPE-273"
            class_name=temp_class
            print("**********class_name",class_name)
            class_data['student'].append({s_id:temp_stud_id})
            DB['classes'].update({class_id : class_name})
            str=jsonify(id=class_id,name=class_name,student=class_data['student'])
            break
        else:
            str="classes Details Not Found"  
    #print(DB['classes'])
    response = str
    #print(DB)
    return response 
    

