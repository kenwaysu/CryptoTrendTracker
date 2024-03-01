from flask import Flask,request,jsonify,render_template
import websocket
import requests

app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello, World!"

@app.route("/home")
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

if __name__ == '__main__':
    app.run(debug=True)
