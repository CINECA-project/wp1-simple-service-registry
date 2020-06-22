import React, { Component } from 'react';
import GetServicesTable from './components/ServicesTable/GetServicesTable';
import logo from './CINECA_logo.png';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" /> Service Registry
        </header>

        <h1 className="header">Registered Services</h1>
        <GetServicesTable/>        
      </div>
    );
  }
}

export default App;
