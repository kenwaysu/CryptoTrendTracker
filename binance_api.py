import websocket
import _thread
import time
import rel
import json



def on_message(ws, message):
    data = json.loads(message)
    # 处理接收到的报价数据
    print("Received quote:", data['p'])

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Closed connection")

def on_open(ws):
    print("Connected to WebSocket")
    # 订阅报价通道
    subscribe_message = json.dumps({"method": "SUBSCRIBE", 
                                    "params":  ["ethusdt@trade"], 
                                    "id": 1})
    ws.send(subscribe_message)



if __name__ == "__main__":
    uri = "wss://stream.binance.com:9443/ws"
 
    ws = websocket.WebSocketApp(uri,  
                                on_message=on_message, 
                                on_error=on_error, 
                                on_close=on_close,
                                on_open = on_open)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()





