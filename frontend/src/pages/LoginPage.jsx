import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { PageLayout, Card, Input, Button } from '../components/Layout'
import { studentApi } from '../api/services'
import { useStudent } from '../context/StudentContext'

export default function LoginPage() {
  const navigate = useNavigate()
  const { setStudent } = useStudent()
  const [form, setForm] = useState({
    name: '',
    department: '',
    roll_number: '',
    resume: null,
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    console.log('Starting registration...', form)
    try {
      const formData = new FormData()
      formData.append('name', form.name)
      formData.append('department', form.department)
      formData.append('roll_number', form.roll_number)
      if (form.resume) {
        formData.append('resume', form.resume)
      }

      console.log('Sending registration request...')
      const { data } = await studentApi.register(formData)
      console.log('Registration successful:', data)
      
      setStudent(data)
      console.log('Navigating to /rules...')
      navigate('/rules')
    } catch (err) {
      console.error('Registration error:', err)
      setError(err.response?.data?.detail || 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <PageLayout>
      <div className="text-center mb-8">
        <h1 className="text-2xl md:text-3xl font-bold gradient-text mb-3 animate-scale-3d">
          Student Registration
        </h1>
        <p className="text-slate-400 text-sm md:text-base leading-relaxed">
          Register to participate in the Capgemini Aptitude Assessment.
        </p>
      </div>

      <Card>
        <form onSubmit={handleSubmit}>
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
          <Input
            label="Roll Number"
            placeholder="Enter your roll number"
            value={form.roll_number}
            onChange={(e) => setForm({ ...form, roll_number: e.target.value })}
            required
          />
          <div className="mb-4">
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Resume (PDF, DOC, DOCX)
            </label>
            <input
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={(e) => setForm({ ...form, resume: e.target.files[0] })}
              className="w-full px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-slate-300 focus:outline-none focus:ring-2 focus:ring-capgemini-light"
            />
          </div>

          {error && (
            <div className="mb-4 p-4 rounded-xl bg-red-900/30 border border-red-500/50 text-red-300 text-sm animate-fade-in">
              {error}
            </div>
          )}

          <Button type="submit" disabled={loading}>
            {loading ? 'Processing...' : 'Register'}
          </Button>
        </form>

        <div className="mt-4 text-center">
          <button
            type="button"
            onClick={() => navigate('/profile')}
            className="text-capgemini-light text-sm hover:underline"
          >
            View My Profile
          </button>
        </div>
      </Card>
    </PageLayout>
  )
}
