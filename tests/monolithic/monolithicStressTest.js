import http from 'k6/http'
import { sleep } from 'k6'

export let options = {
    insecureSkipTLSVerify: true,
    noConnectionReuse: false,
    stages: [
        { duration: '1m', target: 10 }, // below normal load
        { duration: '2m', target: 10 },
        { duration: '1m', target: 20 }, // normal load
        { duration: '2m', target: 20 },
        { duration: '1m', target: 30 }, // around the breaking point
        { duration: '2m', target: 30 },
        { duration: '1m', target: 40 }, // beyond the breaking point
        { duration: '2m', target: 40 },
        { duration: '3m', target: 0 } // scale down. Recovery stage. 
    ]
}

const API_BASE_URL = 'http://127.0.0.1:5001'

export default () => {
    http.batch([
        ['GET', `${API_BASE_URL}/movies`]
    ])
    sleep(1)
}