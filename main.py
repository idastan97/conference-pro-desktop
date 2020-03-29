import serial
import queue
from flask import Flask, request, jsonify, Response
import time
import _thread
PORT = "/dev/ttyACM0"
SLEEP_TIME = 2
app = Flask(__name__)
qu = queue.Queue()
POINT_command = 'POINT'
PEN_UP_command = 'PEN_UP'
PEN_DOWN_command = 'PEN_DOWN'


@app.route('/point', methods=['GET'])
def add_point():
    data = request.args
    if 'x' not in data or 'y' not in data:
        return 'bad request'
    x = data.get('x')
    y = data.get('y')
    qu.put({
        'command': POINT_command,
        'data': [float(x), float(y)]
    })
    resp = Response("ok")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/pen_up', methods=['GET'])
def pen_up():
    qu.put({
        'command': PEN_UP_command,
    })
    resp = Response("ok")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/pen_down', methods=['GET'])
def pen_down():
    data = request.args
    if 'z' not in data:
        return 'bad request'
    z = data.get('z')
    print("pendo")
    print(z)
    qu.put({
        'command': PEN_DOWN_command,
        'data': z
    })
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
        com = u"G0 F5000"
        send_command(ser, com)
        time.sleep(3)
        while True:
            try:
                vals = qu.get()
                print(vals)
                if vals['command'] == POINT_command:
                    x, y = vals['data']
                    print("xy: ", x, y)
                    com = f"G01 X{x} Y{y}"
                elif vals['command'] == PEN_DOWN_command:

                    z = vals['data']
                    print("z: ", z)
                    com = f"M3 S{z}"
                elif vals['command'] == PEN_UP_command:
                    print("pen_up")
                    com = f"M5"
                print(com)
                send_command(ser, com)
            except Exception as e:
                print('exception')
                print(e)
            finally:
                time.sleep(0.5)


if __name__ == "__main__":
    _thread.start_new_thread(app.run, (), {'host': '0.0.0.0'})
    # app.run(host='0.0.0.0')
    main()
