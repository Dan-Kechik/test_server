from flask import Flask, request
import requests
import json
import os

sms_api_key = os.environ['MTS_API_KEY']
crm_api_key = os.environ['CRM_API_KEY']
crm_phone = os.environ['CRM_ACCOUNT_PHONE']
mng_phone = os.environ['MANAGER_PHONE']

def take_phone_by_id(client_id):
    request_to_crm = {"request": {
    "client_id": client_id
      }
    }
    resp = requests.post('https://myfavouritecrm.envycrm.com/openapi/v1/client/getContacts/', 
        params={'api_key': crm_api_key}, json=request_to_crm)
    print((resp.text))
    if not resp.status_code == 200:
        print('Can''t take client phone from CRM')
        return None
    ans = json.loads(resp.text)['result']['contacts']
    for c in ans:
        if c['type_id'] == 1:
            return c['value']
    return None

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
    client_id = metadata['form'].get('deal[client_id]', None)
    
    
    enevt_type = metadata['form'].get('event', None) or 'unknown event'
    print('-----')
    print(enevt_type)
    recepient = mng_phone
    
    if enevt_type == 'create_lead' and client_name and client_phone:
        # Inform manager about incoming lead
        send_str = f'Заявка от клиента  {client_name}'
    elif enevt_type == 'create_deal' and client_id:
        # Inform client that lead has approved
        send_str = 'Ваша заявка взята в работу'
        client_phone = take_phone_by_id(client_id)
        if not client_phone:
            send_str = 'Can''t inform client'
        else:
            recepient = client_phone
    else:
        send_str = 'Obtained request without valid arguments'
    
    print(send_str)
    send_str = '  '.join((enevt_type, send_str))
    print(send_str)
    
    payload = {'number': crm_phone, 'destination': recepient, 'text': send_str}
    print(payload)
    r = requests.post(r'https://api.exolve.ru/messaging/v1/SendSMS', headers={'Authorization': 'Bearer '+sms_api_key}, data=json.dumps(payload))
    print('ANS:')
    print(r.text)

    return str(metadata)+f'\n\n---TEXT: '+r.text, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
