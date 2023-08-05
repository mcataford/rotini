import React from "react"
import ReactDOM from "react-dom/client"

import App from "./App"

const rootNode = document.getElementById("app")

if (!rootNode) throw new Error("Failed to find app root.")

const root = ReactDOM.createRoot(rootNode)

root.render(<App />)
