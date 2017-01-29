import React from 'react';
import Table from './Table2.jsx';

export default class App extends React.Component {
  render() {
    return (<div>
      <p>React boilerplate</p>
      <Table />
    </div>);
  }
}
App.propTypes = { children: React.PropTypes.object };
