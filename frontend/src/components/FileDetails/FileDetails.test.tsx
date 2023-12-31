import { vi, expect, describe, it } from "vitest"
import { act } from "@testing-library/react"
import { within } from "@testing-library/dom"
import userEvent from "@testing-library/user-event"
import { type UseQueryResult } from "@tanstack/react-query"

import {
	renderWithContexts as render,
	getAxiosMockAdapter,
} from "../../tests/helpers"
import FileDetails from "."
import { type FileData } from "../../types/files"
import * as fileQueries from "../../hooks/files"
import * as locationContextUtils from "../../contexts/LocationContext"

describe("FileDetails", () => {
	const mockItem = {
		title: "Item 1",
		filename: "item1.txt",
		size: 1,
		id: "b61bf93d-a9db-473e-822e-a65003b1b7e3",
	}
	it("Clicking the download button trigger a file download", async () => {
		// FIXME: Validating file downloads is ... tricky. The current interaction with dynamically created DOM
		// elements is not visible by vi.

		const expectedUrlPattern = new RegExp(`/files/${mockItem.id}/content/$`)

		const axiosMock = getAxiosMockAdapter()

		axiosMock.onGet(expectedUrlPattern).reply(200, mockItem)

		vi.spyOn(fileQueries, "useFileDetails").mockReturnValue({
			data: mockItem,
			isLoading: false,
		} as UseQueryResult<FileData, Error>)
		const user = userEvent.setup()

		const { getByLabelText, debug, rerender } = render(
			<FileDetails itemId={mockItem.id} />,
		)

		const downloadButton = getByLabelText("download item")

		await user.click(downloadButton)

		const downloadRequests = axiosMock.history.get

		expect(downloadRequests.length).toEqual(1)

		const downloadRequest = downloadRequests[0]

		expect(downloadRequest.url).toMatch(expectedUrlPattern)
	})

	it("Clicking the delete button fires request to delete file", async () => {
		const expectedUrlPattern = new RegExp(`/files/${mockItem.id}/$`)

		const axiosMock = getAxiosMockAdapter()

		axiosMock.onDelete(expectedUrlPattern).reply(200, mockItem)

		vi.spyOn(fileQueries, "useFileDetails").mockReturnValue({
			data: mockItem,
			isLoading: false,
		} as UseQueryResult<FileData, Error>)
		const user = userEvent.setup()

		const { getByLabelText, debug, rerender } = render(
			<FileDetails itemId={mockItem.id} />,
		)

		const deleteButton = getByLabelText("delete item")

		await user.click(deleteButton)

		const deleteRequests = axiosMock.history.delete

		expect(deleteRequests.length).toEqual(1)

		const deleteRequest = deleteRequests[0]

		expect(deleteRequest.url).toMatch(expectedUrlPattern)
	})

	it("Clicking the delete button redirects to the file list after success", async () => {
		const expectedUrlPattern = new RegExp(`/files/${mockItem.id}/$`)

		const axiosMock = getAxiosMockAdapter()

		axiosMock.onDelete(expectedUrlPattern).reply(200, mockItem)

		vi.spyOn(fileQueries, "useFileDetails").mockReturnValue({
			data: mockItem,
			isLoading: false,
		} as UseQueryResult<FileData, Error>)

		const navigateMock = vi.fn().mockImplementation((a: string) => {})
		vi.spyOn(locationContextUtils, "useLocationContext").mockReturnValue({
			location: {
				path: "",
				label: null,
				params: {},
				pattern: "",
			},
			navigate: navigateMock,
		})
		const user = userEvent.setup()

		const { getByLabelText, debug, rerender } = render(
			<FileDetails itemId={mockItem.id} />,
		)

		const deleteButton = getByLabelText("delete item")

		await user.click(deleteButton)

		expect(navigateMock.mock.calls.length).toEqual(1)

		const navigateCall = navigateMock.mock.calls[0]

		expect(navigateCall[0]).toEqual("/")
	})
})
