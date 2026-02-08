import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [video, setVideo] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!video) return alert("Please upload a video first.");
    
    const formData = new FormData();
    formData.append("file", video);
    
    setLoading(true);
    setResult(null);
    
    try {
      // Connects to your FastAPI backend
      const res = await axios.post("http://127.0.0.1:8000/analyze-video", formData);
      setResult(res.data);
    } catch (err) {
      alert("Error analyzing video");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Lucid TRACE</h1>
      <p>Upload video evidence to verify authenticity</p>
      
      <input 
        type="file" 
        accept="video/*" 
        onChange={(e) => setVideo(e.target.files[0])} 
      />
      
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Video"}
      </button>

      {result && (
        <div className="result">
          <p><b>Frames Analyzed:</b> {result.frames_analyzed}</p>
          <p><b>AI Probability:</b> {result.ai_probability}%</p>
          <p><b>Verdict:</b> {result.verdict}</p>
        </div>
      )}
    </div>
  );
}

export default App;