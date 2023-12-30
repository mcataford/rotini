import { afterEach, describe, it, vi, expect } from "vitest"
import { render, screen } from "@testing-library/react"

import { LocationContext } from "../contexts/LocationContext"
import Router from "./Router"
import Route from "./Route"

function renderComponent(component: React.ReactElement) {
	render(<LocationContext routes={{}}>{component}</LocationContext>)
}

describe("Router", () => {
	afterEach(() => {
		vi.resetAllMocks()
	})

	it("throws an error if no Route exists for the given location", () => {
		vi.spyOn(globalThis, "location", "get").mockReturnValue({
			...globalThis.location,
			pathname: "/doesnotexist",
		})

		// Silence the error to avoid logspam in tests.
		vi.spyOn(console, "error").mockImplementation(() => {})

		expect(() =>
			renderComponent(
				<Router>
					<Route path="/">
						<p>{"test"}</p>
					</Route>
				</Router>,
			),
		).toThrow()
	})

	it("renders the route matching the given location", () => {
		vi.spyOn(globalThis, "location", "get").mockReturnValue({
			...globalThis.location,
			pathname: "/exists",
		})

		renderComponent(
			<Router>
				<Route path="/exists">
					<p>{"test"}</p>
				</Route>
			</Router>,
		)

		expect(screen.getByText(/test/i)).toBeInTheDocument()
	})

	it("only renders the route that matches", () => {
		vi.spyOn(globalThis, "location", "get").mockReturnValue({
			...globalThis.location,
			pathname: "/matches",
		})

		renderComponent(
			<Router>
				<Route path="/matches">
					<p>{"test"}</p>
				</Route>
				<Route path="/doesnotmatch">
					<p>{"notthere"}</p>
				</Route>
			</Router>,
		)

		expect(screen.getByText(/test/i)).toBeInTheDocument()
		expect(screen.queryByText(/notthere/i)).toBeNull()
	})
})
