import { Link } from 'react-router'
import './Internships.css'

function Internships() {
  const internships = [
    {
      id: 1,
      title: 'AI / Machine Learning Intern',
      company: 'ABC Technologies',
      location: 'Remote',
      skills: ['Python', 'Machine Learning', 'SQL'],
      type: 'Internship',
    },
    {
      id: 2,
      title: 'Frontend Developer Intern',
      company: 'XYZ Solutions',
      location: 'Hyderabad',
      skills: ['React.js', 'JavaScript', 'HTML', 'CSS'],
      type: 'Internship',
    },
    {
      id: 3,
      title: 'Data Analyst Intern',
      company: 'DataWorks',
      location: 'Bangalore',
      skills: ['Python', 'SQL', 'Excel'],
      type: 'Internship',
    },
    {
      id: 4,
      title: 'Backend Developer Intern',
      company: 'TechLabs',
      location: 'Remote',
      skills: ['Python', 'FastAPI', 'Git'],
      type: 'Internship',
    },
  ]

  return (
    <div className="internships-page">
      <div className="internships-header">
        <h1>Internships</h1>
        <p>
          Find internship opportunities that match your skills and career goals.
        </p>
      </div>

      <div className="internship-search">
        <input
          type="text"
          placeholder="Search internships, companies, or skills..."
        />
      </div>

      <div className="internship-grid">
        {internships.map((internship) => (
          <div className="internship-card" key={internship.id}>
            <div className="internship-card-header">
              <span className="internship-type">
                {internship.type}
              </span>
            </div>

            <h2>{internship.title}</h2>

            <p className="company-name">
              {internship.company}
            </p>

            <p className="location">
              📍 {internship.location}
            </p>

            <div className="skill-list">
              {internship.skills.map((skill) => (
                <span className="skill-tag" key={skill}>
                  {skill}
                </span>
              ))}
            </div>

            <Link
              to={`/internships/${internship.id}`}
              className="view-internship"
            >
              View Details →
            </Link>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Internships