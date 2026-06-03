import { useState, useEffect, useCallback } from 'react'

export function useTimer(durationMinutes, startedAt, onExpire) {
  const totalSeconds = durationMinutes * 60

  const getRemaining = useCallback(() => {
    if (!startedAt) return totalSeconds
    const elapsed = Math.floor((Date.now() - parseInt(startedAt, 10)) / 1000)
    return Math.max(0, totalSeconds - elapsed)
  }, [startedAt, totalSeconds])

  const [remaining, setRemaining] = useState(getRemaining)

  useEffect(() => {
    setRemaining(getRemaining())
    const interval = setInterval(() => {
      const r = getRemaining()
      setRemaining(r)
      if (r <= 0) {
        clearInterval(interval)
        onExpire?.()
      }
    }, 1000)
    return () => clearInterval(interval)
  }, [startedAt, getRemaining, onExpire])

  const minutes = Math.floor(remaining / 60)
  const seconds = remaining % 60
  const formatted = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
  const isWarning = remaining <= 300 && remaining > 0

  return { remaining, formatted, isWarning, isExpired: remaining <= 0 }
}
