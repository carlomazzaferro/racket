import React, {PureComponent} from 'react'
import PropTypes from 'prop-types'
import {Icon, Menu} from 'antd'
import {Link} from "react-router-dom";
import {connect} from 'react-redux'


const SubMenu = Menu.SubMenu;

class SiderMenu extends PureComponent {

    render() {
        const {
            collapsed,
        } = this.props;

        return (
            <Menu
                mode="inline"
                theme={'light'}
                inlineCollapsed={collapsed}
                defaultSelectedKeys={['1']}
            >
                <Menu.Item key={['1']}>
                    <Link to={'/dashboard'}>
                        <Icon type='dashboard'/>
                        <span>Dashboard</span>
                    </Link>)
                </Menu.Item>
                <SubMenu
                    key="sub1"
                    title={<span><Icon type="dot-chart"/><span>Models</span></span>}
                >
                    <Menu.Item key="3">
                        <Link to={'/models'}><span>Available Models</span></Link>
                    </Menu.Item>
                    <Menu.Item key="4">
                        <Link to={'/model/' + this.props.active}><span>Active model</span></Link>
                    </Menu.Item>
                </SubMenu>
                <Menu.Item key="9">
                    <Icon type="pushpin"/>
                    <span>Actions</span>
                </Menu.Item>
            </Menu>
        )
    }
}

SiderMenu.propTypes = {
    menus: PropTypes.array,
    theme: PropTypes.string,
    collapsed: PropTypes.bool,
};


const mapStateToProps = (state) => {
    return {active: state.loader.active_id}

};


export default connect(mapStateToProps)(SiderMenu);

