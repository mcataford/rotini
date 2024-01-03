/*
 * Authentication queries
 *
 * This module contains the set of queries (both fetches and mutations) that
 * affect the user's session.
 *
 */
import { useMutation } from "@tanstack/react-query"
import { useLocationContext } from "../contexts/LocationContext"
import axiosWithDefaults from "../axios"

/*
 * Handles the log-out interaction.
 *
 * Using `logout` will instruct the application to invalidate
 * the current authentication token and will redirect the user
 * to the login page.
 */
function useLogout() {
	const { navigate } = useLocationContext()
	const logoutMutation = useMutation({
		mutationFn: async () => {
			return axiosWithDefaults.delete("/auth/session/")
		},
		onSuccess: () => {
			navigate("/login")
		},
	})

	const { mutate, isError, isPending, ...rest } = logoutMutation

	return {
		logout: mutate,
		isError,
		isPending,
	}
}

export { useLogout }

export default {
	useLogout,
}
