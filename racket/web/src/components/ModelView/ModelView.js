import React from 'react'
import PropTypes from 'prop-types'
import {Col, Row} from 'antd'
import Page from '../../components/Page/Page'
import {fetchModelHistory, fetchSelected} from "../../services";
import {connect} from 'react-redux'
import LineChartPage from "./Charts/Chart";
import Model from "./Model/Model";


class ModelView extends React.Component {

    componentDidMount() {
        this.props.loadHistory(this.props.model_id);
        this.props.loadSelectedModel(this.props.model_id);
    }

    componentWillMount() {
    }

    render() {
        const colProps = {
            lg: 12,
            md: 24,
        };

        return (
            <Page inner>
                <div className="content-inner">
                    <Row gutter={32}>
                        <Col {...colProps}>
                            <Model/>
                        </Col>
                        <Col {...colProps}>
                            <LineChartPage data={this.props.history}/>
                        </Col>
                    </Row>
                </div>
            </Page>
        );
    }
}


const mapDispatchToProps = (dispatch) => {
    return ({
        loadHistory: (model_id) => dispatch(fetchModelHistory(model_id)),
        loadSelectedModel: (model_id) => dispatch(fetchSelected(model_id))
    })
};


const mapStateToProps = (state) => {
    return {
        selected: state.loader.selected,
        active: state.loader.active_id,
        chartKeys: state.loader.keys,
        history: state.loader.model_history
    }

};


ModelView.propTypes = {
    model_id: PropTypes.number
};

export default connect(mapStateToProps, mapDispatchToProps)(ModelView);



