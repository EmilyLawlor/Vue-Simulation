from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sse import sse


from Simulation.rdt3_0.main import run as run_StopAndWait
from Simulation.GBN.main import run as run_GoBackN
from Simulation.SR.main import run as run_SelectiveRepeat
from Simulation.rdt2_2.main import run as run_rdt2_2
from Simulation.rdt2_1.main import run as run_rdt2_1
from Simulation.rdt2_0.main import run as run_rdt2_0
from Simulation.rdt1_0.main import run as run_rdt1_0

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config["REDIS_URL"] = "redis://localhost:6379"
app.register_blueprint(sse, url_prefix='/stream')

CORS(app)


@app.route('/stop-and-wait', methods=['GET'])
def stop_and_wait():
    runTimeSeconds = float(request.args['runTime']) * 60
    run_StopAndWait(runTimeSeconds, int(request.args['errorRate']), int(request.args['lossRate']))
    return jsonify( {'protocol':'stop and wait'})


@app.route('/go-back-n', methods=['GET'])
def go_back_n():
    runTimeSeconds = float(request.args['runTime']) * 60
    run_GoBackN(runTimeSeconds, int(request.args['errorRate']), int(request.args['lossRate']), int(request.args['windowSize']))
    return jsonify( {'protocol':'go back n'} )


@app.route('/selective-repeat', methods=['GET'])
def selective_repeat():
    runTimeSeconds = float(request.args['runTime']) * 60
    run_SelectiveRepeat(runTimeSeconds, int(request.args['errorRate']), int(request.args['lossRate']), int(request.args['windowSize']))
    return jsonify( {'protocol':'selective repeat'})


@app.route('/others', methods=['GET'])
def others():
    protocol = request.args['protocol']
    runTimeSeconds = float(request.args['runTime']) * 60

    if protocol == 'rdt2.2':
        run_rdt2_2(runTimeSeconds, int(request.args['errorRate']))
    elif protocol == 'rdt2.1':
        run_rdt2_1(runTimeSeconds, int(request.args['errorRate']))
    elif protocol == 'rdt2.0':
        run_rdt2_0(runTimeSeconds, int(request.args['errorRate']))
    else:
        run_rdt1_0(runTimeSeconds)
    
    return jsonify( {'protocol': protocol})


if __name__ == '__main__':
    app.run()
