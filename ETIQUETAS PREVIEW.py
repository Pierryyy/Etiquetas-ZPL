from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import base64
import io

app = Flask(__name__)
CORS(app, resources={r"/preview": {"origins": ["https://hlg.streetsales.com.br",
                                                  "https://streetsales.com.br", "http://127.0.0.1", "http://localhost"]}})

# Endpoint da API
@app.route('/preview', methods=['POST'])
def preview():
    data = request.get_json(silent=True)
    print("Received data:", base64.b64decode(data['zpl']).decode('utf-8'))

    if data and 'zpl' in data:
        codigoZpl = base64.b64decode(data['zpl'])
        url = 'http://api.labelary.com/v1/printers/6dpmm/labels/4x2/0/'
        files = {'file': codigoZpl}
        headers = {'Accept': 'image/png'}
        response = requests.post(url, headers=headers, files=files, stream=True)

        if response.status_code == 200:
            response.raw.decode_content = True
            png_content = response.content

            # Retorna os bytes da imagem PNG como parte da resposta JSON
            return jsonify({"code": "Success", "image": base64.b64encode(png_content).decode('utf-8')})
        else:
            return jsonify({"code": "Error", "message": 'Labelary API Error'}), 500
    else:
        return jsonify({"code": "False", "message": "No 'zpl' key in data or no data received"}), 400
if __name__ == '__main__':
    app.run(debug=True)
