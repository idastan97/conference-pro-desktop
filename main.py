import serial
import queue
from flask import Flask, request, jsonify, Response
import time
import _thread
PORT = "/dev/ttyACM0"
SLEEP_TIME = 2
app = Flask(__name__)
qu = queue.Queue()


@app.route('/put', methods=['GET'])
def add_point():
    data = request.args
    print(data)
    x = data.get('x')
    y = data.get('y')
    print(x, y)
    qu.put((float(x), float(y)))
    resp = Response("ok")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def send_command(ser, com):
    com += "\r\n"
    ser.write(com.encode())
    ser.flush()
    # time.sleep(1)


def main():
    print("segg")
    ser = serial.Serial(PORT, 115200)
    if ser.is_open:
        time.sleep(3)
        com = u"G0 F500"
        send_command(ser, com)
        time.sleep(3)
        while True:
            try:
                x, y = qu.get()
                print("get", x, y)
                com = f"G01 X{x} Y{y}"
                send_command(ser, com)
            finally:
                time.sleep(0.5)


if __name__ == "__main__":
    _thread.start_new_thread(app.run, (), {'host': '0.0.0.0'})
    # app.run(host='0.0.0.0')
    main()
