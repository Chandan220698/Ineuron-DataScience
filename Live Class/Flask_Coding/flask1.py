from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/xyz', methods = ['GET', 'POST'])
def test():
    if request.method == 'POST':
        a = request.json['num1']
        b = request.json['num2']

        return jsonify(str(a+b))

@app.route('/xyz/abc1', methods = ['GET', 'POST'])
def test1():
    if request.method == 'POST':
        a = request.json['num3']
        b = request.json['num4']

        return jsonify(str(a+b))

@app.route('/xyz/abc2', methods = ['GET', 'POST'])
def test2():
    if request.method == 'POST':
        a = request.json['num5']
        b = request.json['num6']

        return jsonify(str(a*b))

@app.route('/xyz/abc3', methods = ['GET', 'POST'])
def test3():
    if request.method == 'POST':
        a = request.json['name']
        b = request.json['title']

        return jsonify(str(a+b))

if __name__ == '__main__':
    app.run()
