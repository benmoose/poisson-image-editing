import React from 'react'
import axios from 'axios'
import classnames from 'classnames'
import { Link } from 'react-router-dom'

class Task1 extends React.Component {
  state = {
    imageName: null,
    imageBoundingClientRect: null,
    resultUrl: '',
    region: [],
    loading: false,
    imageNotFound: false
  }

  componentDidMount () {
    const { match } = this.props
    this.setState({ imageName: match.params.imageName })
    axios.get(`http://localhost:5000/static/${match.params.imageName}`)
      .catch(err => this.setState({
        imageNotFound: true
      }))
  }

  handleImageClick = (e) => {
    this.setState({ imageBoundingClientRect: e.target.getBoundingClientRect() })
    const { x, y } = e.target.getBoundingClientRect()
    const clientX = e.clientX - x
    const clientY = e.clientY - y
    this.setState(p => ({
      region: [...p.region, { x: clientX, y: clientY }]
    }))
  }

  handleRegionClear = (e) => this.setState({ region: [], resultUrl: '' })

  handleRunTask = () => {
    const { region, imageBoundingClientRect } = this.state
    if (region.length < 3) return
    this.setState({ loading: true })
    // Values are abs, but we need percentages
    const encodedRegion = region.map(p => `${(p.x / imageBoundingClientRect.width).toFixed(2) },${(p.y / imageBoundingClientRect.height).toFixed(2)}`).join(',')
    axios.get(`http://localhost:5000/poisson/t5/${this.state.imageName}`, {
      params: { region: encodedRegion }
    })
      .then(res => this.setState({ resultUrl: res.data.result_url, loading: false }))
  }

  render () {
    const { imageName, region, resultUrl, loading, imageNotFound } = this.state
    return imageNotFound ? (
      <div className='container pt-3'>
        <article className='alert alert-danger'>
          <div><strong>{imageName}</strong> not found.</div>
          <div><Link to='/task5'>Go back</Link></div>
        </article>
      </div>
    ) : (
      <div>
        <div className='navbar navbar-expand bg-light navbar-light'>
          <div className='d-flex w-100 align-items-center justify-content-between'>
            <h5 className='navbar-brand mb-0'>{imageName}</h5>
            <div>
              <Link to='/task5'>Back</Link>
              <button
                disabled={!region.length || loading}
                className='btn btn-danger ml-2'
                onClick={this.handleRegionClear}
              >Clear Region</button>
              <button
                disabled={region.length < 3 || loading}
                className='btn btn-primary ml-2'
                onClick={this.handleRunTask}
              >Run Task</button>
            </div>
          </div>
        </div>
        <div className='container pt-4'>
          <div className='row'>
            <div className='col-6 d-flex flex-column'>
              <h5>Original</h5>
              <div style={{ position: 'relative', width: '100%', height: '100%' }}>
                <svg style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', zIndex: 1, pointerEvents: 'none' }}>
                  <polyline
                    strokeWidth='2'
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
                  style={{ objectFit: 'contain', cursor: 'crosshair' }}
                  src={`http://localhost:5000/static/${imageName}`}
                  alt={imageName}
                  onClick={this.handleImageClick}
                >
                </img>
              </div>
            </div>
            <div className='col-6 d-flex flex-column'>
              <h5 className={classnames({ 'text-muted': loading })}>Result</h5>
              {resultUrl ? (
                <img
                  src={`http://localhost:5000${resultUrl}`}
                  alt='Result'
                  className='img-fluid'
                  style={{ objectFit: 'contain' }}
                />
              ) : (
                <div className={classnames('card h-100', { 'bg-light': loading })} />
              )}
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default Task1
