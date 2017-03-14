from flask import Flask, render_template, request
import search_keyword

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
	query = request.form['query']
	result=search_keyword.search(query)
	return render_template("result.html",result=result)
	#return "hello from the other side"

if __name__ == '__main__':
	app.run(debug = True)