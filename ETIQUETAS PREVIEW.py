from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import socket
import requests
import base64
import re
import io


app = Flask(__name__)
CORS(app, resources={r"/etiquetas": {"origins": ["https://hlg.streetsales.com.br",
                                                  "https://streetsales.com.br", "http://127.0.0.1", "http://localhost"]}})

# Endpoint da API
@app.route('/etiquetas', methods=['POST'])
def pagbank():
    data = request.get_json(silent=True)  # Use get_json para obter os dados JSON
    print("Received data:", base64.b64decode(data['zpl']))  # Adicione este print para verificar o conteúdo de data

    if data and 'zpl' in data:
        codigoZpl = base64.b64decode(data['zpl'])
        # Enviar código ZPL para a API Labelary
        url = 'http://api.labelary.com/v1/printers/8dpmm/labels/4x6/0/'
        files = {'file': codigoZpl}
        headers = {'Accept': 'application/pdf'}
        response = requests.post(url, headers=headers, files=files, stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True
            pdf_content = response.content

            # Retornar o PDF como resposta
            return send_file(io.BytesIO(pdf_content),
                             mimetype='application/pdf',
                             as_attachment=True,
                             download_name='label.pdf')
        else:
            return jsonify({"code": "Error", "message": 'Labelary API Error'}), 500
    else:
        return jsonify({"code": "False", "message": "No 'zpl' key in data or no data received"}), 400

if __name__ == '__main__':
    app.run(debug=True)