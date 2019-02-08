import React, {Fragment, PureComponent} from 'react'
import PropTypes from 'prop-types'
import {Avatar, Icon, Layout, Menu} from 'antd'
import classnames from 'classnames'
import './Header.less'
import {collapseHeader} from "../../actions";
import {connect} from 'react-redux'

const {SubMenu} = Menu;

class Header extends PureComponent {

    handleClickMenu = e => {
        console.log(e)
    };

    render() {
        const {
            fixed,
            avatar,
            username,
        } = this.props;

        const rightContent = [
            <Menu key="user" mode="horizontal" onClick={this.handleClickMenu}>
                <SubMenu
                    title={
                        <Fragment>
                            <span>{username}</span>
                            <Avatar style={{marginLeft: 8}} src={avatar}/>
                        </Fragment>
                    }
                >
                    <Menu.Item key="SignOut">
                    </Menu.Item>
                </SubMenu>
            </Menu>,
        ];
        return (
            <Layout.Header
                className={classnames('header', {
                    'fixed': fixed,
                    'collapsed': this.props.collapsed,
                })}
                id="layoutHeader"
            >
                <div
                    className='button'
                    onClick={this.props.collapse}
                >
                    <Icon
                        type={classnames({
                            'menu-unfold': this.props.collapsed,
                            'menu-fold': !this.props.collapsed,
                        })}
                    />
                </div>

                <div className='rightContainer'>{rightContent}</div>
            </Layout.Header>
        )
    }
}

Header.propTypes = {
    fixed: PropTypes.bool,
    user: PropTypes.object,
};

const mapDispatchToProps = (dispatch) => {
    return ({
        collapse: () => dispatch(collapseHeader()),
    })
};

const mapStateToProps = (state) => {
    return {...state.header}

};


export default connect(mapStateToProps, mapDispatchToProps)(Header)
