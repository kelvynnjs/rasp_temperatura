import importlib
import json
import os
import time

import importlib

# Import test module in a lazy way
leitor_rasp = importlib.import_module("leitor_rasp")

from flask import Flask, request, render_template, send_file, make_response

app = Flask(__name__, template_folder='templates')

# Define the flag variable
stop_flag = False

print("stop_flag: ",stop_flag)

# Initialize the fields_data.json file with default values
if not os.path.exists('fields_data.json'):
    with open('fields_data.json', 'w') as f:
        fields_data = {
            'horarios': []
        }
        json.dump(fields_data, f)


@app.route('/', methods=['GET'])
def index():
    # Load the fields data from the fields_data.json file
    with open('fields_data.json', 'r') as f:
        fields_data = json.load(f)

    # Get the list of times from the fields data
    horarios_verificacao = fields_data['horarios']

    # Render the index template with the fields data
    return render_template('index.html', horarios_verificacao=horarios_verificacao)


# INICIA A APLICAÇÃO
@app.route('/start', methods=['POST'])
def start_app():
    global stop_flag

    horarios = json.loads(request.form.get('horarios'))
    print("horarios", horarios)

    print(request.form.keys())

    # Load the stored fields data

    updateFieldsData(horarios)

    leitor_rasp.iniciar(horarios)

    # Set the stop flag to False to start the iniciar() function
    stop_flag = False

    return 'Aplicação iniciada'


# Define the route for the stop action
@app.route('/stop', methods=['POST'])
def stop_app():
    global stop_flag
    # Set the stop flag to True to stop the iniciar() function
    print("Tentando encerrar")
    leitor_rasp.parar()
    print("stop_flag: ", stop_flag)
    # Release the mutex to allow other threads to acquire it
    # mutex.release()
    return 'Aplicação interrompida com sucesso!'


@app.route('/download')
def download():
    # Set the response headers
    response = make_response()
    response.headers["Content-Disposition"] = "attachment; filename=dados.xlsx"
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    # Read the contents of the file into memory
    with open("dados.xlsx", "rb") as f:
        response.data = f.read()

    return response


def updateFieldsData(horarios_verificacao):
    # Load the current fields data from the fields_data.json file
    with open('fields_data.json', 'r') as f:
        fields_data = json.load(f)

    # Update the fields data with the new horarios_verificacao value
    fields_data['horarios'] = horarios_verificacao

    # Save the updated fields data to the fields_data.json file
    with open('fields_data.json', 'w') as f:
        json.dump(fields_data, f)





# def iniciar(horarios=None):
#     global stop_flag
#     while not stop_flag:
#         print("Executando")
#         print(horarios)
#         time.sleep(2)
#         if stop_flag:
#             break
#     print("Encerrando ------------")



if __name__ == '__main__':
    app.run(host='0.0.0.0')
