import { vi } from "vitest"
import "@testing-library/jest-dom"

// URL.createObjectURL does not exist in jest-jsdom.
globalThis.URL.createObjectURL = vi
	.fn()
	.mockImplementation(() => "http://localhost/downloadUrl")

// Clicking DOM objects is not implemented in jest-jsdom.
HTMLAnchorElement.prototype.click = vi.fn()
