import re
import json


def extract_json(response: str) -> dict:
    # Use a more robust regex to match JSON objects
    match = re.search(r'Action:\s*(\{.*?\})', response, re.DOTALL)

    if match:
        json_str = match.group(1).strip()

        # Remove non-JSON trailing text
        json_str = re.sub(r'\s*(PAUSE|#.*|$)', '', json_str)

        # Fix unbalanced braces
        open_braces = json_str.count('{')
        close_braces = json_str.count('}')
        if open_braces > close_braces:
            json_str += '}' * (open_braces - close_braces)
        elif close_braces > open_braces:
            json_str = '{' + json_str

        # Add missing opening brace if needed
        if not json_str.startswith('{'):
            json_str = '{' + json_str

        # Remove invalid trailing characters and whitespace
        json_str = re.sub(r'[^\{\}\[\]\d\w",:\-.\+\-]', '', json_str)

        # Attempt to parse JSON
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            print("Problematic JSON string:", json_str)
            return {}
    else:
        print("No JSON found in response.")
        return {}


system_prompt = """

You run in a loop of Thought, Action, PAUSE, Action_Response.
At the end of the loop you output an Answer.

You are my personal Appointment AI Agent.
You will help me to manage my appointment. 

Use Thought to understand the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Action_Response will be the result of running those actions.

Your available actions are:

create_appointment:
e.g create_appointment: Adit, 2024-07-25, 05:00, 06:30
read_appointment: 



Example session:

Question: help me to create an appointment with Aditya on 20224-07-25 from 05:00 till 06:
Thought: I will add the appointment on the appointment.csv first.

Action: 

{
  "function_name": "create_appointment",
  "function_params": {
    "Name": "Aditya"
    "Date": "2024-07-25"
    "Start": "05:00:00"
    "End": "06:30:00"
  }
}

PAUSE

You will be called again with this:

Action_Response: 
if succes:
    "Appointment was Added with Aditya on 2024-07-25 at 05:00 until 06:30"
else:
    "Appointment time overlaps with an existing appointment."
"""
