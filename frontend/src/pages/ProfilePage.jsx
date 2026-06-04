import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { PageLayout, Card, Button } from '../components/Layout'
import { resultApi } from '../api/services'

function StatusBadge({ status }) {
  const styles = {
    PASS: 'bg-green-900/40 text-green-400 border-green-500/50',
    FAIL: 'bg-amber-900/40 text-amber-400 border-amber-500/50',
    DISQUALIFIED: 'bg-red-900/40 text-red-400 border-red-500/50',
  }
  return (
    <span className={`inline-block px-3 py-1 rounded-full border font-bold text-xs ${styles[status] || styles.FAIL}`}>
      {status}
    </span>
  )
}

export default function ProfilePage() {
  const navigate = useNavigate()
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)
  const [student, setStudent] = useState(null)

  useEffect(() => {
    const rollNumber = sessionStorage.getItem('last_roll')
    if (!rollNumber) {
      navigate('/')
      return
    }

    // Get student info from latest result
    resultApi.getHistory(rollNumber)
      .then(({ data }) => {
        if (data.length > 0) {
          setStudent({
            name: data[0].student_name,
            department: data[0].department,
            roll_number: data[0].roll_number,
          })
          setHistory(data)
        }
      })
      .catch(() => navigate('/'))
      .finally(() => setLoading(false))
  }, [navigate])

  if (loading) {
    return (
      <PageLayout>
        <p className="text-center text-slate-400">Loading profile...</p>
      </PageLayout>
    )
  }

  if (!student) {
    return (
      <PageLayout>
        <p className="text-center text-slate-400">No test history found</p>
        <Button onClick={() => navigate('/')} className="mt-4">Take Test</Button>
      </PageLayout>
    )
  }

  return (
    <PageLayout>
      <div className="text-center mb-6">
        <h1 className="text-2xl font-bold gradient-text mb-2 animate-scale-3d">My Profile</h1>
        <p className="text-slate-400 text-sm">View your test history and results</p>
      </div>

      <Card className="mb-6">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
          <div className="glass p-4 rounded-lg input-3d">
            <p className="text-slate-500 text-sm">Name</p>
            <p className="font-semibold text-capgemini-light">{student.name}</p>
          </div>
          <div className="glass p-4 rounded-lg input-3d">
            <p className="text-slate-500 text-sm">Department</p>
            <p className="font-semibold text-capgemini-light">{student.department}</p>
          </div>
          <div className="glass p-4 rounded-lg input-3d">
            <p className="text-slate-500 text-sm">Roll Number</p>
            <p className="font-semibold text-capgemini-light">{student.roll_number}</p>
          </div>
        </div>
      </Card>

      <h2 className="text-xl font-bold mb-4 gradient-text">Test History</h2>

      {history.length === 0 ? (
        <Card>
          <p className="text-center text-slate-400 mb-4">No test attempts yet</p>
          <Button onClick={() => navigate('/rules')} className="w-full">Start Test</Button>
        </Card>
      ) : (
        <div className="space-y-4">
          {history.map((result) => (
            <Card key={result.id} className="animate-fade-in">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-slate-500 text-sm">Attempt #{result.attempt_number}</span>
                    <StatusBadge status={result.status} />
                  </div>
                  {result.status === 'DISQUALIFIED' && result.disqualification_reason && (
                    <p className="text-red-400 text-xs mb-2">
                      Reason: {result.disqualification_reason.replace(/_/g, ' ')}
                    </p>
                  )}
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div>
                      <p className="text-slate-500">Score</p>
                      <p className="font-semibold gradient-text">{result.score} / {result.total_questions}</p>
                    </div>
                    <div>
                      <p className="text-slate-500">Percentage</p>
                      <p className="font-semibold gradient-text">{result.percentage}%</p>
                    </div>
                    <div>
                      <p className="text-slate-500">Date</p>
                      <p className="font-semibold text-capgemini-light">
                        {result.submitted_at ? new Date(result.submitted_at).toLocaleDateString() : 'N/A'}
                      </p>
                    </div>
                  </div>
                </div>
                <Button
                  onClick={() => navigate(`/result/${student.roll_number}`)}
                  className="sm:w-auto"
                >
                  View Details
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}

      <div className="mt-6 text-center">
        <Button onClick={() => navigate('/rules')} className="w-full sm:w-auto">
          Take New Test
        </Button>
      </div>
    </PageLayout>
  )
}
