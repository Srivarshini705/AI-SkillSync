import { useState } from 'react'
import './SkillGap.css'

function SkillGap() {
  const [career, setCareer] = useState('')
  const [skills, setSkills] = useState('')
  const [showResult, setShowResult] = useState(false)

  const currentSkills = skills
    .split(',')
    .map((skill) => skill.trim())
    .filter((skill) => skill !== '')

  const requiredSkills = [
    'Python',
    'SQL',
    'Git',
    'FastAPI',
    'REST APIs',
    'Docker',
  ]

  const missingSkills = requiredSkills.filter(
    (requiredSkill) =>
      !currentSkills.some(
        (skill) =>
          skill.toLowerCase() === requiredSkill.toLowerCase()
      )
  )

  function handleAnalyze(event) {
    event.preventDefault()

    if (career && currentSkills.length > 0) {
      setShowResult(true)
    }
  }

  return (
    <div className="skill-gap-page">
      <div className="skill-gap-header">
        <h1>Identify Skill Gap</h1>
        <p>
          Discover the skills you need for your target career.
        </p>
      </div>

      <form
        className="skill-gap-form"
        onSubmit={handleAnalyze}
      >
        <div className="skill-gap-card">
          <div className="form-group">
            <label htmlFor="career">
              Target Career
            </label>

            <select
              id="career"
              value={career}
              onChange={(event) => setCareer(event.target.value)}
            >
              <option value="">
                Select a career
              </option>
              <option value="Python Developer">
                Python Developer
              </option>
              <option value="Frontend Developer">
                Frontend Developer
              </option>
              <option value="Data Analyst">
                Data Analyst
              </option>
              <option value="Machine Learning Engineer">
                Machine Learning Engineer
              </option>
              <option value="AI Engineer">
                AI Engineer
              </option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="skills">
              Your Current Skills
            </label>

            <textarea
              id="skills"
              value={skills}
              onChange={(event) => setSkills(event.target.value)}
              placeholder="Example: Python, SQL, Git"
              rows="5"
            />

            <small>
              Separate each skill using a comma.
            </small>
          </div>

          <button type="submit">
            Analyze Skill Gap
          </button>
        </div>
      </form>

      {showResult && (
        <div className="skill-gap-results">
          <div className="result-section">
            <h2>Your Current Skills</h2>

            <div className="skill-tags">
              {currentSkills.map((skill) => (
                <span className="current-skill" key={skill}>
                  ✓ {skill}
                </span>
              ))}
            </div>
          </div>

          <div className="result-section">
            <h2>Missing Skills</h2>

            <div className="skill-tags">
              {missingSkills.length > 0 ? (
                missingSkills.map((skill) => (
                  <span className="missing-skill" key={skill}>
                    ✗ {skill}
                  </span>
                ))
              ) : (
                <p>
                  Great! You already have the required skills.
                </p>
              )}
            </div>
          </div>

          <div className="result-section roadmap-section">
            <h2>Your Learning Roadmap</h2>

            {missingSkills.length > 0 ? (
              <ol>
                {missingSkills.map((skill) => (
                  <li key={skill}>
                    Learn <strong>{skill}</strong>
                  </li>
                ))}
              </ol>
            ) : (
              <p>
                Focus on projects and interview preparation.
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default SkillGap