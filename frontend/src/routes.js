import React from 'react'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'

import Home from './scenes/home'
import Task1Select from './scenes/task1/select'
import Task1Draw from './scenes/task1/draw'

import Nav from './components/nav'

export default () => (
  <Router>
    <div>
      <Route component={Nav} />
      <Switch>
        <Route exact path='/' component={Home} />

        <Route path='/task1/:imageName' component={Task1Draw} />
        <Route path='/task1' component={Task1Select} />

        <Route render={() => <p>404 Not Found</p>} />
      </Switch>
    </div>
  </Router>
)
