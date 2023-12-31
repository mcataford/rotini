import { useQuery, useQueryClient } from "@tanstack/react-query"

import axios from "../axios"
import { type FileData } from "../types/files"

function useOwnFileList() {
	return useQuery({
		queryKey: ["file-list"],
		queryFn: async () => {
			const response = await axios.get<Array<FileData>>("/files/")

			return response.data
		},
	})
}

function useFileDetails(fileId: string) {
	return useQuery({
		queryKey: ["file-details", fileId],
		queryFn: async () => {
			const response = await axios.get<FileData>(`/files/${fileId}/`)

			return response.data
		},
	})
}

/*
 * `useFileMutations` provides helpers that trigger API interactions
 * with the backend to modify files stored in the system.
 */
function useFileMutations(): {
	deleteFile: (fileId: string) => Promise<FileData>
	uploadFile: (file: File) => Promise<FileData>
} {
	const queryClient = useQueryClient()

	const deleteFile = async (fileId: string): Promise<FileData> => {
		const response = await axios.delete<FileData>(`/files/${fileId}/`)

		queryClient.invalidateQueries({ queryKey: ["file-list"] })
		return response.data
	}

	const uploadFile = async (file: File) => {
		const formData = new FormData()
		formData.append("file", file)

		const response = await axios.postForm<FileData>("/files/", formData)

		return response.data
	}

	return { deleteFile, uploadFile }
}

/*
 * Hook providing callable async functions implementing one-off
 * fetches on the files API.
 *
 * Returns:
 *  downloadFile: Triggers a file download.
 *
 */
function useFileFetches(): {
	downloadFile: (fileId: string, fileName: string) => Promise<void>
} {
	/*
	 * Downloading the file is done by fetching the binary blob from the
	 * API and creating a "virtual" anchor element that we programmatically
	 * click. This is a hack to trigger a file download from a non-file URL.
	 */
	const downloadFile = async (fileId: string, fileName: string) => {
		const response = await axios.get(`/files/${fileId}/content/`)
		const virtualAnchor = document.createElement("a")
		virtualAnchor.href = URL.createObjectURL(
			new Blob([response.data], { type: "application/octet-stream" }),
		)
		virtualAnchor.download = fileName
		virtualAnchor.click()
	}

	return { downloadFile }
}

export { useOwnFileList, useFileDetails, useFileMutations, useFileFetches }
