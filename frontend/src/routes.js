import React from 'react'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'

import Home from './scenes/home'

import Task1Select from './scenes/task1/select'
import Task1Draw from './scenes/task1/draw'
import Task2Select from './scenes/task2/select'
import Task2Draw from './scenes/task2/draw'

import Nav from './components/nav'

export default () => (
  <Router>
    <div>
      <Route component={Nav} />
      <Switch>
        <Route exact path='/' component={Home} />

        <Route path='/task1/:imageName' component={Task1Draw} />
        <Route path='/task1' component={Task1Select} />
        <Route path='/task2/:imageName' component={Task2Draw} />
        <Route path='/task2' component={Task2Select} />

        <Route render={() => <p>404 Not Found</p>} />
      </Switch>
    </div>
  </Router>
)
