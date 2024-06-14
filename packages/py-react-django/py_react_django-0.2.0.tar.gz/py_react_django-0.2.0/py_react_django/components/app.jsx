/**
 * Demo reactView jsx file
 */
import React from 'react'
import ReactDOM from 'react-dom'


function App() {
    return (<h1>ReactView</h1>)
}

const app = document.getElementById("app")

ReactDOM.render(<React.StrictMode>
    <App {...window.props} />
</React.StrictMode>, app)
