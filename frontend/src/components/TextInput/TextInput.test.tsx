import { describe, it, expect, vi } from "vitest"
import React from "react"
import { screen, render, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"

import TextInput, { type TextInputProps } from "."

const defaultProps: TextInputProps = {
	ariaLabel: "input element",
	errorText: "",
	inputType: "text",
	label: "",
	onChange: () => {},
	validate: () => true,
	value: undefined,
}

/*
 * Since TextInput is controlled, this allows rendering it
 * with a stateful wrapper to simulate how the component would
 * behave in the wild.
 */
function renderComponent(props?: Partial<TextInputProps>) {
	const propsWithDefaults = {
		...defaultProps,
		...(props ?? {}),
	}

	const TextInputWithWrapper = () => {
		const [value, setValue] = React.useState<string>()

		const onChange = (newValue: string) => {
			propsWithDefaults.onChange(newValue)
			setValue(newValue)
		}

		return (
			<TextInput {...propsWithDefaults} onChange={onChange} value={value} />
		)
	}

	return {
		...render(<TextInputWithWrapper />),
		user: userEvent.setup(),
	}
}

describe("TextInput", () => {
	it("runs the provided onChange on input", async () => {
		const mockOnChange = vi.fn()
		const mockInput = "testinput"

		const { user } = renderComponent({ onChange: mockOnChange })

		const inputElement = screen.getByLabelText("input element")

		await user.type(inputElement, mockInput)

		await waitFor(() => expect(mockOnChange).toHaveBeenCalledWith(mockInput))
	})

	it("attaches the given ariaLabel to the input element", () => {
		const { user } = renderComponent({
			ariaLabel: "testlabel",
		})

		expect(screen.queryByLabelText("testlabel")).toBeInTheDocument()
	})

	it("passes inputType as the type of the input element", () => {
		const { user } = renderComponent({
			inputType: "password",
		})

		expect(screen.getByLabelText("input element").getAttribute("type")).toEqual(
			"password",
		)
	})
	it("displays an error message if the field validation fails", async () => {
		const mockInput = "thisisamockinput"
		const mockErrorText = "thisinputiserroneous"

		const mockValidation = (value: string) => false

		const { user } = renderComponent({
			validate: mockValidation,
			errorText: mockErrorText,
		})

		const inputElement = screen.getByLabelText("input element")

		user.type(inputElement, mockInput)

		await waitFor(() =>
			expect(inputElement.getAttribute("value")).toEqual(mockInput),
		)

		expect(screen.getByText(mockErrorText)).toBeInTheDocument()
	})

	it("removes the error text when validation errors are corrected", async () => {
		const mockErrorText = "thisinputiserroneous"

		// Valid: more than two characters.
		const mockValidation = (value: string) => value.length > 2

		const { user } = renderComponent({
			validate: mockValidation,
			errorText: mockErrorText,
		})

		const inputElement = screen.getByLabelText("input element")

		user.type(inputElement, "no")

		await waitFor(() =>
			expect(inputElement.getAttribute("value")).toEqual("no"),
		)

		expect(screen.getByText(mockErrorText)).toBeInTheDocument()

		// Value now has three character and is valid again.
		user.type(inputElement, "n")

		await waitFor(() =>
			expect(inputElement.getAttribute("value")).toEqual("non"),
		)

		expect(screen.queryByText(mockErrorText)).not.toBeInTheDocument()
	})

	it("does not display the error state when initially empty", async () => {
		const mockErrorText = "thisinputiserroneous"

		// Always invalid.
		const mockValidation = (value: string) => false

		const { user } = renderComponent({
			validate: mockValidation,
			errorText: mockErrorText,
		})

		const inputElement = screen.getByLabelText("input element")

		expect(screen.queryByText(mockErrorText)).not.toBeInTheDocument()
	})

	it("displays the error state when returning to empty state", async () => {
		const mockErrorText = "thisinputiserroneous"

		const mockValidation = (value: string) => value.length >= 1

		const { user } = renderComponent({
			validate: mockValidation,
			errorText: mockErrorText,
		})

		const inputElement = screen.getByLabelText("input element")

		user.type(inputElement, "t")

		await waitFor(() => expect(inputElement.getAttribute("value")).toEqual("t"))

		user.type(inputElement, "{backspace}")
		await waitFor(() => expect(inputElement.getAttribute("value")).toEqual(""))
		expect(screen.queryByText(mockErrorText)).toBeInTheDocument()
	})
})
