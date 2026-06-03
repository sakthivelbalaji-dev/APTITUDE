import { createContext, useContext, useState, useCallback } from 'react'

const StudentContext = createContext(null)

export function StudentProvider({ children }) {
  const [student, setStudent] = useState(() => {
    const saved = sessionStorage.getItem('student')
    return saved ? JSON.parse(saved) : null
  })
  const [questions, setQuestions] = useState(() => {
    const saved = sessionStorage.getItem('test_questions')
    return saved ? JSON.parse(saved) : []
  })
  const [currentIndex, setCurrentIndex] = useState(0)
  const [answers, setAnswers] = useState(() => {
    const saved = sessionStorage.getItem('test_answers')
    return saved ? JSON.parse(saved) : {}
  })
  const [testStartedAt, setTestStartedAt] = useState(() => {
    return sessionStorage.getItem('test_started_at') || null
  })
  const [durationMinutes, setDurationMinutes] = useState(30)

  const persistStudent = useCallback((s) => {
    setStudent(s)
    if (s) sessionStorage.setItem('student', JSON.stringify(s))
    else sessionStorage.removeItem('student')
  }, [])

  const initTest = useCallback((data) => {
    setQuestions(data.questions)
    setDurationMinutes(data.duration_minutes)
    const now = Date.now().toString()
    setTestStartedAt(now)
    setCurrentIndex(0)
    setAnswers({})
    sessionStorage.setItem('test_questions', JSON.stringify(data.questions))
    sessionStorage.setItem('test_started_at', now)
    sessionStorage.setItem('test_answers', '{}')
  }, [])

  const setAnswer = useCallback((questionId, option) => {
    setAnswers((prev) => {
      const next = { ...prev, [questionId]: option }
      sessionStorage.setItem('test_answers', JSON.stringify(next))
      return next
    })
  }, [])

  const clearTest = useCallback(() => {
    setQuestions([])
    setCurrentIndex(0)
    setAnswers({})
    setTestStartedAt(null)
    sessionStorage.removeItem('test_questions')
    sessionStorage.removeItem('test_started_at')
    sessionStorage.removeItem('test_answers')
  }, [])

  const value = {
    student,
    setStudent: persistStudent,
    questions,
    currentIndex,
    setCurrentIndex,
    answers,
    setAnswer,
    testStartedAt,
    durationMinutes,
    initTest,
    clearTest,
  }

  return (
    <StudentContext.Provider value={value}>
      {children}
    </StudentContext.Provider>
  )
}

export function useStudent() {
  const ctx = useContext(StudentContext)
  if (!ctx) throw new Error('useStudent must be used within StudentProvider')
  return ctx
}
