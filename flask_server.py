from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

@app.route('/printData', methods=['POST'])
def receive_data():
    print("Received a POST request")

    # Collecting request metadata
    metadata = {
        "remote_addr": request.remote_addr,
        "method": request.method,
        "url": request.url,
        "base_url": request.base_url,
        "url_root": request.url_root,
        "headers": dict(request.headers),
        "form": request.form.to_dict(),
        "args": request.args.to_dict()
    }

    print("Request Metadata:")
    for key, value in metadata.items():
        print(f"{key}: {value}")
    
    client_name = metadata['form']['lead[values][main][inputs][name][value]']
    client_phone = metadata['form']['lead[values][main][inputs][phone][value]']
    
    api_key = os.environ['MTS_API_KEY']
    crm_phone = os.environ['CRM_ACCOUNT_PHONE']
    mng_phone = os.environ['MANAGER_PHONE']
    payload = {'number': crm_phone, 'destination': mng_phone, 'text': f'Name: {client_name}; Phone:{client_phone}'}
    r = requests.post(r'https://api.exolve.ru/messaging/v1/SendSMS', headers={'Authorization': 'Bearer '+api_key}, data=json.dumps(payload))

    return str(metadata)+f'\n\n---TEXT: '+r.text, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
