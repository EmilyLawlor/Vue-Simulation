from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sse import sse


from Simulation.rdt3_0.main import Start as StopAndWait
from Simulation.GBN.main import Start as GoBackN
from Simulation.SR.main import Start as SelectiveRepeat
from Simulation.rdt2_2.main import Start as rdt2_2
from Simulation.rdt2_1.main import Start as rdt2_1
from Simulation.rdt2_0.main import Start as rdt2_0
from Simulation.rdt1_0.main import Start as rdt1_0

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config["REDIS_URL"] = "redis://localhost:1111"
app.register_blueprint(sse, url_prefix='/stream')

CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/stop-and-wait', methods=['GET'])
def stop_and_wait():
    runTimeSeconds = float(request.args['runTime']) * 60
    StopAndWait().run(runTimeSeconds, int(request.args['errorRate']), int(request.args['lossRate']))
    return jsonify( {'protocol':'stop and wait'})


@app.route('/go-back-n', methods=['GET'])
def go_back_n():
    runTimeSeconds = float(request.args['runTime']) * 60
    GoBackN().run(runTimeSeconds, int(request.args['errorRate']), int(request.args['lossRate']), int(request.args['windowSize']))
    return jsonify( {'protocol':'go back n'} )


@app.route('/selective-repeat', methods=['GET'])
def selective_repeat():
    runTimeSeconds = float(request.args['runTime']) * 60
    SelectiveRepeat().run(runTimeSeconds, int(request.args['errorRate']), int(request.args['lossRate']), int(request.args['windowSize']))
    return jsonify( {'protocol':'selective repeat'})


@app.route('/others', methods=['GET'])
def others():
    protocol = request.args['protocol']
    runTimeSeconds = float(request.args['runTime']) * 60

    if protocol == 'rdt2.2':
        rdt2_2().run(runTimeSeconds, int(request.args['errorRate']))
    elif protocol == 'rdt2.1':
        rdt2_1().run(runTimeSeconds, int(request.args['errorRate']))
    elif protocol == 'rdt2.0':
        rdt2_0().run(runTimeSeconds, int(request.args['errorRate']))
    else:
        rdt1_0().run(runTimeSeconds)
    
    return jsonify( {'protocol': protocol})


if __name__ == '__main__':
    app.run()
