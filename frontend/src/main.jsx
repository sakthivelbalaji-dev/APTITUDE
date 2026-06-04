import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'

console.log('React app initializing...')

const rootElement = document.getElementById('root')
if (!rootElement) {
  console.error('Root element not found!')
} else {
  console.log('Root element found, mounting React app')
  createRoot(rootElement).render(
    <StrictMode>
      <App />
    </StrictMode>,
  )
}
