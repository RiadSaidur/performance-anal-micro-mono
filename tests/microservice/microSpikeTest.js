import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
    stages: [
        { duration: '10s', target: 100 }, // below normal load
        { duration: '1m', target: 100 },
        { duration: '10s', target: 1000 }, // spike to 1000 users
        { duration: '3m', target: 1000 }, // stay at spike
        { duration: '10s', target: 100 }, // scale down to normal traffic
        { duration: '1m', target: 100 },
        { duration: '10s', target: 0 },
    ],
};

const API_BASE_URL = 'http://127.0.0.1:5000'

export default function () {
    ['GET', `${API_BASE_URL}/movies`]
    sleep(1);
}
