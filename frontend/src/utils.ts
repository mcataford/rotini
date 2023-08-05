function byteSizeToUnits(byteSize: number): string {
	if (byteSize < 1000) return `${byteSize} B`

	if (byteSize < 1_000_000) return `${(byteSize / 1000).toFixed(2)} kB`

	if (byteSize < 1_000_000_000) return `${(byteSize / 1_000_000).toFixed(2)} mB`
	else return `${(byteSize / 1_000_000_000).toFixed(2)} gB`
}

export { byteSizeToUnits }
