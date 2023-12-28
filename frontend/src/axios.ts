import axios from "axios"

const axiosWithDefaults = axios.create({
	baseURL: "http://localhost:8000",
	withCredentials: true,
	xsrfHeaderName: "X-CSRFTOKEN",
	xsrfCookieName: "csrftoken",
})

export default axiosWithDefaults
