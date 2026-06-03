import { useEffect, useState } from 'react'
import { adminApi } from '../../api/services'
import { Card, Input, Button } from '../../components/Layout'

export default function StudentsPage() {
  const [students, setStudents] = useState([])
  const [search, setSearch] = useState('')
  const [department, setDepartment] = useState('')
  const [selectedResult, setSelectedResult] = useState(null)

  const load = () => {
    adminApi.getStudents({ search: search || undefined, department: department || undefined })
      .then(({ data }) => setStudents(data))
      .catch(console.error)
  }

  useEffect(() => { load() }, [])

  const viewResult = async (id) => {
    try {
      const { data } = await adminApi.getStudentResult(id)
      setSelectedResult(data)
    } catch {
      alert('No completed result for this student')
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Student Management</h1>
      <Card className="mb-6">
        <div className="flex flex-col sm:flex-row gap-3">
          <Input placeholder="Search name or roll..." value={search} onChange={(e) => setSearch(e.target.value)} />
          <Input placeholder="Filter department" value={department} onChange={(e) => setDepartment(e.target.value)} />
          <Button className="sm:w-auto" onClick={load}>Search</Button>
        </div>
      </Card>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-slate-500 border-b border-capgemini-border">
              <th className="text-left py-2">Name</th>
              <th className="text-left py-2">Department</th>
              <th className="text-left py-2">Roll</th>
              <th className="text-left py-2">Action</th>
            </tr>
          </thead>
          <tbody>
            {students.map((s) => (
              <tr key={s.id} className="border-b border-capgemini-border/50">
                <td className="py-3">{s.name}</td>
                <td>{s.department}</td>
                <td>{s.roll_number}</td>
                <td>
                  <button onClick={() => viewResult(s.id)} className="text-capgemini-light hover:underline">
                    View Result
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedResult && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50" onClick={() => setSelectedResult(null)}>
          <Card className="max-w-md w-full" onClick={(e) => e.stopPropagation()}>
            <h3 className="font-bold mb-4">Result — {selectedResult.student_name}</h3>
            <p>Score: {selectedResult.score} / {selectedResult.total_questions}</p>
            <p>Percentage: {selectedResult.percentage}%</p>
            <p>Status: <strong>{selectedResult.status}</strong></p>
            <button className="mt-4 text-capgemini-light" onClick={() => setSelectedResult(null)}>Close</button>
          </Card>
        </div>
      )}
    </div>
  )
}
