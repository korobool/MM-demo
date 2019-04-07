import React, { Component } from 'react';
import axios from 'axios';
import { PageHeader, Button, Grid, Row, Col, Form, Container} from "react-bootstrap";
import JSONTree from 'react-json-tree';
import ReactInterval from 'react-interval';

var $ = require('jquery');
var querystring = require('querystring');

require('../css/fullstack.css');


class App extends Component {
  constructor () {
    super()
    this.state = {
      result: '',
      count: 0
    };

    this.json = {array: [1, 2, 3]};
    this.theme = {
      scheme: 'monokai',
      base00: '#272822',
      base01: '#383830',
      base02: '#49483e',
      base03: '#75715e',
      base04: '#a59f85',
      base05: '#f8f8f2',
      base06: '#f5f4f1',
      base07: '#f9f8f5',
      base08: '#f92672',
      base09: '#fd971f',
      base0A: '#f4bf75',
      base0B: '#a6e22e',
      base0C: '#a1efe4',
      base0D: '#66d9ef',
      base0E: '#ae81ff',
      base0F: '#cc6633'
    };

    this.handleClick = this.handleClick.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  };

  handleClick () {
    axios.get('http://localhost:8080/result')
      .then(response => this.setState({result: response.data.tree}))
  };

  handleSubmit(e) {
    alert('The value is: ' + this.input.value);
    axios.post('http://localhost:8080/text', {text: this.input.value})
    .then(function (response) {console.log(response);})
    .catch(function (error) {console.log(error);});
    e.preventDefault();
  };

  render () {
    return (
      <PageHeader>
        <Row>
          <Col sm={4}>
           <form onSubmit={this.handleSubmit}>
             <label> Input text here:</label>
               <textarea  rows="6" ref={(input) => this.input = input}></textarea>
               <input type="submit" value="Send data" />
           </form>
          </Col>
          <Col sm={2}></Col>
          <Col sm={6}>
            Result json tree:
            {this.state.count}
            <ReactInterval timeout={5000} enabled={true} callback={() => this.setState({count: this.state.count + 1})} />
            <JSONTree data={this.json} theme={this.theme} invertTheme={true}/>
          </Col>
        </Row>
      </PageHeader>
    )
  }
}
export default App