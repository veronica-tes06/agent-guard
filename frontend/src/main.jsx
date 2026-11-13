// Entry point of the React app, loaded by index.html.
// Its only job is to attach React to the page and render the App component.

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'

// Find the empty <div id="root"> in index.html and render the app inside it.
createRoot(document.getElementById('root')).render(
  // StrictMode is a development-only helper that warns about common mistakes.
  // Side effect: in development, effects run twice, so /api/health is requested twice. This is normal.
  <StrictMode>
    <App />
  </StrictMode>
)
