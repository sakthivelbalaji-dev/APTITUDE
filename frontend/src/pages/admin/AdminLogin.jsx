import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { PageLayout, Card, Input, Button } from '../../components/Layout'
import { adminApi } from '../../api/services'

export default function AdminLogin() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const { data } = await adminApi.login(form)
      localStorage.setItem('admin_token', data.access_token)
      navigate('/admin/dashboard')
    } catch {
      setError('Invalid username or password')
    } finally {
      setLoading(false)
    }
  }

  return (
    <PageLayout>
      <h1 className="text-2xl font-bold text-center mb-2 gradient-text animate-scale-3d">
        Capgemini Assessment Management System
      </h1>
      <p className="text-center text-slate-400 mb-8">Admin Login</p>
      <Card className="max-w-md mx-auto">
        <form onSubmit={handleSubmit}>
          <Input
            label="Username"
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
            required
          />
          <Input
            label="Password"
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required
          />
          {error && <p className="text-red-400 text-sm mb-4 animate-fade-in">{error}</p>}
          <Button type="submit" disabled={loading}>
            {loading ? 'Signing in...' : 'Login'}
          </Button>
        </form>
      </Card>
    </PageLayout>
  )
}
