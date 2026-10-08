import { useState } from 'react'
import './ATSScore.css'

function ATSScore() {
  const [selectedFile, setSelectedFile] = useState(null)

  function handleFileChange(event) {
    const file = event.target.files[0]

    if (file) {
      setSelectedFile(file)
    }
  }

  return (
    <div className="ats-page">
      <div className="ats-header">
        <h1>ATS Resume Score</h1>
        <p>
          Upload your resume and check how well it matches ATS requirements.
        </p>
      </div>

      <div className="ats-upload-card">
        <h2>Upload Your Resume</h2>

        <p className="upload-description">
          Upload your resume in PDF format to analyze its ATS compatibility.
        </p>

        <label htmlFor="resume-upload" className="upload-box">
          <span className="upload-icon">↑</span>

          <strong>Choose your resume</strong>

          <span>PDF files only</span>

          <input
            type="file"
            id="resume-upload"
            accept=".pdf,application/pdf"
            onChange={handleFileChange}
          />
        </label>

        {selectedFile && (
          <div className="selected-file">
            <strong>Selected file:</strong>
            <span>{selectedFile.name}</span>
          </div>
        )}

        <button
          type="button"
          className="analyze-button"
          disabled={!selectedFile}
        >
          Analyze Resume
        </button>
      </div>
    </div>
  )
}

export default ATSScore