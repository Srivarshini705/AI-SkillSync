import FeatureCard from '../components/FeatureCard'
import './Dashboard.css'

function Dashboard() {
  const features = [
    {
      title: 'Create Resume',
      description: 'Build a professional resume with AI assistance.',
      path: '/resume',
    },
    {
      title: 'ATS Score',
      description: 'Analyze your resume and check its ATS compatibility.',
      path: '/ats',
    },
    {
      title: 'Internships',
      description: 'Explore internship opportunities matched to your skills.',
      path: '/internships',
    },
    {
      title: 'Jobs',
      description: 'Find job opportunities that match your profile.',
      path: '/jobs',
    },
    {
      title: 'Identify Skill Gap',
      description: 'Discover missing skills for your target career.',
      path: '/skill-gap',
    },
    {
      title: 'Chat with SkillSync',
      description: 'Ask SkillSync for personalized career guidance.',
      path: '/chat',
    },
  ]

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <h1>AI SkillSync Dashboard</h1>

        <p>
          Choose a feature to improve your career journey.
        </p>
      </div>

      <div className="feature-grid">
        {features.map((feature) => (
          <FeatureCard
            key={feature.path}
            title={feature.title}
            description={feature.description}
            path={feature.path}
          />
        ))}
      </div>
    </div>
  )
}

export default Dashboard