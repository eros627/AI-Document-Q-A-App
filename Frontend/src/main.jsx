import { StrictMode } from "react"
import { createDOM } from "react-dom/client"
import "./index.css"
import App from "./App"

createDOM(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
)
