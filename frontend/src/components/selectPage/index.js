import React, { Component } from 'react'
import axios from 'axios'
import { string, number } from 'prop-types'

class Select extends Component {
  state = {
    images: []
  }

  componentDidMount () {
    axios.get('http://localhost:5000/images')
      .then(res => this.setState({ images: res.data }))
  }

  render () {
    const { taskNumber, taskDescription } = this.props
    return (
      <div className='container pt-4'>
        <div className='card mb-4'>
          <div className='card-body'>
            <h5 className='card-title'>Task {taskNumber}</h5>
            <span>{taskDescription}</span>
          </div>
        </div>
        <h5>Select Source Image</h5>
        <div className='row'>
          {
            this.state.images.map(i => (
              <div className='col-6 col-md-4 mb-4' key={i.name}>
                <div className='card'>
                  <img
                    src={`http://localhost:5000${i.url}`}
                    alt={i.name}
                    className='card-img-top'
                    style={{ objectFit: 'cover', height: '200px' }}
                  />
                  <div className='card-body'>
                    <h5 className='card-title'>{i.name}</h5>
                    <a href={`/task${taskNumber}/${i.name}`} className='card-link'>Select Image</a>
                  </div>
                </div>
              </div>
            ))
          }
        </div>
      </div>
    )
  }
}

Select.propTypes = {
  taskNumber: number.isRequired,
  taskDescription: string.isRequired
}

export default Select
