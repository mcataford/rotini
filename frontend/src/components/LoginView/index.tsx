import React from "react"

import Typography from "@mui/material/Typography"
import Box from "@mui/material/Box"
import FormGroup from "@mui/material/FormGroup"
import FormControl from "@mui/material/FormControl"
import TextField from "@mui/material/TextField"
import InputLabel from "@mui/material/InputLabel"
import Button from "@mui/material/Button"
import Link from "@mui/material/Link"
import Alert from "@mui/material/Alert"

import { useLogin } from "@/queries/auth"
import axiosWithDefaults from "@/axios"
import TextInput from "@/components/TextInput"

function LoginView() {
	const [emailAddress, setEmailAddress] = React.useState<string>("")
	const [password, setPassword] = React.useState<string>("")
	const { login, isError, isPending } = useLogin()

	const emailField = React.useMemo(
		() => (
			<TextInput
				label="Email"
				ariaLabel="email address login input"
				onChange={setEmailAddress}
				value={emailAddress}
				inputType="email"
			/>
		),
		[emailAddress],
	)

	const passwordField = React.useMemo(
		() => (
			<TextInput
				label="Password"
				ariaLabel="password login input"
				onChange={setPassword}
				value={password}
				inputType="password"
			/>
		),
		[password],
	)

	const isFormValid = React.useMemo(() => {
		return Boolean(emailAddress) && Boolean(password)
	}, [emailAddress, password])

	const onLoginClick = React.useCallback(() => {
		if (!isFormValid) return

		login({ email: emailAddress, password })
	}, [login, emailAddress, password, isFormValid])

	return (
		<Box sx={{ display: "flex", justifyContent: "center", width: "100%" }}>
			<FormGroup
				sx={{
					display: "flex",
					gap: "10px",
					textAlign: "center",
					width: "600px",
				}}
			>
				<Typography variant="h1" sx={{ fontSize: "2rem" }}>
					Log in
				</Typography>
				{isError ? (
					<Alert severity="error">
						{
							"This combination of email and password does not match our records. Verify if the email or password are incorrect."
						}
					</Alert>
				) : null}
				{emailField}
				{passwordField}
				<Button
					variant="contained"
					onClick={onLoginClick}
					aria-label="submit login"
					disabled={!isFormValid || isPending}
				>
					Log in
				</Button>
				<Typography>
					Don't have an account yet? <Link href="/register">Create one!</Link>
				</Typography>
			</FormGroup>
		</Box>
	)
}

export default LoginView
