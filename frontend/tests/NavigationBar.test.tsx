import { within } from "@testing-library/dom"
import userEvent from "@testing-library/user-event"

import { renderWithContexts as render, getAxiosMockAdapter } from "./helpers"
import NavigationBar from "../src/components/NavigationBar"

import { type FileData } from "../src/queries/files"

describe("NavigationBar", () => {
	describe("Upload functionality", () => {
		test("Renders the upload button", () => {
			const { getByText } = render(<NavigationBar />)
			getByText("Upload file")
		})

		test("Clicking the upload button and selecting a file POSTs the file", async () => {
			const axiosMock = getAxiosMockAdapter()
			const expectedUrlPattern = new RegExp("/files/$")
			axiosMock.onPost(expectedUrlPattern).reply(200, {
				id: "b61bf93d-a9db-473e-822e-a65003b1b7e3",
				filename: "test.txt",
				title: "test",
				size: 1,
			})

			const user = userEvent.setup()

			const { getByText, container } = render(<NavigationBar />)
			const uploadButton = getByText("Upload file")
			const mockFile = new File(["test"], "test.txt", { type: "text/plain" })

			const fileInput = container.querySelector('input[type="file"]')

			if (fileInput == null) throw Error("No")

			await user.upload(fileInput as HTMLInputElement, mockFile)

			const postRequests = axiosMock.history.post

			expect(postRequests.length).toEqual(1)

			const postRequest = postRequests[0]

			expect(postRequest.url).toMatch(expectedUrlPattern)
		})
	})
})
