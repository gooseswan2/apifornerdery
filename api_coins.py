import flask
import requests
from flask import request, json, jsonify, render_template
from collections import OrderedDict
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return render_template('api_coins.html', x=True)

@app.route('/api/v1/coins', methods=['GET'])
def api_coins():
    coinDictionary=OrderedDict()
   
    if request.args['amount']:
        amount=request.args['amount']
        for x in amount:
            if x.isalpha():
                return render_template('api_coins.html', mess="Enter monetary amount", x=True)
        
        total=request.args['amount'].lstrip("$").split(".")
        if total[0]=='':
            coinDictionary['silver-dollar']=0
        else:
            coinDictionary['silver-dollar']=int(total[0])
        cents=int(total[1])
        if cents>=50:
            coinDictionary['half-dollar']=1
            cents=cents-50
        else:
            coinDictionary['half-dollar']=0
        if cents>=25:
            coinDictionary['quarter']=1
            cents=cents-25
        else:
            coinDictionary['quarter']=0
        if cents>=10:
            dimes=cents//10
            coinDictionary['dime']=dimes
            cents=cents-10*dimes
        else:
            coinDictionary['dime']=0
        if cents>=5:
            coinDictionary['nickel']=1
            cents=cents-5
        else:
            coinDictionary['nickel']=0
        if cents>0:
            coinDictionary['penny']=cents
        else:
            coinDictionary['penny']=0
    else:
        return render_template('api_coins.html', mess="No value was entered.", x=True)
    return jsonify(coinDictionary)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()
