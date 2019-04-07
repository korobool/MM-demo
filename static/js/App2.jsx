import React, { Component } from 'react'
import { PageHeader } from "react-bootstrap";
import axios from 'axios'
import { Button, Grid, Row, Col, Form } from "react-bootstrap";

var $ = require('jquery');
var querystring = require('querystring')

require('../css/fullstack.css');

class App extends Component {
  constructor () {
    super()
    this.state = {
      result: ''
    }

    this.handleClick = this.handleClick.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleClick () {
    axios.get('http://localhost:8080/result')
      .then(response => this.setState({result: response.data.tree}))
  }

  handleSubmit(e) {
    alert('The value is: ' + this.input.value);
    axios.post('http://localhost:8080/text', {text: this.input.value})
    .then(function (response) {console.log(response);})
    .catch(function (error) {console.log(error);});
    e.preventDefault();
  }

  render () {
    return (
      <PageHeader>
      <div className='header-contents'>
        <Button bsSize="large" bsStyle="danger" onClick={this.handleClick}>Get Result</Button>
        <p>{this.state.result}</p>
      </div>
      <form onSubmit={this.handleSubmit}>
        <label>
          Input text here:
          <input type="text" ref={(input) => this.input = input} />
        </label>
        <input type="submit" value="Submit" />
      </form>
      </PageHeader>
    )
  }
}
export default App