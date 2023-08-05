import { useRef } from "react"

import AppBar from "@mui/material/AppBar"
import Toolbar from "@mui/material/Toolbar"
import Button from "@mui/material/Button"
import Typography from "@mui/material/Typography"
import UploadIcon from "@mui/icons-material/Upload"

import { useAsyncTaskContext } from "../contexts/AsyncTaskContext"

function UploadFileButton() {
	const fileRef = useRef(null)
	const { addTask, tasks } = useAsyncTaskContext()

	const uploadFile = () => {
		fileRef.current.click()
	}
	return (
		<>
			<Button color="inherit" startIcon={<UploadIcon />} onClick={uploadFile}>
				Upload file
			</Button>
			<input
				style={{ display: "none" }}
				type="file"
				ref={fileRef}
				onChange={(e) => {
					if (e.target.files.length === 0) return

					const selectedFile = e.target.files[0]
					addTask({
						type: "upload",
						filename: selectedFile.name,
						size: selectedFile.size,
						title: selectedFile.name,
					})
				}}
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
