const express = require('express');
const app = express();

const port = process.env.PORT || 3001;

app.get('/', (req, res) => {
    res.send({'message': 'Hello World!'});
    });

app.get('/ping', (req, res) => {
    res.send({'message': 'pong'});
    });
    
function sleep(duration) {
    setTimeout(function () {}, duration);
    //return new Promise(resolve => setTimeout(resolve, duration));
    }

app.get('/test', (req, res) => {
    const steps = parseInt(req.query.steps) || 2;
    let duration = 0;
    for (let i = 1; i <= steps; i++) {
        console.log(`Step #${i}; sleeping...`);
        r = Math.random() * 10000;
        duration += r;
        sleep(r);
    }
    let status = Math.random() < 0.75;
    if (status) {
        return res.status(200).json({'duration': parseInt(duration/1000), 'status': 'success'});
    }else{
        return res.status(500).json({'duration': parseInt(duration/1000), 'status': 'failure'});
    }
});

app.get('/ping'), (req, res) => {
    res.send({'message': 'pong'});
    };

app.listen(port, () => {
    console.log(`Server is up on port ${port}`);
});