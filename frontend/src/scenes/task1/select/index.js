import React, { Component } from 'react'
import axios from 'axios'

class App extends Component {
  state = {
    images: []
  }

  componentDidMount () {
    axios.get('http://localhost:5000/images')
      .then(res => this.setState({ images: res.data }))
  }

  render () {
    return (
      <div className='container mt-4'>
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
                    <a href={`/task1/${i.name}`} className='card-link'>Select Image</a>
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

export default App
