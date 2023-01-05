import json
import multiprocessing
import os
import threading

from flask import Flask, request, render_template, make_response

from leitor_rasp import iniciar

app = Flask(__name__, template_folder='templates')

# Define the flag variable
stop_flag = False

print("stop_flag: ", stop_flag)

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


thread = None


@app.route('/start', methods=['POST'])
def start_app():
    global thread
    global stop_flag

    if thread is None or not thread.is_alive():
        stop_flag = multiprocessing.Value('i', 0)
        horarios = json.loads(request.form.get('horarios'))
        print("horarios", horarios)

        # Load the stored fields data
        update_fields_data(horarios)
        # Set the stop flag to False to start the iniciar() function

        # Start the iniciar() function in a new thread
        thread = threading.Thread(target=iniciar, args=(horarios, stop_flag))
        thread.start()
        return 'Aplicação iniciada'
    else:
        return 'A aplicação já está em execução'


# Define the route for the stop action
@app.route('/stop', methods=['POST'])
def stop_app():
    global thread
    global stop_flag
    # Terminate the current thread

    # Set the stop flag to 1 to stop the iniciar() function
    stop_flag.value = 1
    thread.join(timeout=4)
    msg = 'Aplicação interrompida com sucesso!'
    return msg


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


def update_fields_data(horarios_verificacao):
    # Load the current fields data from the fields_data.json file
    with open('fields_data.json', 'r') as f:
        fields_data = json.load(f)

    # Update the fields data with the new horarios_verificacao value
    fields_data['horarios'] = horarios_verificacao

    # Save the updated fields data to the fields_data.json file
    with open('fields_data.json', 'w') as f:
        json.dump(fields_data, f)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
