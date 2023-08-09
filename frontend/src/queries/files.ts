import { useQuery } from "react-query"

function useOwnFileList() {
	return useQuery("file-list", async () => {
		const response = await fetch("http://localhost:8000/files/")

		return response.json()
	})
}

function useFileDetails(fileId: string) {
	return useQuery(`file-details-${fileId}`, async () => {
		const response = await fetch(`http://localhost:8000/files/${fileId}/`)

		return response.json()
	})
}

export { useOwnFileList, useFileDetails }
