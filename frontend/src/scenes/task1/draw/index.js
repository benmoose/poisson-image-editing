import React from 'react'
// import axios from 'axios'
import { Link } from 'react-router-dom'
import { PathLine } from 'react-svg-pathline'

class Task1 extends React.Component {
  state = {
    imageName: null,
    region: []
  }

  componentDidMount () {
    const { match } = this.props
    this.setState({ imageName: match.params.imageName })
  }

  handleImageClick = (e) => {
    console.log('handle im click')
    const { x, y } = e.target.getBoundingClientRect()
    const clientX = e.clientX - x
    const clientY = e.clientY - y
    this.setState(p => ({ region: [...p.region, { x: clientX, y: clientY }] }))
  }

  handleRegionClear = (e) => this.setState({ region: [] })

  render () {
    const { imageName, region } = this.state
    console.log(region, region.map(p => `${p.x},${p.y}`).join(' '))
    return (
      <div>
        <div className='navbar navbar-expand bg-light navbar-light'>
          <div className='d-flex w-100 align-items-center justify-content-between'>
            <h5 className='navbar-brand mb-0'>{imageName}</h5>
            <div>
              <Link to='/task1'>Back</Link>
              <button
                disabled={!region.length}
                className='btn btn-danger ml-2'
                onClick={this.handleRegionClear}
              >Clear Region</button>
              <button
                disabled={region.length < 3}
                className='btn btn-primary ml-2'
              >Run Task</button>
            </div>
          </div>
        </div>
        <div className='container mt-4'>
          <div style={{ position: 'relative', width: '100%', height: '100%' }}>
            <svg style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', zIndex: 1, pointerEvents: 'none' }}>
              <polyline
                strokeWidth='2'
                fill='none'
                stroke='dodgerblue'
                fill='white'
                fillOpacity='0.15'
                points={region.map(p => `${p.x},${p.y}`).join(' ')}
              />
              {region.length >= 3 && (
                <line
                  x1={region[0].x}
                  y1={region[0].y}
                  x2={region[region.length-1].x}
                  y2={region[region.length-1].y}
                  stroke='lime'
                  strokeDasharray='5,5'
                  strokeWidth='2'
                />
              )}
            </svg>
            <img
              className='img-fluid'
              style={{ position: 'relative' }}
              src={`http://localhost:5000/static/${imageName}`}
              onClick={this.handleImageClick}
            >
            </img>
          </div>
        </div>
      </div>
    )
  }
}

export default Task1
