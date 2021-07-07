
import os
import ast

from flask import Flask, jsonify, make_response, request, abort, render_template
from flask_cors import CORS, cross_origin

from ag_segments import AG_segments
from ag_segments_coop import AG_segments_coop
import maquinaEstados
from maquinaEstados import MaquinaEstados
from kmeans import Kmeans
from nmean import Nmean

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True



@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'Error':'Bad Request'}), 400)



@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error':'Not Found'}), 404)



@app.errorhandler(405)
def not_found(error):
	return make_response(jsonify({'error':'Method Not Allowed'}), 405)



def get_params_ag(json):
	params = {}
	if 'pop_size' in json:
		params['pop_size'] = json['pop_size']
	if 'ngen' in json:
		params['ngen'] = json['ngen']
	if 'nespecies' in request.json:
		params['nespecies'] = json['nespecies']
	if 'ngen_intercambio' in json:
		params['ngen_intercambio'] = json['ngen_intercambio']
	if 'cxpb' in json:
		params['cxpb'] = json['cxpb']
	if 'mutpb' in json:
		params['mutpb'] = json['mutpb']
	if 'batch_evaluate' in json:
		params['batch_evaluate'] = json['batch_evaluate']
	if 'batch_size' in json:
		params['batch_size'] = json['batch_size']

	return params



def get_params_kmeans(json):
	params = {}
	if 'k' in json:
		params['k'] = json['k']
	if 'n_init' in json:
		params['n_init'] = json['n_init']
	if 'max_it' in json:
		params['max_it'] = json['max_it']
	if 'params_ag' in json:
		params['params_ag'] = get_params_ag(json['params_ag'])

	return params



def execute_kmeans(ag):
	if not request.json or not 'series' in request.json:
		abort(400)

	series = request.json['series']

	params = get_params_kmeans(request.json)
	params['ag'] = ag

	KM = Kmeans(**params)
	y = KM.fit_predict(series).tolist()
	intertia = KM.inertia

	return y, intertia



def execute_nmean_crisp(ag):
	if not request.json or not 'series' in request.json or not 'centroides' in request.json:
		abort(400)

	series = request.json['series']
	centroides = request.json['centroides']

	params = {}
	params['ag'] = ag
	if 'params_ag' in request.json:
		params['params_ag'] = get_params_ag(request.json['params_ag'])

	NM = Nmean(**params)
	y = NM.pretrained_predict(centroides, series).tolist()

	return y



def execute_nmean_fuzzy(ag):
	if not request.json or not 'series' in request.json or not 'centroides' in request.json:
		abort(400)

	series = request.json['series']
	centroides = request.json['centroides']

	params = {}
	params['ag'] = ag
	if 'params_ag' in request.json:
		params['params_ag'] = get_params_ag(request.json['params_ag'])

	NM = Nmean(**params)
	y = NM.pretrained_fuzzy_predict(centroides, series).tolist()

	return y



@app.route('/frontend', methods=['POST'])
def calcula_estado():
	if not request.json or not 'series' in request.json or not 'poblacion' in request.json:
		abort(400)

	series = request.json['series']
	poblacion = request.json['poblacion']

	if 'cxpb' in request.json:
		cxpb = float(request.json['cxpb'])
	else:
		cxpb = 0.2
	if 'mutpb' in request.json:
		mutpb = float(request.json['mutpb'])
	else:
		mutpb = 0.1
	if 'batch_size' in request.json:
		batch_size = float(request.json['batch_size'])

	ME = MaquinaEstados(series, pop=poblacion, cxpb=cxpb, mutpb=mutpb, batch_size=batch_size)
	estado = ME.nextEstado()
	return make_response(jsonify(estado), 200)



@app.route('/centroide/simple', methods=['POST'])
def ag_segments_simple():
	if not request.json or not 'series' in request.json:
		abort(400)

	series = request.json['series']
	params = get_params_ag(request.json)

	AG = AG_segments(**params)
	C, fitness_mejor, log = AG.calculate_centroids(series)

	return make_response(jsonify({'centroide':C, 'fitness':fitness_mejor}), 200)



@app.route('/centroide/coop', methods=['POST'])
def ag_segments_coop():
	if not request.json or not 'series' in request.json:
		abort(400)

	series = request.json['series']
	params = get_params_ag(request.json)

	AG = AG_segments_coop(**params)
	C, fitness_mejor, log = AG.calculate_centroids(series)

	return make_response(jsonify({'centroide':C, 'fitness':fitness_mejor}), 200)



@app.route('/kmeans/simple', methods=['POST'])
def kmeans_simple():
	y, intertia = execute_kmeans('simple')
	return make_response(jsonify({'y':y, 'inertia':intertia}), 200)



@app.route('/kmeans/coop', methods=['POST'])
def kmeans_coop():
	y, intertia = execute_kmeans('coop')
	return make_response(jsonify({'y':y, 'inertia':intertia}), 200)



@app.route('/nmean/simple/crisp', methods=['POST'])
def nmean_simple_crisp():
	y = execute_nmean_crisp('simple')
	return make_response(jsonify({'y':y}), 200)



@app.route('/nmean/simple/fuzzy', methods=['POST'])
def nmean_simple_fuzzy():
	y = execute_nmean_fuzzy('simple')
	return make_response(jsonify({'y':y}), 200)



@app.route('/nmean/coop/crisp', methods=['POST'])
def nmean_coop_crisp():
	y = execute_nmean_crisp('coop')
	return make_response(jsonify({'y':y}), 200)



@app.route('/nmean/coop/fuzzy', methods=['POST'])
def nmean_coop_fuzzy():
	y = execute_nmean_fuzzy('coop')
	return make_response(jsonify({'y':y}), 200)


@app.route('/frontend')
def show_frontend():
	maquinaEstados.init_seeds()
	return render_template('cliente.html')



port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='127.0.0.1', port=int(port))
