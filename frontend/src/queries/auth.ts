/*
 * Authentication queries
 *
 * This module contains the set of queries (both fetches and mutations) that
 * affect the user's session.
 *
 */
import { useQueryClient, useMutation } from "@tanstack/react-query"

import { useLocationContext } from "@/contexts/LocationContext"
import axiosWithDefaults from "@/axios"

/*
 * Handles the log-out interaction.
 *
 * Using `logout` will instruct the application to invalidate
 * the current authentication token and will redirect the user
 * to the login page.
 *
 * On success, the current-user query is invalidated so that the
 * application is made aware that the user is no longer authenticated.
 */
function useLogout() {
	const { navigate } = useLocationContext()
	const queryClient = useQueryClient()
	const logoutMutation = useMutation({
		mutationFn: async () => {
			return axiosWithDefaults.delete("/auth/session/")
		},
		onSuccess: async () => {
			await queryClient.invalidateQueries({ queryKey: ["current-user"] })
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

/*
 * Handles the log-in interaction.
 *
 * Using `login` will send a request to create a session and on success,
 * refetch the current user data.
 */
function useLogin() {
	const queryClient = useQueryClient()
	const { navigate } = useLocationContext()
	const { mutate, isError, failureReason, isPending } = useMutation({
		mutationFn: async ({
			email,
			password,
		}: { email: string; password: string }) => {
			return axiosWithDefaults.post("/auth/session/", {
				username: email,
				password,
			})
		},
		onSuccess: async () => {
			await queryClient.refetchQueries({ queryKey: ["current-user"] })
			navigate("/")
		},
	})

	return { login: mutate, isError, isPending }
}

export { useLogout, useLogin }

export default {
	useLogout,
	useLogin,
}
