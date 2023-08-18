import { useQuery, useQueryClient } from "@tanstack/react-query"

import axios from "axios"

export const axiosWithDefaults = axios.create({
	baseURL: "http://localhost:8000",
})

interface FileData {
	/* Displayed title of the item. */
	title: string
	/* Filename of the item as it appears on disk. */
	filename: string
	/* Size of the file in bytes. */
	size: number
	/* Unique identifier */
	id: string
}

function useOwnFileList() {
	return useQuery(["file-list"], async () => {
		const response = await axiosWithDefaults.get<Array<FileData>>("/files/")

		return response.data
	})
}

function useFileDetails(fileId: string) {
	return useQuery(["file-details", fileId], async () => {
		const response = await axiosWithDefaults.get<FileData>(`/files/${fileId}/`)

		return response.data
	})
}

/*
 * `useFileMutations` provides helpers that trigger API interactions
 * with the backend to modify files stored in the system.
 */
function useFileMutations(): {
	deleteFile: (fileId: string) => Promise<FileData>
} {
	const queryClient = useQueryClient()

	const deleteFile = async (fileId: string): Promise<FileData> => {
		const response = await axiosWithDefaults.delete<FileData>(
			`/files/${fileId}/`,
		)

		queryClient.invalidateQueries({ queryKey: ["file-list"] })
		return response.data
	}

	return { deleteFile }
}

/*
 * Downloads a file given its ID.
 *
 * This function returns nothing and is intended to trigger a download
 * action in the browser directly.
 */
async function downloadFile(fileId: string, fileName: string) {
	const r = await axiosWithDefaults.get(`/files/${fileId}/content/`)
	const a = document.createElement("a")
	const b = r.data
	a.href = URL.createObjectURL(
		new Blob([b], { type: "application/octet-stream" }),
	)
	a.download = fileName
	a.click()
}

/*
 * Uploads a file.
 */
async function uploadFile(file: File) {
	const formData = new FormData()
	formData.append("file", file)

	const response = await axiosWithDefaults.postForm<FileData>(
		"/files/",
		formData,
	)

	return response.data
}

export {
	useOwnFileList,
	useFileDetails,
	useFileMutations,
	uploadFile,
	downloadFile,
}

// Types
export { FileData }
