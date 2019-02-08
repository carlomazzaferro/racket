import React from 'react'
import {Card} from 'antd'
import {connect} from 'react-redux'
import Glance from "./Glance/Glance";
import Parameters from "./Parameters/Parameters";

const tabList = [{
    key: 'tab1',
    tab: 'At a glance',
}, {
    key: 'tab2',
    tab: 'Parameters',
}];

const contentList = (props) => {
    return {tab1: <Glance {...props}/>, tab2: <Parameters {...props}/>,}
};


class Model extends React.Component {
    state = {
        key: 'tab1',
        noTitleKey: 'app',
    };

    onTabChange = (key, type) => {
        this.setState({[type]: key});
    };

    mmpToStr = (M, m, p) => `${M}.${m}.${p}`;

    render() {
        const {
            created_at,
            major,
            minor,
            patch,
            model_id,
            model_name,
            model_type,
            parameters
        } = this.props;

        const tabProps = {
            tab1: {
                version: this.mmpToStr(major, minor, patch),
                name: model_name,
                model_id: model_id,
                type: model_type,
                created_at: created_at
            },
            tab2: {params: parameters}
        };
        return (
            <div>
                <Card
                    style={{width: '100%'}}
                    title="Active Model"
                    extra={<a href="/#">More</a>}
                    tabList={tabList}
                    activeTabKey={this.state.key}
                    onTabChange={(key) => {
                        this.onTabChange(key, 'key');
                    }}
                >
                    {contentList(tabProps[this.state.key])[this.state.key]}
                </Card>
            </div>
        );
    }
}


const mapStateToProps = (state) => {
    return {...state.loader.selected}

};

export default connect(mapStateToProps)(Model);





