import React from "react"
import { describe, it, expect, vi } from "vitest"
import { renderHook, waitFor } from "@testing-library/react"
import { QueryClientProvider, QueryClient } from "@tanstack/react-query"
import AxiosMockAdapter from "axios-mock-adapter"

import * as locationHook from "@/contexts/LocationContext"
import axiosWithDefaults from "@/axios"
import { useLogout } from "./auth"

function WithProviders({ children }: { children: React.ReactNode }) {
	return (
		<QueryClientProvider client={new QueryClient()}>
			{children}
		</QueryClientProvider>
	)
}

describe("useLogout", () => {
	it("sends a request to the logout api", async () => {
		const axios = new AxiosMockAdapter(axiosWithDefaults)

		axios.onDelete("/auth/session/").reply(204)

		const { result } = renderHook(() => useLogout(), { wrapper: WithProviders })

		result.current.logout()

		await waitFor(() => expect(axios.history.delete.length).toEqual(1))

		const deleteRequest = axios.history.delete[0]

		expect(deleteRequest.url).toEqual("/auth/session/")
	})

	it("navigates to the login page on success", async () => {
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

		const axios = new AxiosMockAdapter(axiosWithDefaults)

		axios.onDelete("/auth/session/").reply(204)

		const { result } = renderHook(() => useLogout(), { wrapper: WithProviders })

		result.current.logout()

		await waitFor(() => expect(mockNavigate).toHaveBeenCalledWith("/login"))
	})
})
