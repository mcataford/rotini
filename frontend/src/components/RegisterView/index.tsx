import React from "react"
import { useMutation } from "@tanstack/react-query"

import Typography from "@mui/material/Typography"
import Box from "@mui/material/Box"
import FormGroup from "@mui/material/FormGroup"
import FormControl from "@mui/material/FormControl"
import TextField from "@mui/material/TextField"
import InputLabel from "@mui/material/InputLabel"
import FormHelperText from "@mui/material/FormHelperText"
import Button from "@mui/material/Button"

import axiosWithDefaults from "../../axios"
import TextInput from "../TextInput"
import { validateEmail, validatePassword } from "./validation"

function RegisterView() {
	const [emailAddress, setEmailAddress] = React.useState<string | undefined>()
	const [password, setPassword] = React.useState<string | undefined>()

	const { mutate } = useMutation({
		mutationFn: async ({
			email,
			password,
		}: { email: string; password: string }) => {
			const response = await axiosWithDefaults.post("/auth/user/", {
				username: email,
				password,
			})

			return response
		},
	})

	const emailField = React.useMemo(
		() => (
			<TextInput
				errorText={"Enter valid email of the format 'abc@xyz.org'"}
				label="Email"
				ariaLabel="New account email address"
				inputType="email"
				onChange={setEmailAddress}
				validate={validateEmail}
				value={emailAddress}
			/>
		),
		[emailAddress, setEmailAddress, validateEmail],
	)

	const passwordField = React.useMemo(
		() => (
			<TextInput
				errorText={"A valid password should have between 8-64 characters."}
				label="Password"
				ariaLabel="New account password input"
				inputType="password"
				onChange={setPassword}
				validate={validatePassword}
				value={password}
			/>
		),
		[setPassword, password, validatePassword],
	)

	const isFormValid = React.useMemo(() => {
		return validateEmail(emailAddress) && validatePassword(password)
	}, [emailAddress, password, validatePassword, validateEmail])

	const onCreateClick = React.useCallback(() => {
		if (!isFormValid) return

		mutate({ email: String(emailAddress), password: String(password) })
	}, [mutate, emailAddress, password, isFormValid])

	return (
		<Box sx={{ display: "flex", justifyContent: "center", width: "100%" }}>
			<FormGroup sx={{ flexGrow: 0.1, display: "flex", gap: "10px" }}>
				<Typography variant="h1" sx={{ fontSize: "2rem" }}>
					Create an account
				</Typography>
				<Typography>
					{"Fill the form below to create an account and get started!"}
				</Typography>
				{emailField}
				{passwordField}
				<Button
					variant="contained"
					onClick={onCreateClick}
					aria-label="submit account registration"
					disabled={!isFormValid}
				>
					Create account
				</Button>
			</FormGroup>
		</Box>
	)
}

export default RegisterView
