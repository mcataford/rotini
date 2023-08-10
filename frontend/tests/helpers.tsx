import { type ReactNode } from "react"
import { render } from "@testing-library/react"
import { QueryClientProvider, QueryClient } from "@tanstack/react-query"

import AsyncTaskContext, {
	type AsyncTask,
} from "../src/contexts/AsyncTaskContext"
import LocationContext from "../src/contexts/LocationContext"

interface ContextInitialValues {
	asyncTaskContext: Array<AsyncTask>
	locationContext: { [key: string]: string }
}

const defaultContextValues = {
	asyncTaskContext: [],
	locationContext: { default: "/" },
}

export function renderWithContexts(
	component: ReactNode,
	initialValues?: Partial<ContextInitialValues>,
) {
	const contextValues = { ...defaultContextValues, ...(initialValues ?? {}) }
	return render(
		<QueryClientProvider client={new QueryClient()}>
			<LocationContext routes={contextValues.locationContext}>
				<AsyncTaskContext initialValue={contextValues.asyncTaskContext}>
					{component}
				</AsyncTaskContext>
			</LocationContext>
		</QueryClientProvider>,
	)
}
