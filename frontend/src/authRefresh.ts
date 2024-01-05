import axiosWithDefaults from "@/axios"

const REFRESH_TOKEN_KEY = "jwt_refresh_token"
const REFRESH_INTERVAL = 30000

/*
 * Singleton tracking the token refresh loop.
 *
 * This ensures that token autorefresh is only initialized
 * once.
 */
let tokenRefreshLoop: ReturnType<typeof setInterval> | null = null

function getRefreshToken() {
	return globalThis.localStorage.getItem(REFRESH_TOKEN_KEY)
}

function setRefreshToken(token: string) {
	globalThis.localStorage.setItem(REFRESH_TOKEN_KEY, token)
}

function unsetRefreshToken() {
	globalThis.localStorage.removeItem(REFRESH_TOKEN_KEY)
}

/*
 * Periodically verifies the status of the authentication token
 * expiration and initiates token refresh based on feedback
 * from the server.
 *
 * If the token is in need of refresh, a request is made to
 * generate a new token that will be attached to the response
 * as a cookie, and the refresh token stored in localStorage
 * gets refreshed.
 */
function setupAuthTokenAutoRefresh() {
	if (tokenRefreshLoop) {
		console.warn("Authentication token refresh loop already initialized.")
		return
	}

	tokenRefreshLoop = setInterval(async () => {
		const fetchResponse = await axiosWithDefaults.get("/auth/session/")

		const shouldRefresh = fetchResponse.data.should_refresh

		if (!shouldRefresh) return

		const refreshResponse = await axiosWithDefaults.put("/auth/session/", {
			refresh_token: getRefreshToken(),
		})

		setRefreshToken(refreshResponse.data.refresh_token)
	}, REFRESH_INTERVAL)

	return () => {
		if (tokenRefreshLoop) clearInterval(tokenRefreshLoop)
		tokenRefreshLoop = null
	}
}

export {
	setRefreshToken,
	getRefreshToken,
	unsetRefreshToken,
	REFRESH_INTERVAL,
	REFRESH_TOKEN_KEY,
}

export default setupAuthTokenAutoRefresh
