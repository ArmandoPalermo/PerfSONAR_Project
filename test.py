from flask import Flask
from flask import request,jsonify
import json
import pythonScriptThroughput as throughputHandler
import pythonScriptLatency as latencyHandler
import pythonScriptRtt as rttHandler
app = Flask(__name__)

@app.post("/ThroughputTests")
def handle_ThroughputTests():
	data = request.json
	if not data:
		return jsonify({"error":"Invalid JSON"}), 400
	throughputHandler.loadTestToDB(request.json)
	return jsonify({"result":"Funzione Eseguita"}),200


@app.post("/LatencyTests")
def handle_LatencyTests():
	data = request.json
	if not data:
		return jsonify({"error":"Invalid JSON"}), 400
	latencyHandler.loadTestToDB(request.json)
	return jsonify({"result":"Funzione Eseguita"}),200


@app.post("/rttTests")
def handle_rttTests():
	data = request.json
	if not data:
		return jsonify({"error":"Invalid JSON"}), 400
	rttHandler.loadTestToDB(request.json)
	return jsonify({"result":"Funzione Eseguita"}),200
