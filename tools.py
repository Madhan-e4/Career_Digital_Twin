import json

def push_unknown_question(question):
    with open("resources/unknown_questions.txt", "a", encoding = "utf-8") as f:
        f.write()

def push_user_details(details):
    with open("resources/record_user_details.txt", "a", encoding = "utf-8") as f:
        f.write(details)


def record_unknown_question(question):
    push_unknown_question(f"\nUnkwown question asked: {question}.\n")
    return "Recorded question"

def record_user_details(email, notes = "Not provided"):
    push_user_details(f"\nUser's email is {email} and notes is {notes}.\n")

record_unknown_question_tool = {
    "name": "record_unknown_question",
    "description": "This tool can be used to record an unknown question",
    "parameters":{
        "type": "object",
        "properties":{
            "question":{"type":"string", "description":"The question that couldn't be answered."}
        },
        "required":["question"],
        "additionalProperties":False
    }
}

record_record_user_details_tool = {
    "name": "record_user_details",
    "description": "This tool can be used to record details of users who want to reach out",
    "parameters":{
        "type": "object",
        "properties":{
            "email":{"type":"string", "description":"Email ID of the user who wants to reach out."},
            "notes":{"type":"string", "description":"Any extra notes that the user might want to provide."}
        },
        "required":["email"],
        "additionalProperties":False
    }
}

tools = [{"type":"function", "function":record_unknown_question_tool}, {"type":"function", "function":record_record_user_details_tool}]

tool_map = {"record_unknown_question":record_unknown_question, "record_user_details":record_user_details}

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        result = tool_map.get(function_name)(**arguments)
        results.append(
            {"role":"tool", "content":json.dumps(result), "tool_call_id":tool_call.id}
        )
    return results
