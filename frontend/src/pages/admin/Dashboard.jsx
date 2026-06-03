import { useEffect, useState } from 'react'
import { adminApi } from '../../api/services'
import { Card } from '../../components/Layout'

const STAT_CARDS = [
  { key: 'total_students', label: 'Total Students', color: 'text-capgemini-light' },
  { key: 'completed_tests', label: 'Completed Tests', color: 'text-blue-400' },
  { key: 'passed', label: 'Passed', color: 'text-green-400' },
  { key: 'failed', label: 'Failed', color: 'text-amber-400' },
  { key: 'disqualified', label: 'Disqualified', color: 'text-red-400' },
]

export default function Dashboard() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    adminApi.getStats().then(({ data }) => setStats(data)).catch(console.error)
  }, [])

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6 gradient-text animate-scale-3d">Dashboard</h1>
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
        {STAT_CARDS.map(({ key, label, color }, i) => (
          <Card key={key} className="text-center animate-fade-in" style={{ animationDelay: `${i * 0.1}s` }}>
            <p className="text-slate-500 text-sm mb-1">{label}</p>
            <p className={`text-3xl font-bold ${color}`}>
              {stats ? stats[key] : '—'}
            </p>
          </Card>
        ))}
      </div>
    </div>
  )
}
