import { useEffect, useState } from 'react'
import { adminApi } from '../../api/services'
import { Card, Input, Button } from '../../components/Layout'

export default function ResultsPage() {
  const [results, setResults] = useState([])
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('')

  const load = () => {
    adminApi.getResults({
      search: search || undefined,
      status_filter: statusFilter || undefined,
    }).then(({ data }) => setResults(data))
  }

  useEffect(() => { load() }, [])

  const exportCsv = async () => {
    const { data } = await adminApi.exportCsv()
    const url = window.URL.createObjectURL(new Blob([data]))
    const a = document.createElement('a')
    a.href = url
    a.download = 'results_export.csv'
    a.click()
  }

  return (
    <div>
      <div className="flex flex-col sm:flex-row justify-between gap-4 mb-6">
        <h1 className="text-2xl font-bold">Results</h1>
        <Button className="sm:!w-auto" onClick={exportCsv}>Export CSV</Button>
      </div>

      <Card className="mb-6 flex flex-col sm:flex-row gap-3">
        <Input placeholder="Search..." value={search} onChange={(e) => setSearch(e.target.value)} />
        <select
          className="px-4 py-3 rounded-xl bg-capgemini-card border border-capgemini-border text-white"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="">All Status</option>
          <option value="PASS">PASS</option>
          <option value="FAIL">FAIL</option>
          <option value="DISQUALIFIED">DISQUALIFIED</option>
        </select>
        <Button className="sm:!w-auto" onClick={load}>Filter</Button>
      </Card>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-slate-500 border-b border-capgemini-border">
              <th className="text-left py-2">Name</th>
              <th className="text-left py-2">Roll</th>
              <th className="text-left py-2">Score</th>
              <th className="text-left py-2">%</th>
              <th className="text-left py-2">Status</th>
            </tr>
          </thead>
          <tbody>
            {results.map((r) => (
              <tr key={r.id} className="border-b border-capgemini-border/50">
                <td className="py-3">{r.student_name}</td>
                <td>{r.roll_number}</td>
                <td>{r.score}/{r.total_questions}</td>
                <td>{r.percentage}%</td>
                <td>
                  <span className={
                    r.status === 'PASS' ? 'text-green-400' :
                    r.status === 'DISQUALIFIED' ? 'text-red-400' : 'text-amber-400'
                  }>{r.status}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
