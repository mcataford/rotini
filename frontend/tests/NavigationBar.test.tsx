import { within } from "@testing-library/dom"
import userEvent from "@testing-library/user-event"

import { renderWithContexts as render } from "./helpers"
import NavigationBar from "../src/components/NavigationBar"
import * as requestUtil from "../src/queries/requestUtils"
import { type FileData } from "../src/queries/files"

function applyMakeRequestMock<Schema>(
	impl: typeof requestUtil.default<Schema>,
) {
	return jest.spyOn(requestUtil, "default").mockImplementation(impl)
}

describe("NavigationBar", () => {
	describe("Upload functionality", () => {
		test("Renders the upload button", () => {
			const { getByText } = render(<NavigationBar />)
			getByText("Upload file")
		})

		test("Clicking the upload button and selecting a file POSTs the file", async () => {
			const spy = applyMakeRequestMock<FileData>(
				async (url: string, opts?: requestUtil.RequestOptions) => ({
					status: 200,
					json: {
						id: "b61bf93d-a9db-473e-822e-a65003b1b7e3",
						filename: "test.txt",
						title: "test",
						size: 1,
					},
				}),
			)

			const user = userEvent.setup()

			const { getByText, container } = render(<NavigationBar />)
			const uploadButton = getByText("Upload file")
			const mockFile = new File(["test"], "test.txt", { type: "text/plain" })

			const fileInput = container.querySelector('input[type="file"]')

			if (fileInput == null) throw Error("No")

			await user.upload(fileInput as HTMLInputElement, mockFile)

			expect(spy.mock.calls.length).toEqual(1)
			const call = spy.mock.lastCall

			if (!call || call.length !== 2) fail("No last call or wrong length.")

			expect(call[0]).toEqual("http://localhost:8000/files/")
			expect(call[1]?.method).toEqual("POST")
		})
	})
})
