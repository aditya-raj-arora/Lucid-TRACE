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
    <div className="container" style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "70vh", textAlign: "center" }}>
      <h1>🔍 Lucid TRACE</h1>
      <p>📹 Upload media evidence to verify authenticity</p>
      
      <div className="upload-wrapper">
        <input 
          type="file" 
          id="file-upload" 
          accept="video/*,image/*" 
          onChange={(e) => setVideo(e.target.files[0])} 
          style={{ display: 'none' }}
        />
        <label htmlFor="file-upload" className="custom-file-upload">
          {video ? `📄 ${video.name}` : "📂 Choose Media File"}
        </label>
      </div>
      
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "⏳ Analyzing..." : "🚀 Analyze Evidence"}
      </button>

      {result && (
        <div className="result">
          <p><b>🎞️ Frames Analyzed:</b> {result.frames_analyzed}</p>
          <p><b>🤖 AI Probability:</b> {result.ai_probability}%</p>
          <p><b>⚖️ Verdict:</b> {result.verdict}</p>
        </div>
      )}
    </div>
  );
}

export default App;