import React from "react"
import { describe, it, expect, vi } from "vitest"
import { renderHook, waitFor } from "@testing-library/react"
import { QueryClientProvider, QueryClient } from "@tanstack/react-query"
import AxiosMockAdapter from "axios-mock-adapter"

import axiosWithDefaults from "../axios"
import { useCurrentUser } from "./user"

function WithProviders({ children }: { children: React.ReactNode }) {
	return (
		<QueryClientProvider client={new QueryClient()}>
			{children}
		</QueryClientProvider>
	)
}

describe("useCurrentUser", () => {
	it("sends a request to the currentUser api", async () => {
		const axios = new AxiosMockAdapter(axiosWithDefaults)

		axios.onGet("/auth/user/").reply(204)

		const { result } = renderHook(() => useCurrentUser(), {
			wrapper: WithProviders,
		})

		await waitFor(() => expect(axios.history.get.length).toEqual(1))

		const getRequest = axios.history.get[0]

		expect(getRequest.url).toEqual("/auth/user/")
	})

	it.each`
		isAuthenticated | returnCode
		${false}        | ${403}
		${true}         | ${200}
	`(
		"sets isAuthenticated ($isAuthenticated) when the api returns $returnCode",
		async ({ isAuthenticated, returnCode }) => {
			const axios = new AxiosMockAdapter(axiosWithDefaults)

			axios.onGet("/auth/user/").reply(returnCode, { status: returnCode })

			const { result } = renderHook(() => useCurrentUser(), {
				wrapper: WithProviders,
			})

			await waitFor(() => expect(result.current.isLoading).toBe(false))
			expect(result.current.isAuthenticated).toBe(isAuthenticated)
		},
	)
})
