import React, { Component } from 'react'
import axios from 'axios'

class Gallary extends Component {
  state = {
    imageSets: []
  }

  componentDidMount () {
    axios.get('http://localhost:5000/poisson/t4')
      .then(res => this.setState({ imageSets: res.data }))
  }

  render () {
    return (
      <div className='container pt-4'>
        <div className='card mb-4'>
          <div className='card-body'>
            <h5 className='card-title'>Task 4</h5>
            Select images you like to edit and show interesting effects.
            Try to record the intermediate results; you can allow multiple
            strokes in this stage. Try to create some cool effects.
          </div>
        </div>
        <h5>Images</h5>
          {
            this.state.imageSets.map((set, i) => (
              <div>
                <h6>Set {i + 1}</h6>
                <div className='row' key={i}>
                  {
                    ['final', 'mask', 'red_channel', 'green_channel', 'blue_channel'].map((pass, i) => (
                      <div className='col-6 mb-4' key={i}>
                        <article className='card'>
                          <img
                            src={`http://localhost:5000${set[pass]}`}
                            alt={pass}
                            className='card-img-top'
                            style={{ objectFit: 'contain' }}
                          />
                          <div className='card-footer'>{pass[0].toUpperCase() + pass.replace('_', ' ').slice(1)}</div>
                        </article>
                      </div>
                    ))
                  }
                </div>
              </div>
            ))
          }
      </div>
    )
  }
}

export default Gallary
