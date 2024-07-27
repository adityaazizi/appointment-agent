import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from crud import CRUD, Appointment
from agent import Agent
from utils import extract_json, system_prompt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = Agent()
crud = CRUD()

available_actions = {
    'create_appointment': crud.create_appointment,
}

messages = [
    {"role": "system", "content": system_prompt},
]


@app.get('/')
async def root():

    return 'p balap'


@app.post("/chat")
async def chat_with_agent(request: Request):
    body = await request.json()
    user_prompt = body.get('message', {}).get('content')
    messages.append({"role": "user", "content": user_prompt})
    response = agent.get_openai_response(messages=messages)
    json_function = extract_json(response)

    if json_function is {}:
        return f'please provide more information'
    function_name = json_function['function_name']
    function_params = json_function['function_params']
    if function_name not in available_actions:
        return f"Unknown action: {function_name}: {function_params}"
    
    action_function = available_actions[function_name]
    result = action_function(**function_params)

    return JSONResponse(content={"message": {"content": result}})


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080))
    )
