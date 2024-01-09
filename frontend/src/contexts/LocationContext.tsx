import {
	useState,
	useMemo,
	useCallback,
	createContext,
	useContext,
	type ReactNode,
} from "react"

interface Location {
	path: string
	label: string | null
	params: {
		[key: string]: string
	}
	pattern: string
}

interface LocationContextData {
	location: Location
	navigate: (path: string) => void
}

const defaultValue = {
	location: {
		path: "",
		label: "",
		params: {},
		pattern: "",
	},
	navigate: () => {},
}

const _LocationContext = createContext<LocationContextData>(defaultValue)

/*
 * Matches the given path with a list of reference paths. Collects templated
 * arguments along the way.
 *
 * The template format is :<label> such that a path
 *
 * /item/:itemId/part/:partId/
 *
 * would match
 *
 * /item/1/part/2/
 *
 * with itemId = 1, partId = 2.
 *
 * Note that if no match is found, then a location without parameters is returned.
 */
function deriveLocation(
	path: string,
	urlMap: { [key: string]: Array<string> },
): Location {
	const splitPath = path.split("/").filter((part) => Boolean(part))

	for (const [label, pattern] of Object.entries(urlMap)) {
		// Cannot be a match if differing lengths.
		if (pattern.length !== splitPath.length) continue

		let collectedParts: { [key: string]: string } | undefined = {}

		for (let idx = 0; idx < pattern.length; idx++) {
			if (pattern[idx].startsWith(":")) {
				const patternLabel = pattern[idx].slice(1)
				collectedParts[patternLabel] = splitPath[idx]
			} else if (pattern[idx] !== splitPath[idx]) {
				collectedParts = undefined
				break
			} else continue
		}

		if (collectedParts !== undefined)
			return {
				path,
				label,
				pattern: `/${pattern.join("/")}`,
				params: collectedParts,
			}
	}

	return { path, pattern: path, label: null, params: {} }
}

/*
 * The LocationContext handles the current location (as defined by
 * globalThis.location.pathname) and parses URLs based on known
 * URL patterns.
 */
export function LocationContext({
	children,
	routes,
}: { children: ReactNode; routes: { [key: string]: string } }) {
	const splitUrlPatterns = useMemo(() => {
		return Object.entries(routes)
			.map(([label, pattern]: [string, string]): [string, Array<string>] => [
				label,
				pattern.split("/").filter((pattern) => Boolean(pattern)),
			])
			.reduce(
				(splitUrlMap, current) => {
					const [label, pattern] = current
					splitUrlMap[label] = pattern
					return splitUrlMap
				},
				{} as { [key: string]: Array<string> },
			)
	}, [routes])

	const [location, setLocation] = useState<Location>(
		deriveLocation(globalThis.location.pathname, splitUrlPatterns),
	)

	const navigate = useCallback(
		(path: string) => {
			history.pushState({}, "", path)
			setLocation(deriveLocation(path, splitUrlPatterns))
		},
		[splitUrlPatterns],
	)

	return (
		<_LocationContext.Provider value={{ location, navigate }}>
			{children}
		</_LocationContext.Provider>
	)
}

function useLocationContext() {
	return useContext(_LocationContext)
}

export default LocationContext

export { useLocationContext }
