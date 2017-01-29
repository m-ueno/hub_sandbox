import React, { Component, PropTypes } from 'react';
// import { Table, Column, Cell } from 'fixed-data-table';

import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';

function scoreFormatter(cell) {
  return `<i class="glyphicon glyphicon-usd"></i> ${cell}`;
}

function urlFormat(cell) {
  return <a href={cell} target="_blank">{cell}</a>;
}

function addButtons(_, row) {
  return <button onClick={() => console.log(row)}>Button</button>;
}
class Table1 extends Component {
  render() {
    return (
      <div>
        <h2>Query: {this.props.queryTerm}</h2>
        <BootstrapTable data={this.props.items} striped hover search multiColumnSearch>
          <TableHeaderColumn dataSort isKey dataField="id">ID</TableHeaderColumn>
          <TableHeaderColumn dataField="full_name" dataSort >FullName</TableHeaderColumn>
          <TableHeaderColumn dataField="description">Description</TableHeaderColumn>
          <TableHeaderColumn dataField="html_url" dataFormat={urlFormat}>URL</TableHeaderColumn>
          <TableHeaderColumn dataField="score" dataSort dataFormat={scoreFormatter} >
            Score
          </TableHeaderColumn>
          <TableHeaderColumn dataFormat={addButtons} >Details</TableHeaderColumn>
        </BootstrapTable>
      </div>
    );
  }
}
Table1.propTypes = {
  items: PropTypes.array,
  queryTerm: PropTypes.string,
};

class WrapTable extends Component {
  constructor(props) {
    super(props);
    this.state = {
      q: 'luigi',
      items: [],
    };
  }
  componentDidMount() {
    window.fetch(`https://api.github.com/search/repositories?q=${this.state.q}`)
      .then(res => res.json())
      .then(json => this.setState({ items: json.items }))
      .catch(e => console.log(e));
  }
  render() {
    return <Table1 queryTerm={this.state.q} items={this.state.items} />;
  }
}

export default WrapTable;
