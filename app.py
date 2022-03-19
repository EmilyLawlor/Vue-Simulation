from flask import Flask, jsonify, Response, request
from flask_cors import CORS
from flask_sse import sse
import datetime
import redis
import time


from Simulation.rdt3_0.main import Start as StopAndWait
from Simulation.GBN.main import Start as GoBackN
from Simulation.SR.main import Start as SelectiveRepeat

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config["REDIS_URL"] = "redis://localhost:1111"
app.register_blueprint(sse, url_prefix='/stream')

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/stop-and-wait', methods=['GET'])
def stop_and_wait():
    runTimeSeconds = int(request.args['runTime']) * 60
    StopAndWait().run(runTimeSeconds, int(request.args['errorRate']), int(request.args['lossRate']))
    return jsonify( {'protocol':'stop and wait'})


@app.route('/go-back-n', methods=['GET'])
def go_back_n():
    runTimeSeconds = int(request.args['runTime']) * 60
    GoBackN().run(runTimeSeconds, int(request.args['errorRate']), int(request.args['lossRate']), int(request.args['windowSize']))
    return jsonify( {'protocol':'go back n'} )


@app.route('/selective-repeat', methods=['GET'])
def selective_repeat():
    runTimeSeconds = int(request.args['runTime']) * 60
    SelectiveRepeat().run(runTimeSeconds, int(request.args['errorRate']), int(request.args['lossRate']), int(request.args['windowSize']))
    return jsonify( {'protocol':'selective repeat'})


if __name__ == '__main__':
   app.run()
