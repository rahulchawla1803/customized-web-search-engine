from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import query_module
import ranking_text_mining
import ranking_nlp
import auto_complete
import combined_ranking
import os


result_list=auto_complete.auto()
result_str=','.join(result_list)


app = Flask(__name__)
CORS(app)
@app.route('/', methods=['POST'])
def index():
	query = request.form['query']
	a, b, c=query_module.query_structure(query)
	result_tm=ranking_text_mining.ranking(a, b, c)
	result_nlp, ngram_considered=ranking_nlp.rank_ngram(query)
	result, result_score=combined_ranking.ranking(result_tm,result_nlp)

	return render_template("result.html",result=result)

@app.route('/analysis', methods=['GET', 'POST'])
def analyze():
	query = request.form['query']
	a, b, c = query_module.query_structure(query)
	clean_query_root = a
	query_synonym_root = b
	query_suggestion_root = c
	query_analyse = query
	result_tm = ranking_text_mining.ranking(a, b, c)
	result_nlp, ngram_considered = ranking_nlp.rank_ngram(query)
	result, result_score = combined_ranking.ranking(result_tm, result_nlp)
	result_analyse = result
	result_score_analyse = result_score
	score=[]
	query_synonym_root=list(set(query_synonym_root))
	query_suggestion_root=list(set(query_suggestion_root))

	for key, value in result_score_analyse.items():
		value=round(value,4)
		result_score_analyse[key]=value
		score.append(value)


	return render_template("analysis.html",
						   query=query_analyse,
						   query_root=clean_query_root,
						   synonym=query_synonym_root,
						   suggestion=query_suggestion_root,
						   result_title=result_analyse,
						   result_score=result_score_analyse,
						   score=score,
						   ngram=ngram_considered)



@app.route('/autocomplete', methods=['GET'])
def auto():
	#print("Reached server")
	return result_str


if __name__ == '__main__':
	app.run(host=os.getenv('LISTEN', '0.0.0.0'), port=int(os.getenv('PORT', '5000')), debug = True)