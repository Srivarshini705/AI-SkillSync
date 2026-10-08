import { Outlet } from 'react-router'
import Navbar from './Navbar'

function Layout() {
  return (
    <>
      <Navbar />

      <main className="app-content">
        <Outlet />
      </main>
    </>
  )
}

export default Layout