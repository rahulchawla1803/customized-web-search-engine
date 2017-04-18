from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import query_module
import ranking_text_mining
import ranking_nlp
import auto_complete

print("server START")
result_list=auto_complete.auto()
#print(len(result_list))
result_str=','.join(result_list)
#print(result_str)
#print(len(result_str))

app = Flask(__name__)
CORS(app)
@app.route('/', methods=['POST'])
def index():
	query = request.form['query']
	a, b, c=query_module.query_structure(query)
	result=ranking_text_mining.ranking(a, b, c)
	temp_result=ranking_nlp.rank_ngram(query)
	print(temp_result)
	#result = ranking_text_mining.ranking(query_module.query_structure(query))

	return render_template("result.html",result=result)

@app.route('/analysis', methods=['POST'])
def analyze():
	query = request.form['query']
	clean_query_root, query_synonym_root, query_suggestion_root = query_module.query_structure(query)


	return render_template("analysis.html",query=query)


@app.route('/ana', methods=['GET'])
def ana():
	return render_template("ana.html", result="hello")

@app.route('/autocomplete', methods=['GET'])
def auto():
	print("Reached server")
	return result_str


if __name__ == '__main__':
	app.run("0.0.0.0",debug = True)