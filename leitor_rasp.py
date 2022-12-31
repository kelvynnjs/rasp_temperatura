import os
import time
import openpyxl
import threading

# import Adafruit_DHT ---

# Configure the DHT22 sensor
# dispositivo = Adafruit_DHT.DHT22 ---
PIN = 4

# Define the flag variable
stop_flag = False

mutex = threading.Lock()


def iniciar(horarios=None):
    global stop_flag
    # Acquire the mutex before running the loop
    mutex.acquire()
    # Create a new spreadsheet and add a new sheet
    wb = openpyxl.Workbook()
    sheet1 = wb.active
    # Write the header row
    sheet1.append(['Dia do Mês', 'Temperatura (C)', 'Umidade', 'Hora da Leitura', 'Temperatura Média (C)'])
    # Initialize variables to keep track of the total temperature and the number of readings per day
    dia_atual = None
    temperatura_total = 0
    num_leituras = 0
    # Define a list of times that indicate when data should be stored

    horarios_verificacao = horarios
    if horarios_verificacao is None:
        horarios_verificacao = ["02:24", "08:00", "12:00", "16:00", "20:00"]

    # Initialize a counter to keep track of the current time
    indice_horario = 0
    print("Iniciando a aplicação de controle")
    print("Horários configurados para leitura: " + str(horarios_verificacao))

    # Define a flag variable to keep track of whether an entry has been added for the current day at the current time
    entry_added = False

    # Define a flag variable to keep track of the previous minute value
    previous_minute = None

    # Read the temperature and humidity at the specified times
    while not stop_flag:
        # Read data from the sensor
        # umidade, temperatura = Adafruit_DHT.read_retry(dispositivo, PIN)

        umidade, temperatura = 1, 2

        # Get the current date and time
        from datetime import datetime

        agora = datetime.now()
        tempo = agora.strftime("%H:%M")
        print("Tempo ", tempo)

        # Check if the current time is a time to be checked
        if tempo == horarios_verificacao[indice_horario]:
            print("Verificando temperatura as: ", tempo)
            # Check if the current day is different from the previous reading
            if agora.day != dia_atual:
                # If the current day is different, calculate
                # If the current day is different, calculate the average temperature
                if dia_atual is not None:
                    temperatura_media = "{:.2f}".format(temperatura_total / num_leituras)
                    sheet1.append([agora.strftime("%d/%m/%Y"), '', '', '', temperatura_media])

                # Reset the total temperature and number of readings for the new day
                dia_atual = agora.day
                temperatura_total = 0
                num_leituras = 0
                # Reset the flag variable for the new day
                entry_added = False

                # Check if the minute value has changed
            if agora.minute != previous_minute:
                # Update the previous minute value
                previous_minute = agora.minute
                # Add the current temperature to the total temperature and increment the number of readings
                temperatura_total += temperatura
                num_leituras += 1
                # Write the data to the spreadsheet
                sheet1.append([agora.strftime("%d/%m/%Y"), temperatura, umidade, agora.strftime("%H:%M:%S"), ''])
                # Save the spreadsheet
                wb.save(os.path.join(os.getcwd(), 'dados.xlsx'))

                # Increment the time index
            indice_horario += 1
            # If the time index is at the end of the list, reset it to 0
            if indice_horario == len(horarios_verificacao):
                indice_horario = 0
            # Wait for the next time to be checked
            time.sleep(60)


        # Define a function to stop the loop
        def parar():
            global stop_flag
            # Acquire the mutex before changing the flag value
            mutex.acquire()
            # Set the flag value to True
            stop_flag = True
            # Release the mutex
            mutex.release()

