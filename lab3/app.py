from graphql import graphql_sync
import time
from flask import Flask, escape, request,jsonify
from ariadne import MutationType, make_executable_schema
from graphql import parse, validate

app = Flask(__name__)   

type_defs = """

    input StudentInput {
        name : String
        id : ID
    }

    type Query {
        name : String
        id : ID
    }
    
    type Student {
        name : String
        id : ID
    }
    type Mutation {
        addStudent(data : StudentInput) : Student
    }
    """



mutation = MutationType()

schema = make_executable_schema(type_defs, mutation)
    
@mutation.field("addStudent")
@app.route("/graphql", methods=["POST"])
def resolve_add_student():  # pylint: disable=unused-variable
    req = request.get_json()
    n = req['name']
    t=time.time()
    StudentInput = {
        'name' : n ,
        'id' : t
    }

    #print(StudentInput)

    #assert data ==  {"name": 'pragati'}
    #return data

    #success, result = graphql_sync(schema, 'mutation { addStudent(data: StudentInput)}')

    print(schema)
    errors = validate(schema, parse("""{addStudent(data : StudentInput) : Student}"""))
    print(errors)
    success,result = graphql_sync(
       schema, 'mutation { addStudent(data: { name: "Bob" , id : ID(t) })}'
    )

    #mutation { addStaff(name: "Bob") { name } }
    #success,result = graphql_sync(
     #   schema, 'mutation { addStudent(data : StudentInput) : Student}'
    #)

    #success,result = graphql_sync(
    #    schema, 'mutation { addStudent(data: { name : n } { id : t}) { name } { id }}'
    #)
   # success, result = graphql_sync(schema, 'mutation { addStudent(data: {StudentInput}){StudentInput}')
   
   
   # query getLogin($username: String, $password: String){
   # login(username: $username, password: $password) {            RQToken          }
    #  }

    #success, result = graphql_sync(
    #    schema, 'mutation { addStudent(data: { "name": "Bob" , "id": time.time()})}'
    #)
    print(result)

    status_code = "200" if success else "400"
    return status_code
    #return result
