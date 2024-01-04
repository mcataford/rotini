import { useCallback } from "react"

import MuiArticleIcon from "@mui/icons-material/Article"
import MuiDeleteIcon from "@mui/icons-material/Delete"
import MuiDownloadIcon from "@mui/icons-material/Download"
import MuiList from "@mui/material/List"
import MuiListItem from "@mui/material/ListItem"
import MuiListItemText from "@mui/material/ListItemText"
import MuiListItemButton from "@mui/material/ListItemButton"
import MuiListItemIcon from "@mui/material/ListItemIcon"
import MuiIconButton from "@mui/material/IconButton"
import MuiTypography from "@mui/material/Typography"

import { byteSizeToUnits } from "@/utils"
import { useLocationContext } from "@/contexts/LocationContext"
import { useAsyncTaskContext } from "@/contexts/AsyncTaskContext"
import { useFileMutations, useFileFetches } from "@/hooks/files"
import { type FileData } from "@/types/files"
interface FileListProps {
	data: Array<FileData>
}

interface FileListItemProps {
	title: string
	size: number
	filename: string
	onClickHandler: () => void
	onDeleteHandler: () => void
	onDownloadHandler: () => void
}

function FileListItem({
	title,
	size,
	filename,
	onClickHandler,
	onDeleteHandler,
	onDownloadHandler,
}: FileListItemProps) {
	const getSecondaryActions = useCallback(
		() => (
			<>
				<MuiIconButton
					aria-label="download item"
					onClick={() => onDownloadHandler()}
				>
					<MuiDownloadIcon />
				</MuiIconButton>
				<MuiIconButton
					aria-label="delete item"
					onClick={() => onDeleteHandler()}
				>
					<MuiDeleteIcon />
				</MuiIconButton>
			</>
		),
		[onDeleteHandler, onDownloadHandler],
	)

	return (
		<MuiListItem disablePadding secondaryAction={getSecondaryActions()}>
			<MuiListItemButton onClick={onClickHandler}>
				<MuiListItemIcon>
					<MuiArticleIcon />
				</MuiListItemIcon>
				<MuiListItemText
					primaryTypographyProps={{ "aria-label": "item title" }}
					primary={title}
					secondary={byteSizeToUnits(size)}
					secondaryTypographyProps={{ "aria-label": "item size" }}
				/>
			</MuiListItemButton>
		</MuiListItem>
	)
}

/*
 * FileList represents an interactive list of files displayed to the user.
 */
function FileList({ data }: FileListProps) {
	const { tasks } = useAsyncTaskContext()
	const { navigate } = useLocationContext()
	const { deleteFile } = useFileMutations()
	const { downloadFile } = useFileFetches()

	const onClickHandler = (uid: string) => {
		navigate(`/item/${uid}/`)
	}

	const dataWithPlaceholders = [...tasks, ...data]

	const getListItems = useCallback(() => {
		return dataWithPlaceholders.map((itemData) => (
			<FileListItem
				title={itemData.title ?? itemData.filename}
				size={itemData.size}
				filename={itemData.filename}
				onClickHandler={() =>
					onClickHandler("id" in itemData ? itemData.id : "")
				}
				onDownloadHandler={async () => {
					"id" in itemData ? downloadFile(itemData.id, itemData.filename) : null
				}}
				onDeleteHandler={() =>
					"id" in itemData ? deleteFile(itemData.id) : null
				}
				key={`file list item ${itemData.filename}`}
			/>
		))
	}, [dataWithPlaceholders, onClickHandler, downloadFile, deleteFile])

	return (
		<MuiList sx={{ width: "100%", display: "flex", flexDirection: "column" }}>
			{getListItems()}
		</MuiList>
	)
}

export default FileList
