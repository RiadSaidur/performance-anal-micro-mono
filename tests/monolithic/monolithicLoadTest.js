import http from 'k6/http';
import { sleep, check } from 'k6';

// Setting the base URL
const API_BASE_URL = 'http://127.0.0.1:5001';

export let options = {
    stages: [
        { duration: '5m', target: 100 }, // ramp up to 100 users over 5 minutes
        { duration: '10m', target: 100 }, // stay at 100 users for 10 minutes
        { duration: '10m', target: 1000 }, // ramp up to 1000 users for 10 minutes
        { duration: '5m', target: 0 }, // ramp down to 0 users over 5 minutes
    ]
};

export default function () {
    const res = http.get(`${API_BASE_URL}/movies`);
    check(res, {
        'is status 200': (r) => r.status === 200,
        'body size is at least 500 bytes': (r) => r.body.length > 500,
    });
    sleep(1); // Think time between each request per VU
}
