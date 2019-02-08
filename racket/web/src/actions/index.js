import * as types from '../constants/actionTypes'

export const loadData = (payload) => ({type: types.LOAD_DATA, payload});
export const loadSelected = (payload) => ({type: types.LOAD_SELECTED, payload});
export const loadActive = (payload) => ({type: types.LOAD_ACTIVE, payload});
export const loadModelHistory = (payload) => ({type: types.LOAD_MODEL_HISTORY, payload});

export const setDateFilters = (payload) => ({type: types.SET_DATE_FILTERS, payload});

export const collapseHeader = () => ({type: types.COLLAPSE_HEADER});
