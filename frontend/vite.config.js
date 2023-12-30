import legacy from "@vitejs/plugin-legacy"
import basicSSL from "@vitejs/plugin-basic-ssl"

import { defineConfig } from "vite"

export default defineConfig({
	plugins: [legacy(), basicSSL()],
	server: {
		port: 1234,
		strictPort: true,
		https: false,
	},
	test: {
		environment: "jsdom",
		setupFiles: ["./src/tests/testSetup.ts"],
		testMatch: ["./src/**/*.test.tsx?"],
		globals: true,
	},
})
