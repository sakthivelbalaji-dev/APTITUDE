import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { PageLayout, Card, Input, Button } from '../components/Layout'
import { studentApi } from '../api/services'
import { useStudent } from '../context/StudentContext'

export default function HomePage() {
  const navigate = useNavigate()
  const { setStudent } = useStudent()
  const [form, setForm] = useState({ name: '', department: '', roll_number: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const { data } = await studentApi.login(form)
      if (data.already_completed) {
        setError(data.message || 'You have already attempted the test.')
        setLoading(false)
        return
      }
      setStudent(data.student)
      navigate('/rules')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <PageLayout>
      <div className="text-center mb-8">
        <h1 className="text-2xl md:text-3xl font-bold gradient-text mb-3 animate-scale-3d">
          Welcome to the Capgemini Aptitude Assessment Portal
        </h1>
        <p className="text-slate-400 text-sm md:text-base leading-relaxed">
          Evaluate your logical reasoning, quantitative aptitude, and problem-solving
          skills through a secure online assessment.
        </p>
      </div>

      <Card>
        <p className="text-capgemini-light text-sm mb-6 text-center">
          Welcome to the Capgemini Aptitude Assessment.
          Please ensure you have a stable internet connection and complete the test
          without leaving the assessment screen.
        </p>

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

          {error && (
            <div className="mb-4 p-4 rounded-xl bg-red-900/30 border border-red-500/50 text-red-300 text-sm animate-fade-in">
              {error}
            </div>
          )}

          <Button type="submit" disabled={loading}>
            {loading ? 'Validating...' : 'Continue to Rules'}
          </Button>
        </form>
      </Card>
    </PageLayout>
  )
}
