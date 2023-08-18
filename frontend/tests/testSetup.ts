// URL.createObjectURL does not exist in jest-jsdom.
globalThis.URL.createObjectURL = jest
	.fn()
	.mockImplementation(() => "http://localhost/downloadUrl")
