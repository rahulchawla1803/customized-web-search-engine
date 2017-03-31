from flask import Flask, render_template, request
import search_ranking_title_IR2

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
	query = request.form['query']
	result=search_ranking_title_IR2.search(query)
	return render_template("result.html",result=result)

if __name__ == '__main__':
	app.run(debug = True)