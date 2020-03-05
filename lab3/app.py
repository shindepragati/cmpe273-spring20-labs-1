from ariadne import QueryType, graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, MutationType
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify
import time


app = Flask(__name__)

DB={
    'students':{},
    'classes':{'student':[]}
}

type_defs = load_schema_from_path('schema.graphql')
query = QueryType()
mutation = MutationType()

stud_name=""
stud_id=0

@query.field("hello")
def hello(_, info):
    request = info.context
    user_agent = request.headers.get("User-Agent", "Guest")
    return "Hello, %s!" % user_agent

@query.field("createStudent")
@mutation.field("createStudent")
def createStudent(_, info, name):
    #req = info.context
    n=name
    did=int(time.time())
    DB['students'].update({did : n})
    student = { 
        "id" : did,
        "name" : n
    }
    print(DB)
    return student


@query.field("getStudentDetails")
def getStudentDetails(_, info, id):
    data = DB['students']
    temp=""
    for i in data.keys():
        print(i)
        if int(id)==i:
            temp=data[i]
            break

    if(temp!=""):
        student = { 
        "id" : id,
        "name" : temp
        }     

    return student 

@query.field("createClass")
@mutation.field("createClass")
def createClass(_, info, name):
    
    did=int(time.time())
   
    DB['classes'].update({did : name})
    classes = { 
        "id" : did,
        "name" : name
    }
    
    print(DB)
    return classes 

@query.field("getClassDetails")
def getClassDetails(_, info, id):
    temp=""
    data = DB['classes']
    for i in data.keys():
        print(i)
        if int(id)==i:
            temp=data[i]
            break

    if(temp!=""):
        classes = { 
            "id" : id,
            "name" : temp
        }
    return classes 

@query.field("addStudenttoClass")
@mutation.field("addStudenttoClass")
def addStudenttoClass(_, info, id, classId):
    stud_data = DB['students']
    class_data = DB['classes']
   
    for j in class_data.keys():
        if int(classId)==j:
            temp_class=class_data[j]
            temp_c_id=j
            for i in stud_data.keys():
                print(id,"****i",i)
                if int(id)==i:
                    name=stud_data[i]
                    sid=i
                    print(name,"******",sid)
                    class_data['student'].append({"id":sid,"name":name})
                    DB['classes'].update({temp_c_id : temp_class})
                    print(DB)
                    classes={"id":classId,"name":temp_class,"student":class_data['student']}
                    break
        
    return classes 


schema = make_executable_schema(type_defs, [query, mutation])

@app.route("/graphql", methods=["GET"])
def graphql_playgroud():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    #print(data)
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    #print(result)
    status_code = 200 if success else 400
    return result, status_code


if __name__ == "__main__":
    app.run(debug=True)