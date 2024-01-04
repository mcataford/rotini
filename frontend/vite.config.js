import legacy from "@vitejs/plugin-legacy"
import basicSSL from "@vitejs/plugin-basic-ssl"
import path from "node:path"
import { defineConfig } from "vite"

export default defineConfig({
	plugins: [legacy(), basicSSL()],
	build: {
		outDir: "./dist",
		rollupOptions: {
			external: "./src",
		},
	},
	server: {
		port: 1234,
		strictPort: true,
		https: false,
	},
	test: {
		environment: "jsdom",
		setupFiles: ["./src/tests/testSetup.ts"],
		include: ["./src/**/*.test.ts", "./src/**/*.test.tsx"],
		globals: true,
	},
	resolve: {
		alias: [
			{
				find: "@",
				replacement: path.resolve(__dirname, "./src"),
			},
		],
	},
})
