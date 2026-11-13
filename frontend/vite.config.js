// Vite configuration. Vite is the tool that runs the React app during development and builds it for production.
//
// package.json (JSON, which can't contain comments) lists:
//   - scripts:          npm run dev / build / preview, each runs a Vite command
//   - dependencies:     react and react-dom, which run in the browser
//   - devDependencies:  vite and @vitejs/plugin-react, only needed while developing

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  // Lets Vite understand JSX and update the page instantly when a file is saved.
  plugins: [react()],

  server: {
    // Any request starting with /api is forwarded to the FastAPI backend on port 8000.
    proxy: { '/api': 'http://localhost:8000' },
  },
})
