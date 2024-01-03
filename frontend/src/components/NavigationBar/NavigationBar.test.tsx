import { vi, it, describe, expect } from "vitest"
import { within } from "@testing-library/dom"
import userEvent from "@testing-library/user-event"
import { screen, render, waitFor } from "@testing-library/react"
import { QueryClientProvider, QueryClient } from "@tanstack/react-query"

import * as locationHook from "../../contexts/LocationContext"
import { getAxiosMockAdapter } from "../../tests/helpers"
import NavigationBar from "."

import { type FileData } from "../../types/files"

function renderComponent() {
	const wrapper = ({ children }: { children: React.ReactNode }) => (
		<QueryClientProvider client={new QueryClient()}>
			{children}
		</QueryClientProvider>
	)
	return {
		...render(<NavigationBar />, { wrapper }),
		user: userEvent.setup(),
	}
}

describe("NavigationBar", () => {
	describe("Upload functionality", () => {
		it("Renders the upload button", () => {
			renderComponent()
			expect(screen.queryByText("Upload file")).toBeInTheDocument()
		})

		it("Clicking the upload button and selecting a file POSTs the file", async () => {
			const axiosMock = getAxiosMockAdapter()
			const expectedUrlPattern = new RegExp("/files/$")
			axiosMock.onPost(expectedUrlPattern).reply(200, {
				id: "b61bf93d-a9db-473e-822e-a65003b1b7e3",
				filename: "test.txt",
				title: "test",
				size: 1,
			})

			const { user, container } = renderComponent()
			const uploadButton = screen.getByText("Upload file")
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

	describe("Log out", () => {
		it("renders a logout button", () => {
			renderComponent()

			expect(screen.queryByText("Log out")).toBeInTheDocument()

			const button = screen.getByText("Log out")
		})

		it("sends a logout request and redirects to the login page when logging out", async () => {
			const axiosMock = getAxiosMockAdapter()
			axiosMock.onDelete("/auth/session/").reply(204)
			const mockNavigate = vi.fn()
			const mockLocationHook = vi
				.spyOn(locationHook, "useLocationContext")
				.mockImplementation(() => ({
					location: {
						path: "",
						label: "",
						params: {},
						pattern: "",
					},
					navigate: mockNavigate,
				}))

			const { user } = renderComponent()

			const logoutButton = screen.getByText("Log out")

			await user.click(logoutButton)

			await waitFor(() => expect(axiosMock.history.delete.length).toEqual(1))
			expect(mockNavigate).toHaveBeenCalledWith("/login")
		})
	})
})
