import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from 'axios'

import * as d3 from 'd3';
import Charts from './Charts/Charts';

function App() {
  const [count, setCount] = useState(0)
  const [currentTime, setCurrentTime] = useState(0);
  
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState([]);

  // Time effect
  useEffect(() => {
    fetch('/api/time').then(res => res.json()).then(Tdata => {
      setCurrentTime(Tdata.time);
    });
  }, []);

  // D3 effect
  useEffect(() => {
    // const dataURL = "https://d3js-in-action-third-edition.github.io/hosted-data/apis/front_end_frameworks.json";
    const dataURL = "http://127.0.0.1:5000/api/file1.json"
    
    let mounted = true;
    d3.json(dataURL).then(data => {
      console.log("data", data);

      if (mounted) {
        setData(data);
        setLoading(false);
      }
    });

    return () => mounted = false;
  }, []);

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>The current time is {new Date(currentTime * 1000).toLocaleString()}.</p>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <FileUploader/>

      <div className="container">
        {loading && <div className="loading">Loading...</div>}
        {!loading && <Charts data={data} />}
      </div>
    </>
  )
}

function FileUploader() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [content, setContent] = useState("")

  // When user selects a file
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  // Upload to Flask backend
  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file); // <-- must match Flask key: request.files['file']

    setMessage("Processing...");

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
    } catch (error) {
      console.error(error);
      setMessage("Upload failed." + error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Upload a File</h2>

      <input type="file" onChange={handleFileChange} />

      <br /><br />

      <button onClick={handleUpload}>Upload</button>

      <p>{message}</p>

      <p>{content}</p>
    </div>
  );
}

export default App
