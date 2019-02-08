import React, {Fragment, PureComponent} from 'react'
import PropTypes from 'prop-types'
import {Breadcrumb, Icon} from 'antd'
import './Bread.less'


class Bread extends PureComponent {
    generateBreadcrumbs = paths => {
        return paths.map((item, key) => {
            const content = (
                <Fragment>
                    {item.icon ? (
                        <Icon type={item.icon} style={{marginRight: 4}}/>
                    ) : null}
                    {item.name}
                </Fragment>
            );

            return (
                <Breadcrumb.Item key={key}>
                    {content}
                </Breadcrumb.Item>
            )
        })
    };

    render() {
        const {routeList} = this.props;

        // Find a route that matches the pathname.

        // Find the breadcrumb navigation of the current route match and all its ancestors.
        const paths = [
            routeList[0],
            {
                id: 404,
                name: 'Not Found',
            },
        ];

        return (
            <Breadcrumb className='bread'>
                {this.generateBreadcrumbs(paths)}
            </Breadcrumb>
        )
    }
}

Bread.propTypes = {
    routeList: PropTypes.array,
};

export default Bread
