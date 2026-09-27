import { useState } from "react"
import Upload from "./pages/Upload"
import Chat from "./pages/Chat"

export default function App() {
  const [docId, setDocId] = useState(null)
  const [filename, setFilename] = useState("")

  function handleUploadSuccess(id, name) {
    setDocId(id)
    setFilename(name)
  }

  if (!docId) {
    return <Upload onUploadSuccess={handleUploadSuccess} />
  }

  return <Chat docId={docId} filename={filename} />
}
