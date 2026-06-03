import { useEffect, useRef, useCallback } from 'react'

/**
 * Monitors tab switch, blur, visibility changes, screenshot attempts, and AI tool usage patterns during the test.
 */
export function useAntiCheat(onViolation, enabled = true) {
  const triggered = useRef(false)
  const clipboardActivityCount = useRef(0)
  const copyStartTime = useRef(null)

  const disqualify = useCallback((reason) => {
    if (!enabled || triggered.current) return
    triggered.current = true
    onViolation(reason)
  }, [enabled, onViolation])

  useEffect(() => {
    if (!enabled) return

    const handleVisibility = () => {
      if (document.hidden) disqualify('TAB_SWITCH_DETECTED')
    }

    const handleBlur = () => disqualify('TAB_SWITCH_DETECTED')

    // Detect Print Screen key
    const handleKeyDown = (e) => {
      if (e.key === 'PrintScreen' || e.keyCode === 44) {
        e.preventDefault()
        disqualify('SCREENSHOT_DETECTED')
      }
      // Detect common AI tool shortcuts (Ctrl+Shift+I for dev tools, etc.)
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'I') {
        e.preventDefault()
        disqualify('DEV_TOOLS_DETECTED')
      }
    }

    // Detect clipboard paste (could indicate screenshot paste or AI-generated content)
    const handlePaste = (e) => {
      const items = e.clipboardData?.items
      if (items) {
        for (let i = 0; i < items.length; i++) {
          if (items[i].type.indexOf('image') !== -1) {
            e.preventDefault()
            disqualify('SCREENSHOT_DETECTED')
            break
          }
        }
      }
      // Check for large text pastes (could indicate AI-generated answers)
      const text = e.clipboardData?.getData('text')
      if (text && text.length > 500) {
        e.preventDefault()
        disqualify('SUSPICIOUS_CLIPBOARD_ACTIVITY')
      }
    }

    // Detect copy activity (could indicate copying questions to AI tools)
    const handleCopy = () => {
      clipboardActivityCount.current += 1
      if (!copyStartTime.current) {
        copyStartTime.current = Date.now()
      }
      // If multiple copies in short time, likely using AI tool
      if (clipboardActivityCount.current >= 3) {
        const timeElapsed = Date.now() - copyStartTime.current
        if (timeElapsed < 10000) { // 3 copies within 10 seconds
          disqualify('SUSPICIOUS_COPY_ACTIVITY')
        }
      }
    }

    // Detect selection changes (could indicate selecting text to copy to AI)
    const handleSelection = () => {
      const selection = window.getSelection()
      if (selection.toString().length > 100) {
        // Large text selection might indicate copying to AI
        clipboardActivityCount.current += 1
        if (!copyStartTime.current) {
          copyStartTime.current = Date.now()
        }
      }
    }

    document.addEventListener('visibilitychange', handleVisibility)
    window.addEventListener('blur', handleBlur)
    window.addEventListener('keydown', handleKeyDown)
    window.addEventListener('paste', handlePaste)
    window.addEventListener('copy', handleCopy)
    document.addEventListener('selectionchange', handleSelection)

    return () => {
      document.removeEventListener('visibilitychange', handleVisibility)
      window.removeEventListener('blur', handleBlur)
      window.removeEventListener('keydown', handleKeyDown)
      window.removeEventListener('paste', handlePaste)
      window.removeEventListener('copy', handleCopy)
      document.removeEventListener('selectionchange', handleSelection)
    }
  }, [enabled, disqualify])
}
