import { expect, describe, it, vi } from "vitest"
import { within } from "@testing-library/dom"
import userEvent from "@testing-library/user-event"

import {
	renderWithContexts as render,
	getAxiosMockAdapter,
} from "../../tests/helpers"
import FileList from "."
import AxiosMockAdapter from "axios-mock-adapter"

describe("FileList", () => {
	const mockItems = [
		{
			title: "Item 1",
			filename: "item1.txt",
			size: 1,
			id: "b61bf93d-a9db-473e-822e-a65003b1b7e3",
		},
		{
			title: "Item 2",
			filename: "item2.txt",
			size: 1,
			id: "b61bf93d-a9db-473e-822e-a65003b1b7e4",
		},
	]

	const mockAsyncTasks = [
		{ title: "Async Item 0", filename: "async.txt", size: 2, type: "upload" },
	]

	it("Renders list items provided", () => {
		const { getAllByText } = render(<FileList data={mockItems} />)
		const renderedItems = getAllByText(/Item/)

		expect(renderedItems.length).toEqual(mockItems.length)
	})

	it("Prepends items in flight as tracked by async task context", () => {
		const { getAllByText, getByText } = render(
			<FileList data={[mockItems[0]]} />,
			{ asyncTaskContext: mockAsyncTasks },
		)

		const renderedItems = getAllByText(/Item/)

		expect(renderedItems.length).toEqual(2)

		within(renderedItems[0]).getByText(mockAsyncTasks[0].title)
		within(renderedItems[1]).getByText(mockItems[0].title)
	})

	describe("FileListItem", () => {
		it("Renders the item title", () => {
			const { getByLabelText, debug } = render(
				<FileList data={[mockItems[0]]} />,
			)
			const title = getByLabelText("item title")
			within(title).getByText(mockItems[0].title)
		})

		it("Renders the item size", () => {
			const { getByLabelText, debug } = render(
				<FileList data={[mockItems[0]]} />,
			)
			const title = getByLabelText("item size")
			within(title).getByText(`${mockItems[0].size} B`)
		})

		it.each(["download item", "delete item"])(
			"Renders secondary action buttons (%s)",
			(action) => {
				const { getByLabelText, debug } = render(
					<FileList data={[mockItems[0]]} />,
				)
				getByLabelText(action)
			},
		)

		it("Clicking the delete button fires request to delete file", async () => {
			const expectedUrlPattern = new RegExp(`/files/${mockItems[0].id}/$`)

			const axiosMock = getAxiosMockAdapter()

			axiosMock.onDelete(expectedUrlPattern).reply(200, mockItems[0])

			const user = userEvent.setup()

			const { getByLabelText, debug } = render(
				<FileList data={[mockItems[0]]} />,
			)
			const deleteButton = getByLabelText("delete item")

			await user.click(deleteButton)

			const deleteRequests = axiosMock.history.delete

			expect(deleteRequests.length).toEqual(1)

			const deleteRequest = deleteRequests[0]

			expect(deleteRequest.url).toMatch(expectedUrlPattern)
		})

		it("Clicking the download button trigger a file download", async () => {
			// FIXME: Validating file downloads is ... tricky. The current interaction with dynamically created DOM
			// elements is not visible by vi.
			const expectedUrlPattern = new RegExp(
				`/files/${mockItems[0].id}/content/$`,
			)

			const axiosMock = getAxiosMockAdapter()

			axiosMock.onGet(expectedUrlPattern).reply(200, mockItems[0])

			const user = userEvent.setup()

			const { getByLabelText, debug } = render(
				<FileList data={[mockItems[0]]} />,
			)
			const downloadButton = getByLabelText("download item")

			await user.click(downloadButton)

			const getRequests = axiosMock.history.get

			expect(getRequests.length).toEqual(1)

			const getRequest = getRequests[0]

			expect(getRequest.url).toMatch(expectedUrlPattern)
		})
	})
})
