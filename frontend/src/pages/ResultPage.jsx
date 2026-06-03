import { useEffect, useState } from 'react'
import { useNavigate, useParams, useLocation } from 'react-router-dom'
import { PageLayout, Card } from '../components/Layout'
import { resultApi } from '../api/services'

function StatusBadge({ status }) {
  const styles = {
    PASS: 'bg-green-900/40 text-green-400 border-green-500/50 animate-glow',
    FAIL: 'bg-amber-900/40 text-amber-400 border-amber-500/50',
    DISQUALIFIED: 'bg-red-900/40 text-red-400 border-red-500/50 animate-glow',
  }
  return (
    <span className={`inline-block px-4 py-2 rounded-full border font-bold ${styles[status] || styles.FAIL}`}>
      {status}
    </span>
  )
}

export default function ResultPage() {
  const { rollNumber } = useParams()
  const location = useLocation()
  const navigate = useNavigate()
  const [result, setResult] = useState(location.state?.result || null)
  const [loading, setLoading] = useState(!location.state?.result)

  useEffect(() => {
    if (result) return
    const roll = rollNumber || sessionStorage.getItem('last_roll')
    if (!roll) {
      navigate('/')
      return
    }
    resultApi.getByRoll(roll)
      .then(({ data }) => setResult(data))
      .catch(() => navigate('/'))
      .finally(() => setLoading(false))
  }, [rollNumber, result, navigate])

  if (loading) {
    return (
      <PageLayout>
        <p className="text-center text-slate-400">Loading results...</p>
      </PageLayout>
    )
  }

  if (!result) return null

  return (
    <PageLayout>
      <div className="text-center mb-6">
        <h1 className="text-2xl font-bold gradient-text mb-2 animate-scale-3d">Your Result</h1>
        <p className="text-slate-400 text-sm">
          Thank you for participating in the Capgemini Aptitude Assessment.
          Your results have been successfully recorded.
        </p>
      </div>

      <Card className="space-y-4">
        <div className="text-center mb-6">
          <StatusBadge status={result.status} />
        </div>

        {result.status === 'DISQUALIFIED' && result.disqualification_reason && (
          <div className="bg-red-900/20 border border-red-500/50 rounded-lg p-4 mb-4 animate-fade-in">
            <p className="text-red-400 text-sm text-center font-semibold">
              ⚠️ Disqualified: {result.disqualification_reason.replace(/_/g, ' ')}
            </p>
          </div>
        )}

        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="glass p-3 rounded-lg input-3d">
            <p className="text-slate-500">Name</p>
            <p className="font-semibold">{result.student_name}</p>
          </div>
          <div className="glass p-3 rounded-lg input-3d">
            <p className="text-slate-500">Roll Number</p>
            <p className="font-semibold">{result.roll_number}</p>
          </div>
          <div className="glass p-3 rounded-lg col-span-2 input-3d">
            <p className="text-slate-500">Department</p>
            <p className="font-semibold">{result.department}</p>
          </div>
          <div className="glass p-3 rounded-lg col-span-2 text-center input-3d">
            <p className="text-slate-500">Score</p>
            <p className="font-semibold gradient-text text-2xl">{result.score} / {result.total_questions}</p>
          </div>
          <div className="glass p-3 rounded-lg input-3d">
            <p className="text-slate-500">Correct</p>
            <p className="font-semibold text-green-400">{result.correct_answers}</p>
          </div>
          <div className="glass p-3 rounded-lg input-3d">
            <p className="text-slate-500">Wrong</p>
            <p className="font-semibold text-red-400">{result.wrong_answers}</p>
          </div>
          <div className="glass p-3 rounded-lg col-span-2 text-center input-3d">
            <p className="text-slate-500">Percentage</p>
            <p className="text-3xl font-bold gradient-text">{result.percentage}%</p>
          </div>
        </div>

        <p className="text-center text-xs text-slate-500 pt-4">
          Pass criteria: 50% or more
        </p>
      </Card>
    </PageLayout>
  )
}
