import { Box } from "@mui/material"
import { QueryClient, QueryClientProvider, useQuery } from "react-query"

import NavigationBar from "./components/NavigationBar"
import FileList from "./components/FileList"
import FileDetails from "./components/FileDetails"
import AsyncTaskContext from "./contexts/AsyncTaskContext"
import LocationContext, { useLocationContext } from "./contexts/LocationContext"
import { useOwnFileList } from "./queries/files"

const routeLabels = {
	ITEM_DETAILS: "item-details",
}

const routes = {
	[routeLabels.ITEM_DETAILS]: "/item/:itemId",
}

const App = () => {
	const { location } = useLocationContext()
	const { isLoading, data } = useOwnFileList()

	if (isLoading) return

	return (
		<Box sx={{ display: "flex", flexDirection: "column", width: "100%" }}>
			<NavigationBar />
			<Box component="main" sx={{ display: "flex", paddingTop: "10px" }}>
				<Box component="div" sx={{ flexGrow: 1 }}>
					<FileList data={data} />
				</Box>
				{location.label === routeLabels.ITEM_DETAILS ? (
					<Box component="div" sx={{ flexGrow: 1 }}>
						<FileDetails itemId={location.params.itemId} />
					</Box>
				) : null}
			</Box>
		</Box>
	)
}

const queryClient = new QueryClient()

const AppWithContexts = () => (
	<QueryClientProvider client={queryClient}>
		<AsyncTaskContext>
			<LocationContext routes={routes}>
				<App />
			</LocationContext>
		</AsyncTaskContext>
	</QueryClientProvider>
)

export default AppWithContexts
