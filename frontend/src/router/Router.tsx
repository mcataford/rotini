import React, { Children } from "react"

import { useLocationContext } from "../contexts/LocationContext"

interface RouterProps {
	children: React.ReactNode
}

function Router({ children }: RouterProps) {
	const { location } = useLocationContext()
	const routerChildren = React.useMemo(
		() => Children.toArray(children),
		[children],
	)

	const matchingComponents = routerChildren.filter((child) => {
		if (typeof child !== "object") return false

		const childRoute = child as React.ReactElement

		return childRoute.props.path === location.pattern
	})

	if (matchingComponents.length !== 1) {
		throw new Error("Router failed to find what to render.")
	}

	return matchingComponents[0]
}

export default Router
