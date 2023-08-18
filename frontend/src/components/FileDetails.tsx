import MuiCard from "@mui/material/Card"
import MuiTypography from "@mui/material/Typography"
import MuiArticleIcon from "@mui/icons-material/Article"
import MuiBox from "@mui/material/Box"
import { byteSizeToUnits } from "../utils"
import MuiDeleteIcon from "@mui/icons-material/Delete"
import MuiDownloadIcon from "@mui/icons-material/Download"
import MuiIconButton from "@mui/material/IconButton"

import { useLocationContext } from "../contexts/LocationContext"
import {
	useFileDetails,
	useFileMutations,
	useFileFetches,
} from "../queries/files"

interface FileDetailsProps {
	itemId: string
}

function FileDetails({ itemId }: FileDetailsProps) {
	const { isLoading, data } = useFileDetails(itemId)
	const { deleteFile } = useFileMutations()
	const { navigate } = useLocationContext()
	const { downloadFile } = useFileFetches()

	if (isLoading || !data) return null

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
						onClick={async () => {
							await downloadFile(itemId, currentFileDetails.filename)
						}}
					>
						<MuiDownloadIcon />
					</MuiIconButton>
					<MuiIconButton
						aria-label="delete item"
						onClick={async () => {
							await deleteFile(itemId)
							navigate("/")
						}}
					>
						<MuiDeleteIcon />
					</MuiIconButton>
				</>
			</MuiBox>
		</MuiCard>
	)
}

export default FileDetails
