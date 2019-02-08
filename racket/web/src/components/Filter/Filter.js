/* global document */
import React, {PureComponent} from 'react'
import PropTypes from 'prop-types'
import {Col, DatePicker, Form, Row} from 'antd'
import {setDateFilters} from "../../actions";
import {connect} from 'react-redux'

const {RangePicker} = DatePicker;

const ColProps = {
    xs: 24,
    sm: 12,
    style: {
        marginBottom: 16,
    },
};

const TwoColProps = {
    ...ColProps,
    xl: 96,
};

class Filter extends PureComponent {
    onChange = (date) => {
        console.log(date);
        this.props.setFilter({start: date[0], end: date[1]})
    };

    render() {
        return (
            <Row gutter={24}>
                <Col
                    {...ColProps}
                    xl={{span: 6}}
                    md={{span: 8}}
                    sm={{span: 12}}
                    id="createTimeRangePicker"
                >
                    <RangePicker
                        style={{width: '100%'}}
                        onChange={this.onChange}
                        getCalendarContainer={() => {
                            return document.getElementById('createTimeRangePicker')
                        }}
                    />
                </Col>

                <Col
                    {...TwoColProps}
                    xl={{span: 10}}
                    md={{span: 24}}
                    sm={{span: 24}}
                >
                </Col>
            </Row>
        )
    }
}

Filter.propTypes = {
    onAdd: PropTypes.func,
    form: PropTypes.object,
    filter: PropTypes.object,
    onFilterChange: PropTypes.func,
};


const mapDispatchToProps = (dispatch) => {
    return ({
        setFilter: (payload) => dispatch(setDateFilters(payload)),
    })
};


const mapStateToProps = () => {
    return {}

};


const WrappedFilter = connect(mapStateToProps, mapDispatchToProps)(Form.create({name: 'filter_stuff'})(Filter));
export default WrappedFilter
