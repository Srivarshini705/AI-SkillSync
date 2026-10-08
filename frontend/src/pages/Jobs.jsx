import { Link } from 'react-router'
import './Jobs.css'

function Jobs() {
  const jobs = [
    {
      id: 1,
      title: 'Junior Python Developer',
      company: 'TechNova',
      location: 'Hyderabad',
      skills: ['Python', 'SQL', 'Git', 'REST API'],
      type: 'Full Time',
    },
    {
      id: 2,
      title: 'Frontend Developer',
      company: 'WebCraft',
      location: 'Remote',
      skills: ['React.js', 'JavaScript', 'HTML', 'CSS'],
      type: 'Full Time',
    },
    {
      id: 3,
      title: 'Machine Learning Engineer',
      company: 'AI Labs',
      location: 'Bangalore',
      skills: ['Python', 'Machine Learning', 'TensorFlow'],
      type: 'Full Time',
    },
    {
      id: 4,
      title: 'Backend Developer',
      company: 'CloudWorks',
      location: 'Chennai',
      skills: ['Python', 'FastAPI', 'SQL', 'Git'],
      type: 'Full Time',
    },
  ]

  return (
    <div className="jobs-page">
      <div className="jobs-header">
        <h1>Jobs</h1>
        <p>
          Explore job opportunities that match your skills and career goals.
        </p>
      </div>

      <div className="job-search">
        <input
          type="text"
          placeholder="Search jobs, companies, or skills..."
        />
      </div>

      <div className="job-grid">
        {jobs.map((job) => (
          <div className="job-card" key={job.id}>
            <div className="job-card-header">
              <span className="job-type">
                {job.type}
              </span>
            </div>

            <h2>{job.title}</h2>

            <p className="job-company">
              {job.company}
            </p>

            <p className="job-location">
              📍 {job.location}
            </p>

            <div className="job-skill-list">
              {job.skills.map((skill) => (
                <span className="job-skill-tag" key={skill}>
                  {skill}
                </span>
              ))}
            </div>

            <Link
              to={`/jobs/${job.id}`}
              className="view-job"
            >
              View Details →
            </Link>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Jobs