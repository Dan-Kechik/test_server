from flask import Flask, request

app = Flask(__name__)

@app.route('/print', methods=['POST'])
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

    return str(metadata), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
