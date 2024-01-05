import { expect, describe, it, vi } from "vitest"

import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { QueryClientProvider, QueryClient } from "@tanstack/react-query"
import AxiosMockAdapter from "axios-mock-adapter"

import axios from "@/axios"
import * as locationHook from "@/contexts/LocationContext"
import LoginView from "."

function renderComponent() {
	return {
		...render(
			<QueryClientProvider client={new QueryClient()}>
				<LoginView />
			</QueryClientProvider>,
		),
		user: userEvent.setup(),
	}
}

describe("LoginView", () => {
	it("renders an email and password field", () => {
		renderComponent()

		expect(screen.getByLabelText("Email")).toBeInTheDocument()
		expect(
			screen.getByLabelText(/email address login input/i),
		).toBeInTheDocument()

		expect(screen.getByLabelText("Password")).toBeInTheDocument()
		expect(screen.getByLabelText(/password login input/i)).toBeInTheDocument()
	})

	it("renders a submit button", () => {
		renderComponent()

		expect(
			screen.getByText("Log in", { selector: "button" }),
		).toBeInTheDocument()
		expect(screen.getByLabelText(/submit login/i)).toBeInTheDocument()
	})

	it("renders a registration link", async () => {
		const mock = vi.fn()
		const { user } = renderComponent()

		expect(screen.getByText(/don\'t have an account yet?/i)).toBeInTheDocument()

		const registrationLink = screen.getByText(/create one/i)
		expect(registrationLink).toBeInTheDocument()

		expect(registrationLink.getAttribute("href")).toEqual("/register")
	})

	it("sends a request to the authentication API on submit", async () => {
		const axiosMockAdapter = new AxiosMockAdapter(axios)

		axiosMockAdapter.onPost("/auth/session/").reply(201)

		const { user } = renderComponent()

		const testInput = {
			username: "test@domain.com",
			password: "password",
		}

		const emailInput = screen.getByLabelText(/email address login input/i)
		await user.type(emailInput, testInput.username)

		const passwordInput = screen.getByLabelText(/password login input/i)
		await user.type(passwordInput, testInput.password)

		const submitButton = screen.getByText("Log in", { selector: "button" })

		await user.click(submitButton)

		expect(axiosMockAdapter.history.post.length).toEqual(1)

		const requestBody = JSON.parse(axiosMockAdapter.history.post[0].data)

		expect(requestBody).toEqual(testInput)
	})

	it("displays error messaging if the login attempt is not successful", async () => {
		const axiosMockAdapter = new AxiosMockAdapter(axios)

		axiosMockAdapter.onPost("/auth/session/").reply(400)

		const { user } = renderComponent()

		const testInput = {
			username: "test@domain.com",
			password: "password",
		}

		const emailInput = screen.getByLabelText(/email address login input/i)
		await user.type(emailInput, testInput.username)

		const passwordInput = screen.getByLabelText(/password login input/i)
		await user.type(passwordInput, testInput.password)

		const submitButton = screen.getByText("Log in", { selector: "button" })

		await user.click(submitButton)

		await waitFor(() => expect(screen.getByRole("alert")).toBeInTheDocument())

		expect(
			screen.getByText(
				/this combination of email and password does not match our records\. verify if the email or password are incorrect\./i,
			),
		).toBeInTheDocument()
	})

	it("redirects the user on success", async () => {
		const mockNavigate = vi.fn()
		const mockLocationHook = vi
			.spyOn(locationHook, "useLocationContext")
			.mockImplementation(() => ({
				location: {
					path: "",
					label: "",
					params: {},
					pattern: "",
				},
				navigate: mockNavigate,
			}))
		const axiosMockAdapter = new AxiosMockAdapter(axios)

		axiosMockAdapter
			.onPost("/auth/session/")
			.reply(201, { refresh_token: "notatoken" })

		const { user } = renderComponent()

		const testInput = {
			username: "test@domain.com",
			password: "password",
		}

		const emailInput = screen.getByLabelText(/email address login input/i)
		await user.type(emailInput, testInput.username)

		const passwordInput = screen.getByLabelText(/password login input/i)
		await user.type(passwordInput, testInput.password)

		const submitButton = screen.getByText("Log in", { selector: "button" })

		await user.click(submitButton)

		expect(mockNavigate).toHaveBeenCalledWith("/")
	})
})
