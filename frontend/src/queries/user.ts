import { useQuery } from "@tanstack/react-query"

import axiosWithDefaults from "@/axios"

/*
 * Current user data fetch.
 *
 * This hook fetches data about the currently-authenticated user
 * if there is one and returns basic information about them as well
 * as a `isAuthenticated` flag that determines if we are logged in or not.
 */
function useCurrentUser() {
	const { data, isLoading, isError, isSuccess } = useQuery({
		queryKey: ["current-user"],
		queryFn: async () => {
			return axiosWithDefaults.get("/auth/user/")
		},
		retry: false,
	})

	const isAuthenticated = !isLoading && isSuccess && data.status === 200

	return { currentUser: data, isSuccess, isError, isLoading, isAuthenticated }
}

export { useCurrentUser }

export default { useCurrentUser }
