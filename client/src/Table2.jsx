import React, { Component, PropTypes } from 'react';

import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';

function urlFormat(cell) {
  return <a href={cell} target="_blank">{cell}</a>;
}

function addButtons(_, row) {
  return <button onClick={() => console.log(row)}>Button</button>;
}

class Table2 extends Component {
  render() {
    return (
      <div>
        <h2>Query: {this.props.queryTerm}</h2>
        <BootstrapTable data={this.props.items} striped hover search multiColumnSearch>
          <TableHeaderColumn dataSort isKey dataField="id">ID</TableHeaderColumn>
          <TableHeaderColumn dataField="filename" dataSort >FullName</TableHeaderColumn>
          <TableHeaderColumn dataField="page">page</TableHeaderColumn>
          <TableHeaderColumn dataField="text">text</TableHeaderColumn>
          <TableHeaderColumn dataField="URL" dataSort dataFormat={urlFormat}>URL</TableHeaderColumn>
          <TableHeaderColumn dataField="score" dataSort>Score</TableHeaderColumn>
          <TableHeaderColumn dataFormat={addButtons} >Details</TableHeaderColumn>
        </BootstrapTable>
      </div>
    );
  }
}
Table2.propTypes = {
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
    // window.fetch(`https://api.github.com/search/repositories?q=${this.state.q}`)
    window.fetch('http://192.168.0.14:8000/search')
      .then(res => res.json())
      .then(json => this.setState({
        items: json.hits.hits.map(e => ({
          score: e['_score'],
          text: e['_source']['text'],
          page: e['_source']['page'],
          filename: e['_source']['filename'],
          URL: `/uploads/${e['_source']['filename']}`,
        })
        ),
      }))
      .catch(e => console.log(e));
  }
  render() {
    console.log(this.state.items);
    return <Table2 queryTerm={this.state.q} items={this.state.items} />;
  }
}

export default WrapTable;
