import MuiCard from "@mui/material/Card"
import MuiTypography from "@mui/material/Typography"
import MuiArticleIcon from "@mui/icons-material/Article"
import MuiBox from "@mui/material/Box"
import { byteSizeToUnits } from "../utils"
import MuiDeleteIcon from "@mui/icons-material/Delete"
import MuiDownloadIcon from "@mui/icons-material/Download"
import MuiIconButton from "@mui/material/IconButton"

import { useFileDetails } from "../queries/files"

interface FileDetailsProps {
	itemId: string
}

function FileDetails({ itemId }: FileDetailsProps) {
	const { isLoading, data } = useFileDetails(itemId)

	if (isLoading) return null

	const handleDownloadClick = () => {
		console.log("download click")
	}

	const handleDeleteClick = () => {
		console.log("delete click")
	}

	const currentFileDetails = data

	return (
		<MuiCard sx={{ height: "100%", display: "flex", flexDirection: "column" }}>
			<MuiBox
				component="div"
				sx={{ display: "flex", alignItems: "center", flexDirection: "column" }}
			>
				<MuiArticleIcon sx={{ fontSize: 120 }} />
				<MuiTypography variant="h1" sx={{ fontSize: 30 }}>
					{currentFileDetails.title ?? currentFileDetails.filename}
				</MuiTypography>
				<MuiTypography>
					{byteSizeToUnits(currentFileDetails.size)}
				</MuiTypography>
			</MuiBox>
			<MuiBox sx={{ display: "flex", justifyContent: "center" }}>
				<>
					<MuiIconButton
						aria-label="download item"
						onClick={() => handleDownloadClick()}
					>
						<MuiDownloadIcon />
					</MuiIconButton>
					<MuiIconButton
						aria-label="delete item"
						onClick={() => handleDeleteClick()}
					>
						<MuiDeleteIcon />
					</MuiIconButton>
				</>
			</MuiBox>
		</MuiCard>
	)
}

export default FileDetails
