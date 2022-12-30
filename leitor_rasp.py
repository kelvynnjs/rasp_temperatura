import os
import time
import Adafruit_DHT
import openpyxl

# Configure the DHT22 sensor
dispositivo = Adafruit_DHT.DHT22
PIN = 4

def iniciar():
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
    horarios_verificacao = ["02:24","08:00", "12:00", "16:00", "20:00"]
    # Initialize a counter to keep track of the current time
    indice_horario = 0
    print("Iniciando a aplicação de controle")
    print("Horários configurados para leitura: " + str(horarios_verificacao))

    # Read the temperature and humidity at the specified times
    while True:
        # Read data from the sensor
        umidade, temperatura = Adafruit_DHT.read_retry(dispositivo, PIN)

        # Get the current date and time
        from datetime import datetime

        agora = datetime.now()
        tempo = agora.strftime("%H:%M")
        print(tempo)

        # Check if the current time is a time to be checked
        if tempo == horarios_verificacao[indice_horario]:
            # Check if the current day is different from the previous reading
            if agora.day != dia_atual:
                # If the current day is different, calculate the average temperature for the previous day
                if dia_atual is not None:
                    temperatura_media = "{:.2f}".format(temperatura_total / num_leituras)
                    sheet1.append([dia_atual, '', '', '', temperatura_media])

                # Reset the total temperature and number of readings for the new day
                dia_atual = agora.day
                temperatura_total = 0
                num_leituras = 0

            # Add the current temperature to the total temperature and increment the number of readings
            temperatura_total += temperatura
            num_leituras += 1

        # Write the data to the spreadsheet
        sheet1.append([agora.day, temperatura, umidade, agora.strftime("%H:%M:%S"), ''])
        # Increment the time index
        indice_horario += 1
        # If the time index is at the end of the list, reset it to 0
        if indice_horario == len(horarios_verificacao):
            indice_horario = 0
        # Sleep for 1 second before checking the time again
        time.sleep(1)

    # Calculate the average temperature for the last day
    temperatura_media = temperatura_total / num_leituras
    sheet1.append([dia_atual, '', '', '', temperatura_media])
    # Save the spreadsheet
    wb.save('controle_temperatura.xlsx')

# Start the application
iniciar()

