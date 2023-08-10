import { useRef, useCallback, ChangeEvent } from "react"
import { useQueryClient } from "@tanstack/react-query"

import AppBar from "@mui/material/AppBar"
import Toolbar from "@mui/material/Toolbar"
import Button from "@mui/material/Button"
import Typography from "@mui/material/Typography"
import UploadIcon from "@mui/icons-material/Upload"

import { uploadFile } from "../queries/files"

function UploadFileButton() {
	const fileRef = useRef(null)
	const queryClient = useQueryClient()

	const onClick = () => {
		if (fileRef.current) (fileRef.current as HTMLInputElement).click()
	}

	const onSelectedFileChange = useCallback(
		async (e: ChangeEvent<HTMLInputElement>) => {
			const inputFiles = e.target.files
			if (!inputFiles || inputFiles.length === 0) return

			const selectedFile = inputFiles[0]
			const response = await uploadFile(selectedFile)
			queryClient.invalidateQueries({ queryKey: ["file-list"] })
		},
		[uploadFile, queryClient],
	)
	return (
		<>
			<Button color="inherit" startIcon={<UploadIcon />} onClick={onClick}>
				Upload file
			</Button>
			<input
				style={{ display: "none" }}
				type="file"
				ref={fileRef}
				onChange={onSelectedFileChange}
			/>
		</>
	)
}

function NavigationBar() {
	return (
		<AppBar position="sticky" sx={{ display: "flex" }}>
			<Toolbar>
				<Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
					Rotini
				</Typography>
				<UploadFileButton />
			</Toolbar>
		</AppBar>
	)
}

export default NavigationBar
