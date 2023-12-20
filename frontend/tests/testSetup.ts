import "@testing-library/jest-dom"

// URL.createObjectURL does not exist in jest-jsdom.
globalThis.URL.createObjectURL = jest
	.fn()
	.mockImplementation(() => "http://localhost/downloadUrl")

// Clicking DOM objects is not implemented in jest-jsdom.
HTMLAnchorElement.prototype.click = jest.fn()
