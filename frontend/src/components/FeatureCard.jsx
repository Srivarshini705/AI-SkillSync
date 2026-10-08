import { Link } from 'react-router'

function FeatureCard({ title, description, path }) {
  return (
    <Link
      to={path}
      className="feature-card"
    >
      <h2>{title}</h2>

      <p>{description}</p>

      <span>Open →</span>
    </Link>
  )
}

export default FeatureCard