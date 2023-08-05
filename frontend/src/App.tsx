import { Box } from "@mui/material"

import NavigationBar from "./components/NavigationBar"
import FileList from "./components/FileList"
import FileDetails from "./components/FileDetails"
import AsyncTaskContext from "./contexts/AsyncTaskContext"
import LocationContext, { useLocationContext } from "./contexts/LocationContext"

const mockData = [
	{
		title: "Test file",
		filename: "testfile.txt",
		size: 1023,
		uid: "123",
	},
	{
		title: "Other file",
		filename: "testfile2.txt",
		size: 535346,
		uid: "456",
	},
]
const routeLabels = {
	ITEM_DETAILS: "item-details",
}

const routes = {
	[routeLabels.ITEM_DETAILS]: "/item/:itemId",
}

const App = () => {
	const { location } = useLocationContext()

	return (
		<Box sx={{ display: "flex", flexDirection: "column", width: "100%" }}>
			<NavigationBar />
			<Box component="main" sx={{ display: "flex", paddingTop: "10px" }}>
				<Box component="div" sx={{ flexGrow: 1 }}>
					<FileList data={mockData} />
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

const AppWithContexts = () => (
	<AsyncTaskContext>
		<LocationContext routes={routes}>
			<App />
		</LocationContext>
	</AsyncTaskContext>
)

export default AppWithContexts
