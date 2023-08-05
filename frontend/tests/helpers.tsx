import { type ReactNode } from "react"
import { render } from "@testing-library/react"

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
		<LocationContext routes={contextValues.locationContext}>
			<AsyncTaskContext initialValue={contextValues.asyncTaskContext}>
				{component}
			</AsyncTaskContext>
		</LocationContext>,
	)
}
