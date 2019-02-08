import {combineReducers} from 'redux';
import {loader} from './models';
import {header} from './layout';

export default combineReducers({
    loader,
    header,
});
