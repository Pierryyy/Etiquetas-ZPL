# -*- coding: UTF-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
import base64
from traceback import format_exc

app = Flask(__name__)
CORS(app, resources={r"/pagbank": {"origins": ["https://hlg.streetsales.com.br",
                                                 "https://streetsales.com.br", "http://127.0.0.1", "http://localhost"]}})

# Endpoint da api
@app.route('/etiquetas', methods=['POST'])
def pagbank():
    data = request.json  # Assume that the request body is JSON
    if data:
        codigoZpl = base64.b64decode(data['zpl'])

        # Montar lógica para enviar código zpl para impressora zebra
        try:
            # Replace 'printer_ip' and 'printer_port' with your printer's IP address and port
            printer_ip = data['printer_ip']
            printer_port = data['printer_port']

            # Create a socket connection to the printer
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((printer_ip, printer_port))

                # Send ZPL code to the printer
                # s.sendall(codigoZpl.encode('utf-8'))
                s.sendall(codigoZpl)

            # Montar retorno de sucesso!
            return jsonify({"code": "Success", "message": 'Operation finished'}), 200
        except Exception as e:
            # Capture the detailed exception information for debugging
            exception_traceback = format_exc()

            return jsonify({"code": "Error", "message": str(e), "traceback": exception_traceback}), 500
    else:
        return jsonify({"code": "False", "message": "No data received"}), 400


if __name__ == '__main__':
    # Api
    app.run(debug=True)
