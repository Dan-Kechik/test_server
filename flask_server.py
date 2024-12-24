from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

@app.route('/printData', methods=['POST'])
def receive_data():
    print("Received a POST request")
    print(request.args.to_dict())
    print('================')
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
    
    #print(metadata['form'].keys())
    for key, value in metadata['form'].items():
        print(f"{key}: {value}")
    client_name = metadata['form'].get('lead[values][main][inputs][name][value]', None)
    client_phone = metadata['form'].get('lead[values][main][inputs][phone][value]', None)
    
    
    enevt_type = metadata['form'].get('event', None) or 'unknown event'
    print('-----')
    print(enevt_type)
    if client_name and client_phone:
        send_str = f'Name  {client_name}   Phone {client_phone}' #
    else:
        send_str = 'Obtained request without valid arguments'
    print(send_str)
    #send_str = '  '.join((enevt_type, send_str))
    print(send_str)
    api_key = os.environ['MTS_API_KEY']
    crm_phone = os.environ['CRM_ACCOUNT_PHONE']
    mng_phone = os.environ['MANAGER_PHONE']
    payload = {'number': crm_phone, 'destination': mng_phone, 'text': send_str}
    print(payload)
    r = requests.post(r'https://api.exolve.ru/messaging/v1/SendSMS', headers={'Authorization': 'Bearer '+api_key}, data=json.dumps(payload))
    print('ANS:')
    print(r.text)

    return str(metadata)+f'\n\n---TEXT: '+r.text, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
