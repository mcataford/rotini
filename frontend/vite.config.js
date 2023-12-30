import legacy from '@vitejs/plugin-legacy'
import react from '@vitejs/plugin-react'
import basicSSL from '@vitejs/plugin-basic-ssl'

import { defineConfig } from 'vite'

export default defineConfig({
    plugins: [legacy(), react(), basicSSL()],
    server: {
        port: 1234,
        strictPort: true,
        https: false
    }
})
