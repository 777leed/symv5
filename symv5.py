import requests
import time
import json
import openai

def turbo_responds(prompt):
    openai.api_key = "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"
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    )
    return completion.choices[0].message["content"]

# Whatsapp GREEN API
def send_message(chat_id, message):
    id_instance = "1101829018"
    api_token_instance = "5c4dafe85d314497bc3d90876de869e488e3bb82a45d433881"
    url = f"https://api.green-api.com/waInstance{id_instance}/sendMessage/{api_token_instance}"
    payload = {
        "chatId": chat_id,
        "message": message
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.text)
    if response.ok:
        print("Message sent successfully!")
        print("Message:", message)
    else:
        print("Failed to send the message.")


def delete_notification(id):
    id_instance = "1101829018"
    api_token_instance = "5c4dafe85d314497bc3d90876de869e488e3bb82a45d433881" 
    url = f"https://api.green-api.com/waInstance{id_instance}/deleteNotification/{api_token_instance}/{id}"
    response = requests.delete(url)
    result = json.loads(response.text)['result']
    if result == False:
        print("Empty Handed")
        return
    print("Cleaning...")

def receive_notification():
    id_instance = "1101829018"
    api_token_instance = "5c4dafe85d314497bc3d90876de869e488e3bb82a45d433881" 
    url = f"https://api.green-api.com/waInstance{id_instance}/receiveNotification/{api_token_instance}"
    response = requests.get(url)
    if response.status_code == 200:
        response_text = response.text
        # print(response_text.encode('utf8'))
        if response_text != "null":
            response_data = json.loads(response_text)
            receipt_id = response_data.get('receiptId')
            body_data = response_data.get('body', {})
            webhook_type = body_data.get('typeWebhook')
            if webhook_type == 'stateInstanceChanged':
                instance = body_data.get('idInstance', {})
                print("Running Instance:", instance)
            elif webhook_type == 'incomingMessageReceived':
                message_data = body_data.get('messageData', {})
                if message_data.get('typeMessage') == 'extendedTextMessage':
                    text_message = message_data.get('extendedTextMessageData', {}).get('text')
                    print(text_message)
                sender_data = response_data.get('body', {}).get('senderData', {})
                sender_name = sender_data.get('senderName')
                sender_number = sender_data.get('sender')
                print("Sent by:", sender_number, ", AKA:", sender_name)
                reply = turbo_responds(text_message)
                print(reply)
                send_message(sender_number, reply)
            delete_notification(receipt_id)
        else:
            print("Still Waiting...")
    else:
        print("No notification yet. Waiting...")
        time.sleep(2)
def main(): 
    while True:
        receive_notification()

print("Symphony is Awake...")
main()
