from flask import Flask,request,jsonify,render_template
import websocket
import requests
from datetime import datetime

app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello, World!"

@app.route("/")
def home():
    return render_template("home.html")

# @app.route("/<data>")
# def name(data):
#     return f"hello {data}"

@app.route('/search', methods=['POST'])
def search():
    # 接收前端的價格
    data = request.get_json()
    crypto_name = data.get('crypto_name')

    # Binance API讀取
    binance_api_url = f'https://api.binance.com/api/v3/ticker/price?symbol={crypto_name.upper()}USDT'
    response = requests.get(binance_api_url)
    if response.status_code == 200:
        price_data = response.json()
        if 'price' in price_data:
            price = float(price_data['price'])
            # 返回前端
            return jsonify({'crypto_name': crypto_name, 'price': price})
    
    # 錯誤訊息
    return jsonify({'error': 'Unable to fetch price data for the specified cryptocurrency'})

@app.route('/showCurrentKline', methods=['POST'])
def showCurrentKline():
    data = request.get_json()
    crypto_name = data.get('crypto_name')
    tick_interval = '1h'

    url = f'https://api.binance.com/api/v3/klines?symbol={crypto_name.upper()}USDT&interval='+tick_interval
    data = requests.get(url).json()
    kline_data=[]
    for item in data:
        kline_item = {
            'x': datetime.fromtimestamp(item[0] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
            'o': float(item[1]),  
            'h': float(item[2]),  
            'l': float(item[3]),  
            'c': float(item[4]),
            's': [float(item[1]), float(item[4])]
        }
        kline_data.append(kline_item)
    
    # print(kline_data)

    return jsonify(kline_data)

if __name__ == '__main__':
    app.run(debug=True,port='8000',host='0.0.0.0')
