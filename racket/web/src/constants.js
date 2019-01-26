import * as types from './constants'

const API_URL = 'http://localhost:8000/api/v1';


export const endpoint = (kind) => {
    switch (kind) {
        case types.ALIGHTINGS:
            return API_URL + '/info/' + types.ALIGHTINGS;
        case types.BOARDINGS:
            return API_URL + '/info/' + types.BOARDINGS;
        case types.STOPS:
            return API_URL + '/info/' + types.STOPS;
        case types.ROUTES:
            return API_URL + '/info/' + types.ROUTES;
    }
};


export const shuffleArray = (array) => {
    for (let i = array.length - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        let temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    return array
};
