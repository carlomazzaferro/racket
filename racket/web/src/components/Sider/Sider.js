import React, {PureComponent} from 'react'
import PropTypes from 'prop-types'
import {Layout} from 'antd'
import ScrollBar from '../ScrollBar'
import {config} from '../../utils/config'
import SiderMenu from './SiderMenu'
import './Sider.less'
import {connect} from 'react-redux'


class Sider extends PureComponent {

    render() {
        return (
            <Layout.Sider
                className="siderBar"
                width={256}
                theme='light'
                breakpoint="lg"
                trigger={null}
                collapsible
                collapsed={this.props.collapsed}

            >
                <div className='brand'>
                    <div className='logo'>
                        <img alt="logo"
                             src="https://raw.githubusercontent.com/carlomazzaferro/racket/master/docs/images/table-tennis_60px.png"/>
                        {this.props.collapsed ? null :
                            <div>
                                <h1>{config.siteName}</h1>
                                <p>Serve models with confidence</p>
                            </div>
                        }
                    </div>
                </div>

                <div className='menuContainer'>
                    <ScrollBar
                        option={{
                            suppressScrollX: true,
                        }}
                    >
                        <SiderMenu
                            theme='light'
                            collapsed={this.props.collapsed}
                        />

                    </ScrollBar>
                </div>
            </Layout.Sider>
        )
    }
}

Sider.propTypes = {
    theme: PropTypes.string,
    collapsed: PropTypes.bool,
    onThemeChange: PropTypes.func,
};


const mapStateToProps = (state) => {
    return {...state.header}

};


export default connect(mapStateToProps)(Sider);
