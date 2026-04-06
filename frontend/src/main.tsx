import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import posthog from 'posthog-js'
import './index.css'
import App from './App.tsx'

posthog.init('YOUR-POSTHOG-PROJECT-ID', {
  api_host: 'https://app.posthog.com',
  autocapture: false, // We'll manage captures manually to avoid noise
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

