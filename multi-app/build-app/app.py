import logging
import random
import time

from flask import Flask

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

def random_status():
    return random.choice([ True for i in range(8) ] + [False])

def take_a_nap():
    nap_time = random.randint(1, 3)
    logger.info(f'Sleeping for {nap_time} seconds')
    time.sleep(nap_time)
    return nap_time

def do_step(i: int):
    logger.info(f'Doing step: {i}')
    status = random_status()
    logger.info(f'>>> Status: {status}')
    return status

@app.route('/')
@app.route('/ping')
def ping():
    return {'status': 'pong'}

@app.route('/build')
def do_build(steps: int = 3):
    duration = 0
    results = []
    for step in range(steps):
        duration += take_a_nap()
        results.append(do_step(step+1))        
    # for
    if all(results):
        return {'status': 'success', 'duration': duration}
    else:
        return {'status': 'failure', 'results': results, 'duration': duration}, 500
    
if __name__ == '__main__':
    port = 5001
    logger.debug(f'Starting app on port {port}')
    app.run(host='0.0.0.0', port=port, debug=True)