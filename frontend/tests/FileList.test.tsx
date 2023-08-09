import { within } from "@testing-library/dom"

import { renderWithContexts as render } from "./helpers"
import FileList from "../src/components/FileList"

describe("FileList", () => {
	const mockItems = [
		{ title: "Item 1", filename: "item1.txt", size: 1, id: "123" },
		{ title: "Item 2", filename: "item2.txt", size: 1, id: "456" },
	]

	const mockAsyncTasks = [
		{ title: "Async Item 0", filename: "async.txt", size: 2, type: "upload" },
	]

	test("Renders list items provided", () => {
		const { getAllByText } = render(<FileList data={mockItems} />)
		const renderedItems = getAllByText(/Item/)

		expect(renderedItems.length).toEqual(mockItems.length)
	})

	test("Prepends items in flight as tracked by async task context", () => {
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
		test("Renders the item title", () => {
			const { getByLabelText, debug } = render(
				<FileList data={[mockItems[0]]} />,
			)
			const title = getByLabelText("item title")
			within(title).getByText(mockItems[0].title)
		})

		test("Renders the item size", () => {
			const { getByLabelText, debug } = render(
				<FileList data={[mockItems[0]]} />,
			)
			const title = getByLabelText("item size")
			within(title).getByText(`${mockItems[0].size} B`)
		})

		test.each(["download item", "delete item"])(
			"Renders secondary action buttons (%s)",
			(action) => {
				const { getByLabelText, debug } = render(
					<FileList data={[mockItems[0]]} />,
				)
				getByLabelText(action)
			},
		)
	})
})
