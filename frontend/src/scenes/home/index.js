import React from 'react'
import { Link } from 'react-router-dom'

export default () => (
  <ul className='pt-4'>
    <li><Link to='/task1'>Task 1</Link></li>
    <li><Link disabled to='/task2'>Task 2</Link></li>
    <li><Link disabled to='/task3'>Task 3</Link></li>
    <li><Link disabled to='/task4'>Task 4</Link></li>
    <li><Link disabled to='/task5'>Task 5 (Texture Flattening)</Link></li>
  </ul>
)
