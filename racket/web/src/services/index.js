import {loadActive, loadData, loadModelHistory, loadSelected} from "../actions";

const API_URL = 'http://localhost:8000/api/v1';

export const fetchModels = () => async (dispatch) => {
    return fetch(API_URL + '/model/all')
        .then(
            body => body.json())
        .then(r => {
                dispatch(loadData(r));
                return {...r, status: 200}
            }
        )
        .catch(error => error)

};

export const fetchActive = () => async (dispatch) => {
    return fetch(API_URL + '/model/active')
        .then(
            body => body.json())
        .then(r => {
                dispatch(loadActive(r));
                return {...r, status: 200}
            }
        )
        .catch(error => error)

};


export const fetchSelected = (model_id) => async (dispatch) => {
    return fetch(API_URL + `/model/all?model_id=${model_id}`)
        .then(
            body => body.json())
        .then(r => {
                dispatch(loadSelected(r));
                return {...r, status: 200}
            }
        )
        .catch(error => error)

};

export const fetchModelHistory = (model_id) => async (dispatch) => {
    return fetch(API_URL + '/model/historic?model_id=' + model_id.toString(), {})

        .then(
            body => body.json())
        .then(r => {
            dispatch(loadModelHistory(r));
            return {...r, status: 200}
        }).catch(error => error)

};

