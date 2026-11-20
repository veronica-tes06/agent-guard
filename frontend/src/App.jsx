// The main (and so far only) component: shows the app title and whether the backend and database are reachable.

import { useEffect, useState } from 'react'

export default function App() {
  // State holding the response from /api/health. It starts as null (not loaded yet).
  // Calling setHealth updates it, and React re-renders the component.
  const [health, setHealth] = useState(null)

  // Runs once after the first render (the empty [] means "run only once").
  useEffect(() => {
    // The request goes to Vite, which forwards it to FastAPI (see vite.config.js).
    fetch('/api/health')
      .then((r) => r.json())   // parse the JSON response body
      .then(setHealth)         // store it in state, e.g. {api: "ok", database: "ok"}
      // If the request fails completely (backend not running), show that instead.
      .catch(() => setHealth({ api: 'unreachable', database: 'unknown' }))
  }, [])

  // JSX: HTML-like syntax that React turns into elements on the page.
  // Values inside {} are JavaScript. "…" is shown until the response arrives.
  return (
    <main style={{ fontFamily: 'system-ui', padding: '2rem' }}>
      <h1>AgentGuard</h1>
      <p>Guardrails for tool-using LLM agents.</p>
      <p>
        API: {health ? health.api : '…'} · Database: {health ? health.database : '…'}
      </p>
    </main>
  )
}
