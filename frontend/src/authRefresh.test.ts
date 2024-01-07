import { describe, it, vi, expect, beforeEach, afterEach } from "vitest"
import { waitFor } from "@testing-library/react"
import { getAxiosMockAdapter } from "@/tests/helpers"
import setupAuthTokenAutoRefresh, {
	REFRESH_INTERVAL,
	REFRESH_TOKEN_KEY,
} from "./authRefresh"

async function flushPromises() {
	return new Promise((r) => setTimeout(r))
}

describe("setupAuthTokenAutoRefresh", () => {
	let clearInterval: (() => void) | undefined = undefined
	const mockLocalStorage = new Map<string, string>()
	beforeEach(() => {
		vi.spyOn(Storage.prototype, "setItem").mockImplementation(
			(key: string, value: string) => {
				mockLocalStorage.set(key, value)
			},
		)
		vi.spyOn(Storage.prototype, "getItem").mockImplementation(
			(key: string): string => mockLocalStorage.get(key) || "",
		)

		vi.useFakeTimers()
	})

	afterEach(() => {
		vi.restoreAllMocks()
		globalThis.localStorage.clear()

		if (clearInterval) clearInterval()
	})

	it("does not do anything if loop already initialized", () => {
		const clear = setupAuthTokenAutoRefresh()

		expect(clear).not.toBeUndefined()
		const secondClear = setupAuthTokenAutoRefresh()

		expect(secondClear).toBeUndefined()

		clear?.()
	})

	it("checks the status of the auth token at each interval", async () => {
		const axiosMock = getAxiosMockAdapter()

		globalThis.localStorage.setItem(REFRESH_TOKEN_KEY, "refresh_token")

		axiosMock.onGet("/auth/session/").reply(200, { should_refresh: false })
		clearInterval = setupAuthTokenAutoRefresh()

		vi.advanceTimersByTime(REFRESH_INTERVAL)

		expect(axiosMock.history.get.length).toEqual(1)

		const apiCall = axiosMock.history.get[0]

		expect(apiCall.url).toEqual("/auth/session/")
	})

	// FIXME: LocalStorage does not update, but the request is run as expected.
	it.skip("attempts to refresh the token if the status checks says the token must be refreshed", async () => {
		const axiosMock = getAxiosMockAdapter()

		globalThis.localStorage.setItem(REFRESH_TOKEN_KEY, "refresh_token")

		axiosMock
			.onGet("/auth/session/")
			.reply(200, { should_refresh: true })
			.onPut("/auth/session/")
			.reply(201, { refresh_token: "new_refresh_token" })

		clearInterval = setupAuthTokenAutoRefresh()

		vi.advanceTimersByTime(REFRESH_INTERVAL)

		const localStorageToken = globalThis.localStorage.getItem(REFRESH_TOKEN_KEY)

		expect(localStorageToken).toEqual("new_refresh_token")
	})
})
