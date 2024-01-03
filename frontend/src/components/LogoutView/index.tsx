import React from "react"
import Box from "@mui/material/Box"
import Typography from "@mui/material/Typography"

import { useLogout } from "../../queries/auth"

function LogoutView() {
	const { logout } = useLogout()

	React.useEffect(() => {
		logout()
	}, [logout])

	return (
		<Box sx={{ display: "flex", justifyContent: "center", width: "100%" }}>
			<Typography>{"You are now logged out!"}</Typography>
		</Box>
	)
}

export default LogoutView
