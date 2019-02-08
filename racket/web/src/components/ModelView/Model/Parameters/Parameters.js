import React from 'react'
import PropTypes from 'prop-types'
import {Table, Tag} from 'antd';
import _ from 'lodash';

const columns = [{
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
    render: text => <a href="/#">{text}</a>,
}, {
    title: 'Value',
    dataIndex: 'value',
    key: 'value',
    render: text => Array.isArray(text) ? (
        <span>
        {text.map(tag => {
            let color = tag.startsWith('val') ? 'geekblue' : 'volcano';
            return <Tag color={color} key={tag}>{tag.toUpperCase()}</Tag>;
        })}
    </span>
    ) : text.toString()
},
];

class Parameters extends React.Component {

    render() {
        const {
            params
        } = this.props;
        const as_table = params => _.map(params, (value, name) => (value !== null ? {name, value} : {
            name,
            value: 'None',
        }));
        const parsed = JSON.parse(params);
        let data = as_table(parsed).map((m, i) => ({...m, key: i}));
        return (
            <Table columns={columns} dataSource={data}/>
        )
    }
}


Parameters.propTypes = {
    params: PropTypes.string,
};


export default Parameters
