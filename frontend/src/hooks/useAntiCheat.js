import { useEffect, useRef, useCallback } from 'react'

/**
 * Monitors tab switch, blur, and visibility changes during the test.
 */
export function useAntiCheat(onViolation, enabled = true) {
  const triggered = useRef(false)

  const disqualify = useCallback(() => {
    if (!enabled || triggered.current) return
    triggered.current = true
    onViolation('TAB_SWITCH_DETECTED')
  }, [enabled, onViolation])

  useEffect(() => {
    if (!enabled) return

    const handleVisibility = () => {
      if (document.hidden) disqualify()
    }

    const handleBlur = () => disqualify()

    document.addEventListener('visibilitychange', handleVisibility)
    window.addEventListener('blur', handleBlur)

    return () => {
      document.removeEventListener('visibilitychange', handleVisibility)
      window.removeEventListener('blur', handleBlur)
    }
  }, [enabled, disqualify])
}
