import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from 'axios'

import * as d3 from 'd3';
import Charts from './Charts/Charts';

function App() {
  const [count, setCount] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);

  // Time effect
  useEffect(() => {
    fetch('/api/time').then(res => res.json()).then(Tdata => {
      setCurrentTime(Tdata.time);
    });
  }, []);

  return (
    <>
      {/* <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div> */}
      <h1>Last.fm Popularity Calculator</h1>
      <div className="card">
        {/* <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button> */}
        {/* <p className='black-text'>The current time is {new Date(currentTime * 1000).toLocaleString()}.</p> */}
        {/* <p className='black-text'>The current time is {currentTime}.</p>
        <p className='black-text'>A week ago is {currentTime - 864000}.</p>
        <p className='black-text'>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p> */}
        <p className='black-text'> Instructions:</p>
        <ol className='black-text'>
          <li>Visit <a href="https://mainstream.ghan.nl/export.html">this Last.fm export tool</a></li>
          <li>Enter your username, and select "Scrobbles" and "CSV" from the two dropdowns</li>
          <li>Enter "{currentTime - 864000}" into the "timestamp" field</li>
          <li>Click "Go", then upload the exported file below</li>
        </ol>
      </div>
      {/* <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p> */}
      <FileUploader/>


    </>
  )
}

function FileUploader() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [content, setContent] = useState("");

  const [query, setQuery] = useState("");

  const [loading, setLoading] = useState(true);
  const [data, setData] = useState([]);

  // When user selects a file
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  // const handleQuerySubmit = (e) => {
  //   setQuery(e.target.value);
  // };

  // Upload to Flask backend
  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file); // <-- must match Flask key: request.files['file']

    setMessage("Processing...");

    let filename;

    try {
      const response = await axios.post(
        "http://localhost:5000/api/upload", // Flask route
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setMessage(response.data.message);

      setContent(response.data.content);
      filename = response.data.jsonname;
    } catch (error) {
      console.error(error);
      setMessage("Upload failed." + error);
    }
    
    const dataURL = `http://127.0.0.1:5000/api/${filename}`;
    
    console.log("requestURL", dataURL);
    
    let mounted = true;
    d3.json(dataURL).then(data => {
      console.log("data", data);

      if (mounted) {
        setData(data);
        setLoading(false);
      }
    });
  };

  const handleBypass = async () => {
    if (query === "") {
      setMessage("Please enter a query first.");
      return;
    }

    const formData = new FormData();
    formData.append("query", query);
    
    const dataURL = `http://127.0.0.1:5000/api/${query}.json`;
    
    console.log("requestURL (bypass)", dataURL);
    
    let mounted = true;
    d3.json(dataURL).then(data => {
      console.log("data", data);

      if (mounted) {
        setData(data);
        setLoading(false);
      }
    });
  };

  return (
    
    <div style={{ padding: "4px" }}>
      <div style={{ padding: "20px" }}>
        <h3>Upload a File</h3>

        <input type="file" onChange={handleFileChange} />

        <br /><br />

        <button onClick={handleUpload}>Upload</button>

        <br /><br />

        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Past search code..."
        />

        <button onClick={handleBypass}>Go</button>

        <p>{message}</p>

        <p>{content}</p>
      </div> 
      <div className="container">
        {loading && <div className="loading">Waiting for chart data...</div>}
        {!loading && <Charts data={data} />}
      </div>
    </div>
  );
}

export default App
