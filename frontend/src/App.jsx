import { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons";

function App() {
  const [video, setVideo] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [showExternalReview, setShowExternalReview] = useState(false);
  const canvasRef = useRef(null);

  useEffect(() => {
    const loadScript = (src) => {
      return new Promise((resolve) => {
        const script = document.createElement("script");
        script.src = src;
        script.async = true;
        script.onload = resolve;
        document.body.appendChild(script);
      });
    };

    const initThpace = async () => {
      if (!window.ThpaceGL) await loadScript("https://unpkg.com/thpace");
      
      if (window.ThpaceGL && canvasRef.current) {
        const settings = {
          colors: ['#38003c', '#520e0e', '#fc0000'],
          triangleSize: 100,
        };
        window.ThpaceGL.create(canvasRef.current, settings);
      }
    };

    initThpace();
  }, []);

  const handleUpload = async () => {
    if (!video) return alert("Please upload a video first.");
    
    const formData = new FormData();
    formData.append("file", video);
    
    setLoading(true);
    setResult(null);
    setShowExternalReview(false);
    
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

  const onDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const onDragLeave = (e) => {
    e.preventDefault();
    if (!e.currentTarget.contains(e.relatedTarget)) {
      setIsDragging(false);
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setVideo(e.dataTransfer.files[0]);
    }
  };

  const analysisData = result ? (Array.isArray(result) ? result[0] : result) : null;
  const extraData = result && Array.isArray(result) ? result[1] : null;

  return (
    <div style={{ position: "relative", width: "100vw", height: "100vh", display: "flex", alignItems: "center", justifyContent: "center", overflow: "hidden" }}>
    <canvas ref={canvasRef} style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", zIndex: -1 }} />
    <div className="container" style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "70vh", textAlign: "center" }}>
      <h1><FontAwesomeIcon icon={faMagnifyingGlass} /> Lucid TRACE</h1>
      <p>📹 Upload media evidence to verify authenticity</p>
      
      <div 
        className="upload-wrapper"
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        style={{
          border: isDragging ? "2px dashed #fff" : "2px dashed transparent",
          borderRadius: "10px",
          backgroundColor: isDragging ? "rgba(255,255,255,0.1)" : "transparent",
          transition: "all 0.2s ease"
        }}
      >
        <input 
          type="file" 
          id="file-upload" 
          accept="video/*,image/*" 
          onChange={(e) => setVideo(e.target.files[0])} 
          style={{ display: 'none' }}
        />
        <label htmlFor="file-upload" className="custom-file-upload">
          {video ? `📄 ${video.name}` : (isDragging ? "⬇️ Drop File Here" : "📂 Upload Files")}
        </label>
      </div>
      
      <button className="analysis-button" onClick={handleUpload} disabled={loading}>
        {loading ? "⏳ Analyzing..." : "🚀 Analyze Evidence"}
      </button>

      {analysisData && (
        <div className="result">
          <p><b>🎞️ Frames Analyzed:</b> {analysisData.frames_analyzed}</p>
          <p><b>🤖 AI Image Probability:</b> {analysisData.details.ai_image_branch}%</p>
          <p><b>🤖 Deepfake Probability:</b> {analysisData.details.deepfake_branch}%</p>
          <p><b>⚖️ Verdict:</b> {analysisData.verdict}</p>
          {extraData && !showExternalReview && (
            <button className="external-review-button" onClick={() => setShowExternalReview(true)} style={{ marginTop: "15px" }}>
              See External Analysis
            </button>
          )}
          {extraData && showExternalReview && (
            <div style={{ marginTop: "15px", paddingTop: "15px", borderTop: "1px solid rgba(255,255,255,0.2)", textAlign: "left" }}>
              {/* <p><b>📄 File:</b> {extraData.filename}</p> */}
              <p><b>🛡️ Risk Level:</b> <span style={{ color: extraData.color_code, fontWeight: "bold" }}>{extraData.risk_level}</span></p>
              <p><b>📊 Confidence:</b> {(extraData.confidence_avg).toFixed(1)}%</p>
              {/* <p><b>🔑 Hash:</b> <span style={{ fontSize: "0.75em", fontFamily: "monospace", wordBreak: "break-all" }}>{extraData.file_hash}</span></p> */}
            </div>
          )}
        </div>
      )}
    </div>
    </div>
  );
}

export default App;