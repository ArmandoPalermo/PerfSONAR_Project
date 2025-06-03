import mysql.connector
import json
from datetime import datetime

def loadTestToDB(json_data):
    # Connessione al database MySQL
    conn = mysql.connector.connect(
        host="localhost",  # Cambia con il tuo host
        user="admin",        # Cambia con il tuo username
        password="monitorIns123456",  # Cambia con la tua password
        database="perfsonarDB"
    )

    cursor = conn.cursor()


    # Estrazione dei dati principali
    test_id = json_data["id"]
    added = datetime.fromisoformat(json_data["run"]["added"].replace("Z", "+00:00"))
    state = json_data["run"]["state"]
    start_time = datetime.fromisoformat(json_data["run"]["start-time"].replace("Z", "+00:00"))
    end_time = datetime.fromisoformat(json_data["run"]["end-time"].replace("Z", "+00:00"))

    source_ip = json_data["test"]["spec"]["source"]
    dest_ip = json_data["test"]["spec"]["dest"]
    packet_count = json_data["test"]["spec"]["count"]
    packet_size = json_data["test"]["spec"]["length"]
    intervallo = json_data["test"]["spec"]["interval"]

    result_max = float(json_data["run"]["result-full"][0]["result"]["max"].replace("PT", "").replace("S", ""))
    result_min = float(json_data["run"]["result-full"][0]["result"]["min"].replace("PT", "").replace("S", ""))
    result_mean = float(json_data["run"]["result-full"][0]["result"]["mean"].replace("PT", "").replace("S", ""))
    result_stddev = float(json_data["run"]["result-full"][0]["result"]["stddev"].replace("PT", "").replace("S", ""))

    packets_sent = json_data["run"]["result-full"][0]["result"]["sent"]
    packets_received = json_data["run"]["result-full"][0]["result"]["received"]
    packets_lost = json_data["run"]["result-full"][0]["result"]["lost"]

    # Inserimento dei dati nella tabella rtt_tests
    insert_test = """
    INSERT INTO rtt_tests (
        id, added, source_ip, dest_ip, packet_count, packet_size, intervallo,
        result_max, result_min, result_mean, result_stddev,
        packets_sent, packets_received, packets_lost, state, start_time, end_time
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor.execute(insert_test, (
        test_id, added, source_ip, dest_ip, packet_count, packet_size, intervallo,
        result_max, result_min, result_mean, result_stddev,
        packets_sent, packets_received, packets_lost, state, start_time, end_time
    ))

    # Inserimento dei dati nella tabella rtt_roundtrips
    insert_roundtrip = """
    INSERT INTO rtt_roundtrips (test_id, ip, rtt, seq, ttl, packet_length)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for roundtrip in json_data["run"]["result-full"][0]["result"]["roundtrips"]:
        cursor.execute(insert_roundtrip, (
            test_id,
            roundtrip["ip"],
            float(roundtrip["rtt"].replace("PT", "").replace("S", "")),
            roundtrip["seq"],
            roundtrip["ttl"],
            roundtrip["length"]
        ))

    # Commit delle modifiche e chiusura della connessione
    conn.commit()
    cursor.close()
    conn.close()

