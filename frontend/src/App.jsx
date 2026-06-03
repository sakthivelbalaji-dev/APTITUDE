import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { StudentProvider } from './context/StudentContext'
import HomePage from './pages/HomePage'
import RulesPage from './pages/RulesPage'
import TestPage from './pages/TestPage'
import ResultPage from './pages/ResultPage'
import AdminLogin from './pages/admin/AdminLogin'
import AdminLayout from './pages/admin/AdminLayout'
import Dashboard from './pages/admin/Dashboard'
import StudentsPage from './pages/admin/StudentsPage'
import QuestionsPage from './pages/admin/QuestionsPage'
import ResultsPage from './pages/admin/ResultsPage'

export default function App() {
  return (
    <StudentProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/rules" element={<RulesPage />} />
          <Route path="/test" element={<TestPage />} />
          <Route path="/result" element={<ResultPage />} />
          <Route path="/result/:rollNumber" element={<ResultPage />} />
          <Route path="/admin">
            <Route index element={<AdminLogin />} />
            <Route element={<AdminLayout />}>
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="students" element={<StudentsPage />} />
              <Route path="questions" element={<QuestionsPage />} />
              <Route path="results" element={<ResultsPage />} />
            </Route>
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </StudentProvider>
  )
}
