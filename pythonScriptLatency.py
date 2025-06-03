import json
import mysql.connector
from os import listdir
from datetime import datetime


def loadTestToDB(json_data):
	# Dati di connessione MySQL
	db = mysql.connector.connect(
	    host="localhost",
	    user="admin",
	    password="monitorIns123456",
	    database="perfsonarDB"
	)

	cursor = db.cursor()
	
	#Inserimento dati generali
	id = json_data["id"]
	source = json_data["test"]["spec"]["source"]
	dest = json_data["test"]["spec"]["dest"]
	end_time = json_data["run"]["end-time"]
	start_time = json_data["run"]["start-time"]	
	packets_sent = json_data["run"]["result-merged"]["packets-sent"]
	packets_lost = json_data["run"]["result-merged"]["packets-lost"]
	packets_received = json_data["run"]["result-merged"]["packets-received"]
	packets_reordered = json_data["run"]["result-merged"]["packets-reordered"]
	packets_duplicated = json_data["run"]["result-merged"]["packets-duplicated"]
	max_clock_error = json_data["run"]["result-merged"]["max-clock-error"]


	insert_measurement = """
	INSERT INTO latency_measurements (id, source_ip, destination_ip ,end_time, start_time, packets_sent,packets_lost, packets_received, packets_reordered, packets_duplicated, max_clock_error)
	VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)
	"""
	cursor.execute(insert_measurement, (id, source, dest ,end_time, start_time, packets_sent,packets_lost, packets_received, packets_reordered, packets_duplicated, max_clock_error))

	# Inserire i dati della misusurazione
	for latency, freq in json_data["run"]["result-merged"]["histogram-latency"].items():
	    query = """
	    INSERT INTO latency_histogram (measurement_id,latency, numPacket)
	    VALUES (%s, %s, %s)
	    """
	    values = (id,float(latency), freq)
	    cursor.execute(query, values)

	db.commit()
	cursor.close()
	db.close()
