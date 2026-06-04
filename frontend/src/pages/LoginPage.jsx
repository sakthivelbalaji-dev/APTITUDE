import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { PageLayout, Card, Input, Button } from '../components/Layout'
import { studentApi } from '../api/services'
import { useStudent } from '../context/StudentContext'

export default function LoginPage() {
  const navigate = useNavigate()
  const { setStudent } = useStudent()
  const [isLogin, setIsLogin] = useState(true)
  const [form, setForm] = useState({
    roll_number: '',
    password: '',
    name: '',
    department: '',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const endpoint = isLogin ? studentApi.login : studentApi.register
      const payload = isLogin
        ? { roll_number: form.roll_number, password: form.password }
        : {
            name: form.name,
            department: form.department,
            roll_number: form.roll_number,
            password: form.password,
          }
      const { data } = await endpoint(payload)
      
      localStorage.setItem('access_token', data.access_token)
      
      if (data.already_completed) {
        setError(data.message || 'You have already attempted the test.')
        setLoading(false)
        return
      }
      
      setStudent(data.student)
      navigate('/rules')
    } catch (err) {
      setError(err.response?.data?.detail || (isLogin ? 'Login failed. Please check your credentials.' : 'Registration failed. Please try again.'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <PageLayout>
      <div className="text-center mb-8">
        <h1 className="text-2xl md:text-3xl font-bold gradient-text mb-3 animate-scale-3d">
          {isLogin ? 'Login' : 'Register'}
        </h1>
        <p className="text-slate-400 text-sm md:text-base leading-relaxed">
          {isLogin
            ? 'Enter your credentials to access the Capgemini Aptitude Assessment.'
            : 'Create your account to participate in the Capgemini Aptitude Assessment.'}
        </p>
      </div>

      <Card>
        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <>
              <Input
                label="Full Name"
                placeholder="Enter your full name"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
              />
              <Input
                label="Department"
                placeholder="e.g. Computer Science"
                value={form.department}
                onChange={(e) => setForm({ ...form, department: e.target.value })}
                required
              />
            </>
          )}
          <Input
            label="Roll Number"
            placeholder="Enter your roll number"
            value={form.roll_number}
            onChange={(e) => setForm({ ...form, roll_number: e.target.value })}
            required
          />
          <Input
            label="Password"
            type="password"
            placeholder="Enter your password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required
          />

          {error && (
            <div className="mb-4 p-4 rounded-xl bg-red-900/30 border border-red-500/50 text-red-300 text-sm animate-fade-in">
              {error}
            </div>
          )}

          <Button type="submit" disabled={loading}>
            {loading ? 'Processing...' : isLogin ? 'Login' : 'Register'}
          </Button>
        </form>

        <div className="mt-4 text-center">
          <button
            type="button"
            onClick={() => {
              setIsLogin(!isLogin)
              setError('')
              setForm({ roll_number: '', password: '', name: '', department: '' })
            }}
            className="text-capgemini-light text-sm hover:underline"
          >
            {isLogin ? "Don't have an account? Register" : 'Already have an account? Login'}
          </button>
        </div>

        {isLogin && (
          <div className="mt-4 text-center">
            <button
              type="button"
              onClick={() => navigate('/profile')}
              className="text-capgemini-light text-sm hover:underline"
            >
              View My Profile
            </button>
          </div>
        )}
      </Card>
    </PageLayout>
  )
}
