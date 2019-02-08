import React from 'react'
import PropTypes from 'prop-types'
import './Glance.less'

class Glance extends React.Component {
    render() {
        const {
            version,
            name,
            model_id,
            type,
            created_at,
        } = this.props;

        const content = [
            {name: 'Name', val: name},
            {name: 'Version', val: version},
            {name: 'Created At', val: created_at},
            {name: 'Type', val: type},
            {name: 'ID', val: model_id},
        ];

        return (
            <div>
                {content.map((c, i) => (
                        <div key={i} className="titles">
                            {c.name}: <span className='values'> {c.val} </span>
                        </div>
                    )
                )
                }
            </div>
        )
    }
}


Glance.propTypes = {
    version: PropTypes.string,
    name: PropTypes.string,
    model_id: PropTypes.number,
    type: PropTypes.string,
    created_at: PropTypes.string
};


export default Glance
