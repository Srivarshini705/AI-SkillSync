import { Link } from 'react-router'
import './Login.css'

function Login() {
  return (
    <div className="login-page">
      <div className="login-card">
        <h1>AI SkillSync</h1>
        <p className="login-subtitle">
          Your AI-powered career assistant
        </p>

        <form>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              placeholder="Enter your email"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              placeholder="Enter your password"
            />
          </div>

          <button type="submit">
            Login
          </button>
        </form>
        <p className="signup-text">
          Don't have an account?{' '}
          <Link to="/signup">Sign up</Link>
          </p>
      </div>
    </div>
  )
}

export default Login