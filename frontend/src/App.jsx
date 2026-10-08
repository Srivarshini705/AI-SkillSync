import { Routes, Route } from 'react-router'
import Layout from './components/Layout'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import Signup from './pages/Signup'
import CreateResume from './pages/CreateResume'
import ATSScore from './pages/ATSScore'
import Internships from './pages/Internships'
import Jobs from './pages/Jobs'
import SkillGap from './pages/SkillGap'
import Chat from './pages/Chat'
function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />

      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/resume" element={<CreateResume />} />
        <Route path="/ats" element={<ATSScore />} />
        <Route path="/internships" element={<Internships />} />
        <Route path="/jobs" element={<Jobs />} />
        <Route path="/skill-gap" element={<SkillGap />} />
        <Route path="/chat" element={<Chat />} />
      </Route>
    </Routes>
  )
}

export default App