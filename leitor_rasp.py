import board
import digitalio
import adafruit_dht
import openpyxl


def iniciar():
    # Configure o sensor DHT22
    dispositivo_dht = adafruit_dht.DHT22(board.D4)
    # Crie uma nova planilha e adicione uma aba
    wb = openpyxl.Workbook()
    sheet1 = wb.active
    # Escreva a linha de cabeçalho
    sheet1.append(['Dia do Mês', 'Temperatura (C)', 'Umidade', 'Hora da Leitura', 'Temperatura Média (C)'])
    # Inicialize variáveis para manter o controle da temperatura total e do número de leituras por dia
    dia_atual = None
    temperatura_total = 0
    num_leituras = 0
    # Defina uma lista de horários que indicam quando os dados devem ser armazenados
    horarios_verificacao = ["08:00:00", "12:00:00", "16:00:00", "20:00:00"]
    # Inicialize um contador para manter o controle do horário atual
    indice_horario = 0
    print("Iniciando a aplicação de controle")
    print("Horários configurados para leitura: " + horarios_verificacao)
    # Leia a temperatura e a umidade nos horários especificados
    while indice_horario < len(horarios_verificacao):
        # Leia os dados do sensor
        temperatura = dispositivo_dht.temperature
        umidade = dispositivo_dht.humidity

        # Obtenha a data e hora atuais
        from datetime import datetime

        agora = datetime.now()

        # Verifique se o horário atual é um horário a ser verificado
        if agora.strftime("%H:%M:%S") == horarios_verificacao[indice_horario]:
            # Verifique se o dia atual é diferente da leitura anterior
            if agora.day != dia_atual:
                # Se o dia atual for diferente, calcule a temperatura média para o dia anterior
                if dia_atual is not None:
                    temperatura_media = temperatura_total / num_leituras
                    sheet1.append([dia_atual, '', '', '', temperatura_media])

                # Redefina a temperatura total e o número de leituras para o novo dia
                dia_atual = agora.day
                temperatura_total = 0
                num_leituras = 0

            # Adicione a temperatura atual à temperatura total e incremente o número de leituras
            temperatura_total += temperatura
            num_leituras += 1
    # Escreva os dados na planilha
    sheet1.append([agora.day, temperatura, umidade, agora.strftime("%H:%M:%S"), ''])
    # Incremente o índice de horário
    indice_horario += 1
    # Calcule a temperatura média para o último dia
    temperatura_media = temperatura_total / num_leituras
    sheet1.append([dia_atual, '', '', '', temperatura_media])
    # Salve a planilha
    wb.save('controle_temperatura.xlsx')
