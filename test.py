import requests

url = 'http://0.0.0.0:8080/chat'

while True:
    # Prompt the user for input
    message = input("Enter your message (or type 'exit' to quit): ")

    # Check if the user wants to exit the loop
    if message.lower() == 'exit':
        break

    # Prepare the input data
    input_data = {
        'message': message
    }

    # Send the request
    response = requests.post(url, json=input_data)

    # Check the response status
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print('Error:', response.status_code)

print("Exited the chat loop.")