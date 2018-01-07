import React from 'react'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'

import { default as t } from './taskInfo'

import Nav from './components/nav'
import Home from './scenes/home'
import Select from './components/selectPage'

import Task1Draw from './scenes/task1/draw'
import Task2Draw from './scenes/task2/draw'
import Task3Draw from './scenes/task3/draw'
import Task5Draw from './scenes/task5/draw'

export default () => (
  <Router>
    <div>
      <Route component={Nav} />
      <Switch>
        <Route exact path='/' component={Home} />

        <Route path='/task1/:imageName' component={Task1Draw} />
        <Route path='/task1' render={() => <Select taskNumber={t.t1.number} taskDescription={t.t1.desc} />} />
        <Route path='/task2/:imageName' component={Task2Draw} />
        <Route path='/task2' render={() => <Select taskNumber={t.t2.number} taskDescription={t.t2.desc} />} />
        <Route path='/task3/:imageName' component={Task3Draw} />
        <Route path='/task3' render={() => <Select taskNumber={t.t3.number} taskDescription={t.t3.desc} />} />
        <Route path='/task4/:imageName' component={() => <p>Todo...</p>} />
        <Route path='/task4' render={() => <Select taskNumber={t.t4.number} taskDescription={t.t4.desc} />} />
        <Route path='/task5/:imageName' component={Task5Draw} />
        <Route path='/task5' render={() => <Select taskNumber={t.t5.number} taskDescription={t.t5.desc} />} />

        <Route render={() => <p>404 Not Found</p>} />
      </Switch>
    </div>
  </Router>
)
