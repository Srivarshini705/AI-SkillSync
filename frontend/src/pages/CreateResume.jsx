import './CreateResume.css'

function CreateResume() {
  return (
    <div className="resume-page">
      <div className="resume-header">
        <h1>Create Your Resume</h1>
        <p>
          Enter your details and let AI SkillSync help you build
          a professional resume.
        </p>
      </div>

      <form className="resume-form">
        <section className="resume-section">
          <h2>Personal Information</h2>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="fullName">Full Name</label>
              <input
                type="text"
                id="fullName"
                placeholder="Enter your full name"
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                placeholder="Enter your email"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="phone">Phone Number</label>
              <input
                type="tel"
                id="phone"
                placeholder="Enter your phone number"
              />
            </div>

            <div className="form-group">
              <label htmlFor="location">Location</label>
              <input
                type="text"
                id="location"
                placeholder="City, State"
              />
            </div>
          </div>
        </section>

        <section className="resume-section">
          <h2>Professional Summary</h2>

          <div className="form-group">
            <label htmlFor="summary">About You</label>
            <textarea
              id="summary"
              rows="5"
              placeholder="Write a short summary about yourself"
            ></textarea>
          </div>
        </section>

        <section className="resume-section">
          <h2>Education</h2>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="degree">Degree</label>
              <input
                type="text"
                id="degree"
                placeholder="B.Tech / B.Sc / etc."
              />
            </div>

            <div className="form-group">
              <label htmlFor="college">College</label>
              <input
                type="text"
                id="college"
                placeholder="College name"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="graduationYear">
                Graduation Year
              </label>
              <input
                type="text"
                id="graduationYear"
                placeholder="2027"
              />
            </div>

            <div className="form-group">
              <label htmlFor="score">CGPA / Percentage</label>
              <input
                type="text"
                id="score"
                placeholder="Enter your score"
              />
            </div>
          </div>
        </section>

        <section className="resume-section">
          <h2>Skills</h2>

          <div className="form-group">
            <label htmlFor="skills">Technical Skills</label>
            <textarea
              id="skills"
              rows="4"
              placeholder="Example: Python, React.js, FastAPI, SQL, Git"
            ></textarea>
          </div>
        </section>

        <section className="resume-section">
          <h2>Projects</h2>

          <div className="form-group">
            <label htmlFor="projects">Project Details</label>
            <textarea
              id="projects"
              rows="5"
              placeholder="Describe your projects"
            ></textarea>
          </div>
        </section>

        <section className="resume-section">
          <h2>Experience</h2>

          <div className="form-group">
            <label htmlFor="experience">Work / Internship Experience</label>
            <textarea
              id="experience"
              rows="5"
              placeholder="Describe your experience"
            ></textarea>
          </div>
        </section>

        <div className="resume-submit">
          <button type="submit">
            Generate Resume with AI
          </button>
        </div>
      </form>
    </div>
  )
}

export default CreateResume