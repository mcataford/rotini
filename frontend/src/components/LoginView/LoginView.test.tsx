import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { QueryClientProvider, QueryClient } from "@tanstack/react-query"
import AxiosMockAdapter from "axios-mock-adapter"

import axios from "../../axios"
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
		const mock = jest.fn()
		const { user } = renderComponent()

		expect(screen.getByText(/don\'t have an account yet?/i)).toBeInTheDocument()

		const registrationLink = screen.getByText(/create one/i)
		expect(registrationLink).toBeInTheDocument()

		expect(registrationLink.getAttribute("href")).toEqual("/register")
	})

	it("sends a request to the authentication API on submit", async () => {
		const axiosMockAdapter = new AxiosMockAdapter(axios)

		axiosMockAdapter.onPost("/auth/session/").reply(201, { token: "testtoken" })

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
})
