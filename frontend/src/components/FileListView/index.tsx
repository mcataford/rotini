import React from "react"

import Box from "@mui/material/Box"

import FileList from "components/FileList"
import FileDetails from "components/FileDetails"
import { useOwnFileList } from "hooks/files"
import { useLocationContext } from "contexts/LocationContext"

function FileListView() {
	const { isLoading, data } = useOwnFileList()
	const { location } = useLocationContext()

	const sidebar = React.useMemo(() => {
		if (location.params.itemId)
			return (
				<Box
					aria-label="item details sidebar"
					component="div"
					sx={{ flexGrow: 1 }}
				>
					<FileDetails itemId={location.params.itemId} />
				</Box>
			)
		return null
	}, [location])

	if (isLoading || !data) return "Loading"

	return (
		<>
			<Box component="div" sx={{ flexGrow: 1 }}>
				<FileList data={data} />
			</Box>
			{sidebar}
		</>
	)
}

export default FileListView
