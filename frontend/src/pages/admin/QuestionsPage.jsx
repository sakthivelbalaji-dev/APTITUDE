import { useEffect, useState } from 'react'
import { adminApi } from '../../api/services'
import { Card, Input, Button } from '../../components/Layout'

const EMPTY = {
  question: '', option_a: '', option_b: '', option_c: '', option_d: '',
  correct_answer: 'A', difficulty: 'easy', topic: '',
}

export default function QuestionsPage() {
  const [questions, setQuestions] = useState([])
  const [form, setForm] = useState(EMPTY)
  const [editId, setEditId] = useState(null)
  const [showForm, setShowForm] = useState(false)

  const load = () => adminApi.getQuestions().then(({ data }) => setQuestions(data))

  useEffect(() => { load() }, [])

  const handleSave = async (e) => {
    e.preventDefault()
    try {
      if (editId) {
        await adminApi.updateQuestion(editId, form)
      } else {
        await adminApi.createQuestion(form)
      }
      setForm(EMPTY)
      setEditId(null)
      setShowForm(false)
      load()
    } catch (err) {
      alert(err.response?.data?.detail || 'Save failed')
    }
  }

  const handleEdit = (q) => {
    setForm({
      question: q.question,
      option_a: q.option_a,
      option_b: q.option_b,
      option_c: q.option_c,
      option_d: q.option_d,
      correct_answer: q.correct_answer,
      difficulty: q.difficulty,
      topic: q.topic,
    })
    setEditId(q.id)
    setShowForm(true)
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this question?')) return
    await adminApi.deleteQuestion(id)
    load()
  }

  const handleBulkImport = () => {
    const raw = prompt('Paste JSON array of questions (QuestionCreate format)')
    if (!raw) return
    try {
      const data = JSON.parse(raw)
      adminApi.bulkImport(data).then(() => { alert('Imported'); load() })
    } catch {
      alert('Invalid JSON')
    }
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Question Management</h1>
        <div className="flex gap-2">
          <Button className="!w-auto px-4 py-2 text-sm" onClick={() => { setShowForm(true); setEditId(null); setForm(EMPTY) }}>Add</Button>
          <Button variant="secondary" className="!w-auto px-4 py-2 text-sm" onClick={handleBulkImport}>Bulk Import</Button>
        </div>
      </div>

      {showForm && (
        <Card className="mb-6">
          <form onSubmit={handleSave} className="space-y-3">
            <textarea
              className="w-full p-3 rounded-xl bg-capgemini-dark border border-capgemini-border text-white"
              placeholder="Question text"
              value={form.question}
              onChange={(e) => setForm({ ...form, question: e.target.value })}
              required
              rows={3}
            />
            {['a', 'b', 'c', 'd'].map((l) => (
              <Input
                key={l}
                placeholder={`Option ${l.toUpperCase()}`}
                value={form[`option_${l}`]}
                onChange={(e) => setForm({ ...form, [`option_${l}`]: e.target.value })}
                required
              />
            ))}
            <div className="flex gap-3 flex-wrap">
              <select
                className="px-3 py-2 rounded-lg bg-capgemini-dark border border-capgemini-border text-white"
                value={form.correct_answer}
                onChange={(e) => setForm({ ...form, correct_answer: e.target.value })}
              >
                {['A', 'B', 'C', 'D'].map((o) => <option key={o} value={o}>{o}</option>)}
              </select>
              <select
                className="px-3 py-2 rounded-lg bg-capgemini-dark border border-capgemini-border text-white"
                value={form.difficulty}
                onChange={(e) => setForm({ ...form, difficulty: e.target.value })}
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
              </select>
              <Input placeholder="Topic" value={form.topic} onChange={(e) => setForm({ ...form, topic: e.target.value })} />
            </div>
            <div className="flex gap-2">
              <Button type="submit" className="!w-auto">{editId ? 'Update' : 'Create'}</Button>
              <Button variant="secondary" type="button" className="!w-auto" onClick={() => setShowForm(false)}>Cancel</Button>
            </div>
          </form>
        </Card>
      )}

      <div className="space-y-3 max-h-[60vh] overflow-y-auto">
        {questions.map((q) => (
          <Card key={q.id} className="!p-4">
            <p className="text-sm text-capgemini-light mb-1">{q.difficulty} · {q.topic}</p>
            <p className="text-sm mb-2 line-clamp-2">{q.question}</p>
            <div className="flex gap-3 text-sm">
              <button onClick={() => handleEdit(q)} className="text-capgemini-light">Edit</button>
              <button onClick={() => handleDelete(q.id)} className="text-red-400">Delete</button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
