import { Box } from "@mui/material"
import {
	QueryClient,
	QueryClientProvider,
	useQuery,
} from "@tanstack/react-query"

import NavigationBar from "./components/NavigationBar"
import AsyncTaskContext from "./contexts/AsyncTaskContext"
import LocationContext from "./contexts/LocationContext"

import { Router, Route } from "./router"

import FileListView from "./components/FileListView"
import RegisterView from "./components/RegisterView"
import LoginView from "./components/LoginView"

const routeLabels = {
	ITEM_DETAILS: "item-details",
}

const routes = {
	[routeLabels.ITEM_DETAILS]: "/item/:itemId",
}

const App = () => {
	return (
		<Box sx={{ display: "flex", flexDirection: "column", width: "100%" }}>
			<NavigationBar />
			<Box component="main" sx={{ display: "flex", paddingTop: "10px" }}>
				<Router>
					<Route path="/">
						<FileListView />
					</Route>
					<Route path="/item/:itemId">
						<FileListView />
					</Route>
					<Route path="/register">
						<RegisterView />
					</Route>
					<Route path="/login">
						<LoginView />
					</Route>
				</Router>
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
