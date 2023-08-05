import {
	createContext,
	useState,
	useCallback,
	useContext,
	type ReactNode,
} from "react"

interface UploadTaskData {
	type: string
	filename: string
	title: string
	size: number
}

type AsyncTask = UploadTaskData

interface AsyncTaskContextData {
	/* Tasks currently tracked by the system. */
	tasks: Array<AsyncTask>
	/* Utility to append a task to the tasklist. */
	addTask: (t: AsyncTask) => void
}

const defaultData: AsyncTaskContextData = { tasks: [], addTask: () => {} }

const _AsyncTaskContext = createContext<AsyncTaskContextData>(defaultData)

function AsyncTaskContext({
	children,
	initialValue,
}: { children: ReactNode; initialValue?: Array<AsyncTask> }) {
	const [asyncTaskData, setAsyncTaskData] = useState<Array<AsyncTask>>(
		initialValue ?? [],
	)

	const addTask = useCallback(
		(task: AsyncTask) => {
			setAsyncTaskData([...asyncTaskData, task])
		},
		[asyncTaskData, setAsyncTaskData],
	)

	return (
		<_AsyncTaskContext.Provider value={{ addTask, tasks: asyncTaskData }}>
			{children}
		</_AsyncTaskContext.Provider>
	)
}

/*
 * Hook exposing the asynchronous task data and utility functions.
 *
 * This relates to globally-available state tracking active async tasks
 * such as uploads or other processing.
 *
 * Returns an object with fields and functions that can be used
 * to manipulate this state, see return type.
 */
function useAsyncTaskContext(): AsyncTaskContextData {
	return useContext(_AsyncTaskContext)
}

export default AsyncTaskContext

export { useAsyncTaskContext, AsyncTaskContextData, AsyncTask, UploadTaskData }
