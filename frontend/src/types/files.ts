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

export { FileData }
