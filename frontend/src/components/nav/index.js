import React from 'react'
import { Link } from 'react-router-dom'

export default ({ location }) => {
  const isTaskUrl = /\/task\d+/i.test(location.pathname)
  const taskNumber = location.pathname.match(/\/task(\d+)/i)
  return (
    <nav className='navbar navbar-expand navbar-dark bg-dark justify-content-between fixed-top'>
      <Link to='/' className='navbar-brand'>Poisson Image Editing</Link>
      {isTaskUrl && <span className='navbar-text'>Task {taskNumber[1]}</span>}
    </nav>
  )
}
