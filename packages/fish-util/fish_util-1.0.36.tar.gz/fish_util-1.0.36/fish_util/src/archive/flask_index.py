from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['JSONIFY_TIMEOUT'] = 30

@app.route('/search', methods=['GET'])
def search():
   keyword = request.args.get('keyword',"")
   print(f"search keyword: {keyword}")
   return jsonify(keyword)

if __name__ == '__main__':
    app.run(debug=True,port=5001)