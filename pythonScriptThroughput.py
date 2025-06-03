import mysql.connector
import json
from os import listdir
from datetime import datetime

def loadTestToDB(json_data):
    # Connessione al database MySQL
    conn = mysql.connector.connect(
        host="localhost",  # Cambia con l'host del tuo database
        user="admin",       # Cambia con il tuo username
        password="monitorIns123456",  # Cambia con la tua password
        database="perfsonarDB"
    )

    cursor = conn.cursor()

    # Trasformare il dizionario in una stringa JSON
    #json_string = json.dumps(JsonFile, indent=4)  # Usa indent=4 per una stringa formattata
    #json_data = json.loads(JsonFile)

    # Estrazione dei dati principali
    print(json_data["run"]["added"])
    added = datetime.fromisoformat(json_data["run"]["added"].replace("Z", "+00:00"))
    state = json_data["run"]["state"]
    end_time = json_data["run"]["end-time"]
    start_time = json_data["run"]["start-time"]

    # Inserimento dei dati nella tabella measurements
    insert_measurement = """
    INSERT INTO measurements_throughput (added, state, end_time, start_time)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_measurement, (added, state, end_time, start_time))
    measurement_id = cursor.lastrowid

    # Estrazione e inserimento dei dati degli intervalli
    for interval in json_data["run"]["result-full"][0]["intervals"]:
        for stream in interval["streams"]:
            # Accedi ai dati di stream qui
            tcp_window_size = stream["tcp-window-size"]
            end_time = stream["end"]
            rtt = stream["rtt"]
            start_time = stream["start"]
            stream_id = stream["stream-id"]
            retransmits = stream["retransmits"]
            throughput_bits = stream["throughput-bits"]
            throughput_bytes = stream["throughput-bytes"]

            insert_interval = """
            INSERT INTO intervals_throughput (measurement_id, end_time, rtt, start_time, stream_id, retransmits, tcp_window_size, throughput_bits, throughput_bytes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_interval, (measurement_id, end_time, rtt, start_time, stream_id, retransmits, tcp_window_size, throughput_bits, throughput_bytes))

    # Commit delle modifiche e chiusura della connessione
    conn.commit()
    cursor.close()
    conn.close()
    
