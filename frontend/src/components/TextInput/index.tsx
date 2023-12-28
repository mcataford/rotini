/*
 * The TextInput component is a multipurpose text-input component
 * with validation.
 *
 * TextInput is a controlled component and expects to be provided with
 * a current value and state update function (onChange).
 */

import React from "react"
import FormControl from "@mui/material/FormControl"
import TextField from "@mui/material/TextField"
import InputLabel from "@mui/material/InputLabel"
import FormHelperText from "@mui/material/FormHelperText"

interface Props {
	// Aria label applied to the input element.
	ariaLabel: string
	// Text to display if validation fails. Only used if a validation function is provided.
	errorText?: string
	// HTML5 input type of the input field.
	inputType: string
	// Text label visible to the user with the input.
	label: string
	// Function to run on each field change.
	onChange: (value: string) => void
	// Optional validation function that decides if the current input state triggers an error.
	validate?: (value: string) => boolean
	// Input field value
	value: string | undefined
}

function TextInput({
	ariaLabel,
	errorText,
	inputType = "text",
	label,
	onChange,
	validate = () => true,
	value,
}: Props) {
	const isError = value !== undefined && !validate(value)

	const helpText = isError ? <FormHelperText>{errorText}</FormHelperText> : null

	return (
		<FormControl>
			<TextField
				label={label}
				value={value ?? ""}
				onChange={(e) => {
					const updatedValue = e.target.value
					onChange(updatedValue)
				}}
				error={isError}
				inputProps={{
					"aria-label": ariaLabel,
				}}
				type={inputType}
			/>
			{helpText}
		</FormControl>
	)
}

export { Props as TextInputProps }

export default TextInput
