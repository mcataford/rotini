import { useQuery, useQueryClient } from "@tanstack/react-query"

import makeRequest from "./requestUtils"

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
		const response = await makeRequest<Array<FileData>>(
			"http://localhost:8000/files/",
		)

		return response.json
	})
}

function useFileDetails(fileId: string) {
	return useQuery(["file-details", fileId], async () => {
		const response = await makeRequest<FileData>(
			`http://localhost:8000/files/${fileId}/`,
		)

		return response.json
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
		const response = await makeRequest<FileData>(
			`http://localhost:8000/files/${fileId}`,
			{ method: "DELETE" },
		)

		queryClient.invalidateQueries({ queryKey: ["file-list"] })
		return response.json
	}

	return { deleteFile }
}

/*
 * Uploads a file.
 */
async function uploadFile(file: File) {
	const formData = new FormData()
	formData.append("file", file)

	const response = await makeRequest<FileData>("http://localhost:8000/files/", {
		method: "POST",
		body: formData,
	})

	return response.json
}

export { useOwnFileList, useFileDetails, useFileMutations, uploadFile }

// Types
export { FileData }
