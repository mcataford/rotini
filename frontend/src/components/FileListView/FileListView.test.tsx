import { vi, expect, describe, it, afterEach } from "vitest"
import { render, screen, waitFor } from "@testing-library/react"
import { QueryClientProvider, QueryClient } from "@tanstack/react-query"
import AxiosMockAdapter from "axios-mock-adapter"

import axios from "@/axios"
import { LocationContext } from "@/contexts/LocationContext"
import FileListView from "."

const routes = {
	mock: "/item/:itemId",
}
function renderComponent() {
	render(
		<QueryClientProvider client={new QueryClient()}>
			<LocationContext routes={routes}>
				<FileListView />
			</LocationContext>
		</QueryClientProvider>,
	)
}

describe("FileListView", () => {
	afterEach(() => {
		vi.resetAllMocks()
	})

	it("renders no sidebar if no item is in the path", async () => {
		vi.spyOn(globalThis, "location", "get").mockReturnValue({
			...globalThis.location,
			pathname: "/",
		})

		const axiosMockAdapter = new AxiosMockAdapter(axios)

		axiosMockAdapter.onGet("/files/").reply(200, [
			{
				title: "Item 1",
				filename: "item1.txt",
				size: 1,
				id: "b61bf93d-a9db-473e-822e-a65003b1b7e3",
			},
		])

		renderComponent()

		await waitFor(() =>
			expect(screen.queryByText(/loading/i)).not.toBeInTheDocument(),
		)

		expect(
			screen.queryByLabelText("item details sidebar"),
		).not.toBeInTheDocument()
	})

	it("renders a sidebar if an item is selected", async () => {
		const mockItemId = "b61bf93d-a9db-473e-822e-a65003b1b7e3"
		vi.spyOn(globalThis, "location", "get").mockReturnValue({
			...globalThis.location,
			pathname: `/item/${mockItemId}/`,
		})

		const axiosMockAdapter = new AxiosMockAdapter(axios)

		axiosMockAdapter.onGet("/files/").reply(200, [
			{
				title: "Item 1",
				filename: "item1.txt",
				size: 1,
				id: mockItemId,
			},
		])

		axiosMockAdapter.onGet(`/files/${mockItemId}/`).reply(200, {
			title: "Item 1",
			filename: "item1.txt",
			size: 1,
			id: mockItemId,
		})

		renderComponent()

		await waitFor(() =>
			expect(screen.queryByText(/loading/i)).not.toBeInTheDocument(),
		)
		await waitFor(() =>
			expect(screen.queryByLabelText(/file details/i)).toBeInTheDocument(),
		)

		expect(screen.queryByLabelText("item details sidebar")).toBeInTheDocument()
	})
})
