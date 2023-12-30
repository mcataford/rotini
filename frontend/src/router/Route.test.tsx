import React from "react"
import { describe, expect, it } from "vitest"
import { render, screen } from "@testing-library/react"

import Route from "./Route"

describe("Route", () => {
	it("renders its child", () => {
		render(
			<Route path="/test">
				<p data-testid="child">{"Test text"}</p>
			</Route>,
		)

		expect(screen.getByText(/test text/i)).toBeDefined()
		expect(screen.getByTestId("child")).toBeDefined()
	})
})
