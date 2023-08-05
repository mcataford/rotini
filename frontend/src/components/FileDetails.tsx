import MuiCard from "@mui/material/Card"
import MuiTypography from "@mui/material/Typography"
import MuiArticleIcon from "@mui/icons-material/Article"
import MuiBox from "@mui/material/Box"
import { byteSizeToUnits } from "../utils"
import MuiDeleteIcon from "@mui/icons-material/Delete"
import MuiDownloadIcon from "@mui/icons-material/Download"
import MuiIconButton from "@mui/material/IconButton"

interface FileDetailsProps {
	itemId: string
}

// TODO: API data.
const mockData = {
	title: "My File",
	size: 123123123,
}

function FileDetails({ itemId }: FileDetailsProps) {
	const handleDownloadClick = () => {
		console.log("download click")
	}

	const handleDeleteClick = () => {
		console.log("delete click")
	}

	return (
		<MuiCard sx={{ height: "100%", display: "flex", flexDirection: "column" }}>
			<MuiBox
				component="div"
				sx={{ display: "flex", alignItems: "center", flexDirection: "column" }}
			>
				<MuiArticleIcon sx={{ fontSize: 120 }} />
				<MuiTypography variant="h1" sx={{ fontSize: 30 }}>
					{mockData.title}
				</MuiTypography>
				<MuiTypography>{byteSizeToUnits(mockData.size)}</MuiTypography>
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
