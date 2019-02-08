import React, {PureComponent} from 'react'
import {Icon, Table} from 'antd'
import './ModelList.less'
import {connect} from 'react-redux'
import _ from 'lodash'
import moment from 'moment'
import Filter from '../Filter/Filter'
import Page from "../Page/Page";


class ModelList extends PureComponent {

    render() {
        let {models, unique, dateFilter, ...tableProps} = this.props;
        if (dateFilter[0] && dateFilter[1]) {
            models = this.props.models.filter((record) => {
                return moment(record.created_at).isBetween(this.props.dateFilter[0], this.props.dateFilter[1])
            })
        }
        const filterProps = {
            filter: {}
        };

        const columns = [
            {
                title: 'ID',
                dataIndex: 'model_id',
                key: 'model_id',
                width: 72,
                fixed: 'left',
                render: text => <a href={`model/${text}`}>{text}</a>,
            },
            {
                title: 'Name',
                dataIndex: 'model_name',
                key: 'model_name',
                width: 180,
                filters: unique.names.map(m => ({text: m, value: m})),
                filterMultiple: false,
                onFilter: (value, record) => record.model_name.indexOf(value) === 0,
                sorter: (a, b) => a.model_name.length - b.model_name.length,
            },
            {
                title: 'Major',
                dataIndex: 'major',
                key: 'major',
                sorter: (a, b) => a.major - b.major

            },
            {
                title: 'Minor',
                dataIndex: 'minor',
                key: 'minor',
                sorter: (a, b) => a.minor - b.minor,

            },
            {
                title: 'Patch',
                dataIndex: 'patch',
                key: 'patch',
                sorter: (a, b) => a.patch - b.patch,

            },
            {
                title: 'Created At',
                dataIndex: 'created_at',
                key: 'created_at',
                sorter: (a, b) => moment(a.created_at, b.created_at)

            },
            {
                title: 'Model Type',
                dataIndex: 'model_type',
                key: 'model_type',
                filters: unique.model_types.map(m => ({text: m, value: m})),
                filterMultiple: false,
                onFilter: (value, record) => record.model_type.indexOf(value) === 0,
                sorter: (a, b) => a.model_type.length - b.model_type.length,
            },
            {
                title: 'Parameters',
                dataIndex: 'parameters',
                key: 'parameters',
                render: text => {
                    if (text === undefined) {
                        return {}
                    }

                    const parsed = _.pickBy(JSON.parse(text.params));
                    const sampled = _.sampleSize(Object.keys(parsed), 2).map(k => k + '=' + parsed[k]).join(', ');
                    return <div><a href={`model/${text.id}`}> {sampled.slice(0, 20)}... <Icon type='link'/> </a></div>
                },
            },

        ];

        return (
            <Page inner>
                <Filter {...filterProps} />
                <Table
                    dataSource={models}
                    pagination={{
                        ...tableProps.pagination,
                        showTotal: total => `Total ${total} Items`,
                    }}

                    className='table'
                    columns={columns}
                    rowKey={record => record.id}
                />
            </Page>
        )
    }
}

ModelList.propTypes = {};


const mapStateToProps = (state) => {
    return {
        models: state.loader.models.map(m => ({...m, parameters: {params: m.parameters, id: m.model_id}})),
        unique: {
            names: [...new Set(state.loader.models.map(obj => obj.model_name))],
            model_types: [...new Set(state.loader.models.map(obj => obj.model_type))],
        },
        dateFilter: [state.loader.start, state.loader.end]
    }

};


export default connect(mapStateToProps)(ModelList);
