
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import classnames from 'classnames'
import './Page.less'

export default class Page extends Component {
  render() {
    const { className, children, inner = false } = this.props

    return (
      <div
        className={classnames(className, {
          'contentInner': inner,
        })}
      >
        {children}
      </div>
    )
  }
}

Page.propTypes = {
  className: PropTypes.string,
  children: PropTypes.node,
  loading: PropTypes.bool,
  inner: PropTypes.bool,
};
