import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { PageLayout, Card, Button } from '../components/Layout'
import { useStudent } from '../context/StudentContext'
import { testApi } from '../api/services'

const RULES = [
  'Test can be attempted only once.',
  'Duration: 30 minutes.',
  'Total Questions: 30.',
  'No backward navigation.',
  'Switching tabs/apps will immediately disqualify the student.',
  'Test auto-submits when timer ends.',
]

export default function RulesPage() {
  const navigate = useNavigate()
  const { student, initTest } = useStudent()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  if (!student) {
    navigate('/')
    return null
  }

  const handleStart = async () => {
    setLoading(true)
    setError('')
    try {
      const { data } = await testApi.start(student.id)
      initTest(data)
      navigate('/test')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start test')
    } finally {
      setLoading(false)
    }
  }

  return (
    <PageLayout>
      <h1 className="text-2xl font-bold text-center mb-6">Test Rules</h1>
      <Card>
        <ul className="space-y-4 mb-8">
          {RULES.map((rule, i) => (
            <li key={i} className="flex gap-3 text-slate-300">
              <span className="text-capgemini-light font-bold shrink-0">{i + 1}.</span>
              <span>{rule}</span>
            </li>
          ))}
        </ul>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-red-900/30 text-red-300 text-sm">{error}</div>
        )}

        <Button onClick={handleStart} disabled={loading}>
          {loading ? 'Starting...' : 'I Agree and Start Test'}
        </Button>
      </Card>
    </PageLayout>
  )
}
