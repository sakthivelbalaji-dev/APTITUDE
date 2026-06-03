import { useState, useCallback, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { Logo, Button } from '../components/Layout'
import { useStudent } from '../context/StudentContext'
import { useTimer } from '../hooks/useTimer'
import { useAntiCheat } from '../hooks/useAntiCheat'
import { testApi } from '../api/services'

export default function TestPage() {
  const navigate = useNavigate()
  const {
    student,
    questions,
    currentIndex,
    setCurrentIndex,
    answers,
    setAnswer,
    testStartedAt,
    durationMinutes,
    clearTest,
  } = useStudent()

  const [submitting, setSubmitting] = useState(false)
  const submittedRef = useRef(false)

  const submitTest = useCallback(async (disqualified = false, reason = null) => {
    if (submittedRef.current || !student) return
    submittedRef.current = true
    setSubmitting(true)
    try {
      const { data } = await testApi.submit({
        studentId: student.id,
        disqualified,
        disqualificationReason: reason,
      })
      sessionStorage.setItem('last_roll', student.roll_number)
      clearTest()
      navigate('/result', { state: { result: data } })
    } catch {
      navigate(`/result/${student.roll_number}`)
    }
  }, [student, clearTest, navigate])

  const handleExpire = useCallback(() => {
    submitTest(false, null)
  }, [submitTest])

  const { formatted, isWarning, isExpired } = useTimer(
    durationMinutes,
    testStartedAt,
    handleExpire
  )

  const handleViolation = useCallback((reason) => {
    submitTest(true, reason)
  }, [submitTest])

  useAntiCheat(handleViolation, !submitting && !submittedRef.current)

  if (!student || questions.length === 0) {
    navigate('/')
    return null
  }

  if (isExpired && !submittedRef.current) {
    handleExpire()
    return null
  }

  const question = questions[currentIndex]
  const selected = answers[question.id]
  const progress = ((currentIndex + 1) / questions.length) * 100
  const isLast = currentIndex === questions.length - 1

  const handleSelect = async (option) => {
    setAnswer(question.id, option)
    try {
      await testApi.saveAnswer({
        studentId: student.id,
        questionId: question.id,
        selectedOption: option,
      })
    } catch {
      /* auto-save best effort */
    }
  }

  const handleNext = () => {
    if (!isLast) setCurrentIndex(currentIndex + 1)
  }

  const handleSubmitClick = () => {
    if (window.confirm('Are you sure you want to submit the test?')) {
      submitTest(false, null)
    }
  }

  return (
    <div className="min-h-screen bg-capgemini-dark flex flex-col fixed inset-0 z-50">
      <header className="px-4 py-3 glass border-b border-capgemini-border shrink-0">
        <div className="flex items-center justify-between gap-2 mb-2">
          <Logo className="h-6 animate-float-3d" />
          <span className={`font-mono text-lg font-bold ${isWarning ? 'timer-warning' : 'gradient-text'}`}>
            {formatted}
          </span>
        </div>
        <div className="flex justify-between text-xs text-slate-400 mb-2">
          <span>{student.name}</span>
          <span>{student.roll_number}</span>
        </div>
        <div className="h-2 bg-capgemini-border rounded-full overflow-hidden">
          <div
            className="h-full gradient-bg transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
        <p className="text-xs text-slate-500 mt-1 text-center">
          Question {currentIndex + 1} of {questions.length}
        </p>
      </header>

      <main className="flex-1 overflow-y-auto px-4 py-6">
        <div className="glass border border-capgemini-border rounded-2xl p-5 animate-slide-in-3d card-3d">
          <p className="text-capgemini-light text-sm font-medium mb-2">
            Q{currentIndex + 1} · {question.difficulty} · {question.topic}
          </p>
          <h2 className="text-lg font-semibold text-white mb-6 leading-relaxed">
            {question.question}
          </h2>

          <div className="space-y-3">
            {['A', 'B', 'C', 'D'].map((opt) => {
              const key = `option_${opt.toLowerCase()}`
              const text = question[key]
              const isSelected = selected === opt
              return (
                <button
                  key={opt}
                  type="button"
                  onClick={() => handleSelect(opt)}
                  disabled={submitting}
                  className={`w-full text-left p-4 rounded-xl border transition-all input-3d ${
                    isSelected
                      ? 'border-capgemini-light bg-capgemini/20 text-white animate-glow'
                      : 'border-capgemini-border glass text-slate-300 hover:border-capgemini-light'
                  }`}
                >
                  <span className="font-bold text-capgemini-light mr-2">{opt}.</span>
                  {text}
                </button>
              )
            })}
          </div>
        </div>
      </main>

      <footer className="p-4 glass border-t border-capgemini-border shrink-0 flex gap-3">
        {!isLast && (
          <Button onClick={handleNext} disabled={!selected || submitting}>
            Next
          </Button>
        )}
        <Button
          variant={isLast ? 'primary' : 'secondary'}
          onClick={handleSubmitClick}
          disabled={submitting}
        >
          {submitting ? 'Submitting...' : 'Submit Test'}
        </Button>
      </footer>
    </div>
  )
}
