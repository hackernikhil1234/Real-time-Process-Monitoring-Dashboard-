
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import psutil

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('os.html')  # This looks inside templates/os.html

@app.route('/system')
def system_info():
    return jsonify({
        'cpu': psutil.cpu_percent(interval=0.5),
        'memory': psutil.virtual_memory().percent
    })

@app.route('/processes')
def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except psutil.NoSuchProcess:
            continue
    return jsonify(processes)

@app.route('/kill/<int:pid>', methods=['DELETE'])
def kill_process(pid):
    try:
        psutil.Process(pid).terminate()
        return jsonify({'message': f'Process {pid} terminated.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
