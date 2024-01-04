import { expect, it, vi, describe } from "vitest"
import { screen, render, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { QueryClientProvider, QueryClient } from "@tanstack/react-query"
import AxiosMockAdapter from "axios-mock-adapter"

import axios from "@/axios"
import RegisterView from "."

function renderComponent() {
	return {
		...render(
			<QueryClientProvider client={new QueryClient()}>
				<RegisterView />
			</QueryClientProvider>,
		),
		user: userEvent.setup(),
	}
}

describe("RegisterView", () => {
	it("renders form fields", () => {
		renderComponent()

		expect(screen.queryByLabelText("Email")).toBeInTheDocument()
		expect(
			screen.queryByLabelText("New account email address"),
		).toBeInTheDocument()

		expect(screen.queryByLabelText("Password")).toBeInTheDocument()
		expect(
			screen.queryByLabelText("New account password input"),
		).toBeInTheDocument()
	})

	it("renders a submission button", () => {
		renderComponent()

		expect(
			screen.queryByLabelText("submit account registration"),
		).toBeInTheDocument()
		expect(screen.queryByText("Create account")).toBeInTheDocument()
	})

	it("sends a request to the account creation API on submission", async () => {
		const axiosMockAdapter = new AxiosMockAdapter(axios)

		axiosMockAdapter
			.onPost("/auth/user/")
			.reply(201, { username: "test", id: 1 })

		const { user } = renderComponent()

		const testInput = {
			username: "test@domain.com",
			password: "password",
		}

		const emailInput = screen.getByLabelText("New account email address")
		await user.type(emailInput, testInput.username)

		const passwordInput = screen.getByLabelText("New account password input")
		await user.type(passwordInput, testInput.password)

		const submitButton = screen.getByText("Create account")

		await user.click(submitButton)

		expect(axiosMockAdapter.history.post.length).toEqual(1)

		const requestBody = JSON.parse(axiosMockAdapter.history.post[0].data)

		expect(requestBody).toEqual(testInput)
	})

	it.each`
		scenario               | emailAddress         | password
		${"no email value"}    | ${undefined}         | ${"password"}
		${"no password value"} | ${"email@email.com"} | ${undefined}
		${"empty form"}        | ${undefined}         | ${undefined}
	`(
		"the submission button is disabled if the form isn't validated ($scenario)",
		async ({ emailAddress, password }) => {
			const { user } = renderComponent()

			if (emailAddress !== undefined) {
				const emailInput = screen.getByLabelText("New account email address")
				await user.type(emailInput, emailAddress)
				await waitFor(() =>
					expect(emailInput.getAttribute("value")).toEqual(emailAddress),
				)
			}
			if (password !== undefined) {
				const passwordInput = screen.getByLabelText(
					"New account password input",
				)

				await user.type(passwordInput, password)
				await waitFor(() =>
					expect(passwordInput.getAttribute("value")).toEqual(password),
				)
			}

			const submitButton = screen.getByText("Create account")

			await waitFor(() =>
				expect(submitButton.getAttribute("disabled")).not.toBeUndefined(),
			)
		},
	)
})
