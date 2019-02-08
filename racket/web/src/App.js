import {routeList, user} from "./utils/config";
import React, {Fragment, PureComponent} from 'react'
import {BackTop, Layout} from 'antd'
import {GlobalFooter} from 'ant-design-pro'
import {config} from './utils/config'
import './index.less'
import Sider from "./components/Sider/Sider";
import Header from "./components/Header/Header";
import {connect} from 'react-redux'
import Bread from "./components/Bread/Bread";
import ModelList from "./components/Models/ModelList";
import {fetchActive, fetchModels} from "./services";
import ModelView from "./components/ModelView/ModelView";

const {Content} = Layout;

class App extends PureComponent {

    componentWillMount() {
        this.props.loadAll();
        this.props.loadActive();
    }

    render() {
        const {page} = this.props;

        const headerProps = {
            avatar: user.avatar,
            username: user.username,
            fixed: config.fixedHeader,
        };


        const userModel = {
            currentItem: {},
            modalVisible: false,
            modalType: 'create',
            selectedRowKeys: [],
        };


        const childPage = () => {
            switch (page) {
                case 'models':
                    return <ModelList user={userModel}/>;
                case 'model':
                    const id = parseInt(this.props.match.params.id);
                    return <ModelView model_id={id}/>;
                default:
                    return <ModelList user={userModel}/>;
            }
        };


        return (
            <Fragment>
                <Layout>
                    <Sider/>
                    <div
                        className="container"
                        style={{paddingTop: config.fixedHeader ? 72 : 0}}
                        id="primaryLayout"
                    >
                        <Header {...headerProps} />
                        <Content className="content">
                            <div>
                                <Bread routeList={routeList}/>
                                {childPage()}
                            </div>
                        </Content>
                        <BackTop
                            className="backTop"
                            target={() => document.querySelector('#primaryLayout')}
                        />
                        <GlobalFooter
                            className="footer"
                            copyright={config.copyright}
                        />
                    </div>
                </Layout>
            </Fragment>
        )
    }
}


const mapDispatchToProps = (dispatch) => {
    return ({
        loadAll: () => dispatch(fetchModels()),
        loadActive: () => dispatch(fetchActive()),
    })
};


const mapStateToProps = (state) => {
    return {active: state.loader.active}

};

export default connect(mapStateToProps, mapDispatchToProps)(App);
