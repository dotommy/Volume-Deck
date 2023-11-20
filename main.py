import functions
import volume
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import socket
import json
from winotify import Notification


app = Flask(__name__)
CORS(app)

def get_server_ip():
    try:
        # Creazione di un socket per ottenere l'indirizzo IP locale
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        server_ip = s.getsockname()[0]
        s.close()
        return server_ip
    except Exception as e:
        print(f"Errore durante il recupero dell'indirizzo IP del server: {e}")
        return None

@app.route('/')
def index():

    otp_code = functions.otp_generator()
    str_otp = str(otp_code)
    toast = Notification(app_id="Volume Deck",
                         title= "OTP:",
                        msg= str_otp
                     )
    toast.show()
    print('OTP: '+str(otp_code))

    functions.save_otp_in_json(otp_code)

    return render_template('index.html')



@app.route('/volume_deck', methods=['POST'])
def volume_deck():
    
    codice_otp_inviato = request.form.get('codice_otp')
    
    # Effettua la tua logica di verifica del codice OTP
    codice_otp_corretto = str(functions.read_otp_da_json())  # Sostituisci con il codice OTP corretto
    
    functions.remove_json()
    ip_local = get_server_ip()
    if codice_otp_inviato == codice_otp_corretto:
        return render_template('volume_deck.html', server_ip=ip_local)
    else:
        return render_template('verification_failure.html')


@app.route('/set_volume<id_process>', methods=['POST'])
def set_volume(id_process):
    try:
        dati_json = request.get_json()
        # Esegui le operazioni necessarie con il valore ricevuto dal client
        volume_now = dati_json.get('volume', 0)
        print("Valore del volume ricevuto:", volume)
        volume_function = int(volume_now)/100
        app_process = volume.name_process_audio()
        print(app_process)
        id_int = int(id_process)
        volume.volume_process_control(app_process[id_int], volume_function)
        risposta = {"messaggio": "Valore del volume ricevuto con successo"}
        return jsonify(risposta)

    except Exception as e:
        print("Errore durante l'elaborazione della richiesta:", str(e))
        risposta_errore = {"errore": "Si è verificato un errore durante l'elaborazione della richiesta"}
        return jsonify(risposta_errore), 500

@app.route('/get_process', methods=['GET'])
def get_process():
    try:
        process = volume.name_process_audio()
        if len(process) > 0:
            volume_process = []
            for proces in process:
                volume_proces = volume.get_volume_process(proces)
                percent_volume_proces = volume_proces*100
                volume_process.append(percent_volume_proces)
            response = {"process": process,
                        "volume_now": volume_process
                        }
            return jsonify(response)
        else:
             error = {
                "error": {
                    "code": 404,
                    "message": "empty array"
                }
                }
             return  json.dumps(error)
        
    except ValueError as e:
            print(f"Error: {e}")

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)