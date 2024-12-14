import http from 'k6/http';
import { sleep, check } from 'k6';
import { FormData } from 'https://jslib.k6.io/formdata/0.0.2/index.js';


// Setting the base URL
const API_BASE_URL = 'http://192.168.0.105:8079';

export let options = {
    stages: [
        { duration: '5m', target: 100 }, // ramp up to 100 users over 5 minutes
        { duration: '10m', target: 100 }, // stay at 100 users for 10 minutes
        { duration: '10m', target: 200 }, // ramp up to 200 users for 10 minutes
        { duration: '5m', target: 0 }, // ramp down to 0 users over 5 minutes
    ]
};

let file = open('messi-main.jpeg', 'b');

export default function () {
    const fd = new FormData();

    fd.append('file', http.file(file, 'messi-main.jpeg', 'image/jpeg'));

    const res = http.post(`${API_BASE_URL}/upload`, fd.body(), {
        headers: { 'Content-Type': 'multipart/form-data; boundary=' + fd.boundary },
    });

    check(res, {
        'is status 200': (r) => r.status === 200,
    });

    sleep(1);
}
