import {COLLAPSE_HEADER} from "../constants/actionTypes";


export const header = (state = {collapsed: false}, action) => {
    switch (action.type) {
        case COLLAPSE_HEADER:
            return {collapsed: !state.collapsed};
        default:
            return {
                ...state
            }
    }
};
