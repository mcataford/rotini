import React from "react"

interface RouteProps {
	children: React.ReactNode
	path: string
}

function Route({ children }: RouteProps) {
	return children
}

export default Route
