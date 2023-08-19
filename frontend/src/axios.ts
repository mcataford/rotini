import axios from "axios"

const axiosWithDefaults = axios.create({
	baseURL: "http://localhost:8000",
})

export default axiosWithDefaults
