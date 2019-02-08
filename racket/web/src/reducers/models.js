import _ from 'lodash'
import {LOAD_ACTIVE, LOAD_DATA, LOAD_MODEL_HISTORY, LOAD_SELECTED, SET_DATE_FILTERS} from "../constants/actionTypes";


export const loader = (state = {
    active_id: null,
    selected: {},
    models: [],
    model_history: [],
    start: null,
    end: null
}, action) => {
    switch (action.type) {
        case LOAD_SELECTED:
            return {...state, selected: action.payload};
        case LOAD_ACTIVE:
            return {...state, active_id: action.payload.model_id};
        case LOAD_DATA:
            return {...state, models: action.payload};
        case LOAD_MODEL_HISTORY:
            const keys = Object.keys(action.payload);
            const hist = keys.map(k => (action.payload[k].map(v => ({[k]: Number(v.toFixed(4))}))));
            const merger = (...args) => args.reduce((arg, arg1) => ({...arg, ...arg1}));
            const merged = _.zipWith(...hist, merger);
            const final = merged.map((i, m) => ({...i, name: `Epoch: ${m+1}`}));
            return {...state, model_history: final, keys: keys};
        case SET_DATE_FILTERS:
            return {...state, start: action.payload.start, end: action.payload.end};

        default:
            return {
                ...state
            }
    }
};
