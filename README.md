# 🔍 Lucid TRACE
### Technological Review of Artificial Content in Evidence

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

**Lucid TRACE** is a forensic Python tool designed to verify the authenticity of video evidence. It automates the detection of AI-generated content (deepfakes) by extracting random frames from video files and analyzing them against state-of-the-art detection models.

Unlike simple detectors that rely on averages, **Lucid TRACE** identifies "smoking gun" frames—single moments of manipulation that betray an otherwise realistic video.

---

## 🚀 Key Features

* **Stochastic Sampling:** Extracts random frames to prevent temporal overfitting (detects manipulation even if it only appears briefly).
* **Dual-Metric Analysis:** Calculates both **Average Confidence** (overall consistency) and **Max Spike** (worst-case frame) to catch subtle edits.
* **Cost-Efficient:** Smart limits on API calls to prevent overuse of credits while maintaining accuracy.
* **Format Agnostic:** Supports both static images (JPG, PNG) and video files (MP4, AVI, MOV).

---

## 🛠️ Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/lucid-trace.git](https://github.com/yourusername/lucid-trace.git)
    cd lucid-trace
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Keys**
    Create a `.env` file in the root directory and add your Sightengine credentials:
    ```env
    API_USER=your_sightengine_user_id
    API_SECRET=your_sightengine_secret_key
    ```

---

## 💻 Usage

Run the script directly on a video or image file:

```bash
python lucid_trace.py
