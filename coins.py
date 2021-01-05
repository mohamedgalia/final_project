# from flask import Flask, render_template, Response, url_for
# import requests
# import time
#
# app = Flask(__name__)
#
# # @app.route('/')
# # def hello():
# #     while True:
# #         r = requests.get("https://bitpay.com/api/rates")
# #         try:
# #             data = r.json()
# #             val1 = str(data[2]["rate"])
# #             print(val1)
# #             return render_template("index.html", val = val1, val2= val1)
# #         except ValueError:
# #             print("Response content is not valid JSON")
#
# @app.route('/')
# def index():
#     return render_template("index.html")
#
#
# @app.route('/update_price')
# def update_price():
#     def gen():
#         r = requests.get("https://bitpay.com/api/rates")
#         try:
#             data = r.json()
#             val1 = str(data[2]["rate"])
#             yield (val1)
#         except ValueError:
#             print("Response content is not valid JSON")
#     return Response(gen(), mimetype='text')
#
# @app.route('/update_price_avg')
# def update_price_avg():
#     def gen1():
#         val_list = []
#         t_end = time.time() + 60
#         while time.time() < t_end:
#             r = requests.get("https://bitpay.com/api/rates")
#             try:
#                 data = r.json()
#                 val_list.append(float(str(data[2]["rate"])))
#             except ValueError:
#                 print("Response content is not valid JSON")
#         yield str((sum(val_list) / len(val_list)))
#
#     return Response(gen1(), mimetype='text')
#
# if __name__ == '__main__':
#     app.run(host = "0.0.0.0")

from flask import Flask, render_template, request
import requests

api_key = "85aa5a4fb3533fbae7223f74ccb1befb"
url = "http://data.fixer.io/api/latest?access_key=" + api_key

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        fistCurrency = request.form.get("firstCurrency")
        secondCurrency = request.form.get("secondCurrency")
        amount = request.form.get("amount")
        response = requests.get(url)
        app.logger.info(response)
        infos = response.json()
        firstValue = infos["rates"][fistCurrency]
        secondValue = infos["rates"][secondCurrency]
        result = (secondValue / firstValue) * float(amount)
        currencyInfo = dict()
        currencyInfo["firstCurrency"] = fistCurrency
        currencyInfo["secondCurrency"] = secondCurrency
        currencyInfo["amount"] = amount
        currencyInfo["result"] = result
        return render_template("index2.html", info=currencyInfo)
    else:
        return render_template("index2.html")


if __name__ == "__main__":
    app.run(host = "0.0.0.0")
