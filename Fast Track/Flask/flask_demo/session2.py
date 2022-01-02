from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/via_postman', methods=['POST']) # for calling the API from Postman/SOAPUI
def math_operation_via_postman():
    if (request.method=='POST'):
        operation=request.json['operation']
        num1=int(request.json['num1'])
        num2 = int(request.json['num2'])
        if(operation=='add'):
            r=num1+num2
            result= 'the sum of '+str(num1)+' and '+str(num2) +' is '+str(r)
        if (operation == 'subtract'):
            r = num1 - num2
            result = 'the difference of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(r)
        if (operation == 'multiply'):
            r = num1 * num2
            result = 'the product of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(r)
        if (operation == 'divide'):
            r = num1 / num2
            result = 'the quotient when ' + str(num1) + ' is divided by ' + str(num2) + ' is ' + str(r)
        return jsonify(result)

@app.route('/route1', methods=['POST']) # for calling the API from Postman/SOAPUI
def route1():
    if request.method == 'POST':
        return jsonify("inside /route1")

@app.route('/test_url') # for calling the API from Postman/SOAPUI
def test_url1():
    # http://127.0.0.1:5000/test_url?val1=2&val2=6
    test1 = request.args.get('val1')
    test2 = request.args.get('val2')

    return '''<h1>Result is: {}</h1>'''.format(int(test1) + int(test2))

if __name__ == '__main__':
    app.run()
