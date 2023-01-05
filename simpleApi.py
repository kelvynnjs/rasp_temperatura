import Adafruit_DHT
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
   return 'API de temperatura e umidade!'

@app.route('/temperature-humidity')
def temperature_humidity():
   humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
   return {'temperatura': temperature, 'umidade': humidity}

if __name__ == '__main__':
   app.run(host='0.0.0.0')
