import { Link, Outlet, useNavigate, useLocation } from 'react-router-dom'
import { Logo } from '../../components/Layout'

const NAV = [
  { to: '/admin/dashboard', label: 'Dashboard' },
  { to: '/admin/students', label: 'Students' },
  { to: '/admin/questions', label: 'Questions' },
  { to: '/admin/results', label: 'Results' },
]

export default function AdminLayout() {
  const navigate = useNavigate()
  const location = useLocation()

  const logout = () => {
    localStorage.removeItem('admin_token')
    navigate('/admin')
  }

  if (!localStorage.getItem('admin_token')) {
    navigate('/admin')
    return null
  }

  return (
    <div className="min-h-screen bg-capgemini-dark flex flex-col md:flex-row">
      <aside className="md:w-56 glass border-b md:border-b-0 md:border-r border-capgemini-border p-4 shrink-0">
        <Logo className="h-7 mb-6 animate-float-3d" />
        <p className="text-xs text-slate-500 mb-4 hidden md:block">Admin Panel</p>
        <nav className="flex md:flex-col gap-2 overflow-x-auto">
          {NAV.map(({ to, label }) => (
            <Link
              key={to}
              to={to}
              className={`px-4 py-2 rounded-lg text-sm whitespace-nowrap transition input-3d ${
                location.pathname === to
                  ? 'gradient-bg text-white'
                  : 'text-slate-400 hover:bg-capgemini-dark'
              }`}
            >
              {label}
            </Link>
          ))}
        </nav>
        <button
          onClick={logout}
          className="mt-4 w-full text-left px-4 py-2 text-sm text-red-400 hover:bg-red-900/20 rounded-lg transition"
        >
          Logout
        </button>
      </aside>
      <main className="flex-1 p-4 md:p-8 overflow-auto animate-slide-in-3d">
        <Outlet />
      </main>
    </div>
  )
}
