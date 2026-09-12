import { useState } from "react"

export default function Upload({ onUploadSuccess }) {
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState("")
  const [loading, setLoading] = useState(false)

  async function handleUpload() {
    if (!file) return
    setLoading(true)
    setStatus("")

    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/documents/upload`, {
        method: "POST",
        body: formData,
      })

      if (!res.ok) {
        const err = await res.json()
        setStatus(`Error: ${err.detail}`)
        return
      }

      const data = await res.json()
      setStatus(`Uploaded! ${data.chunks_stored} chunks stored.`)
      onUploadSuccess(data.doc_id, file.name)
    } catch (e) {
      setStatus("Could not reach the server.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 gap-6">
      <h1 className="text-3xl font-bold text-gray-800">AI Document Q&A</h1>
      <div className="bg-white rounded-2xl shadow p-8 flex flex-col gap-4 w-full max-w-md">
        <label className="text-sm font-medium text-gray-600">Upload a PDF</label>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="text-sm text-gray-500"
        />
        <button
          onClick={handleUpload}
          disabled={!file || loading}
          className="bg-blue-600 text-white rounded-lg py-2 font-medium hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Uploading..." : "Upload & Process"}
        </button>
        {status && <p className="text-sm text-gray-600">{status}</p>}
      </div>
    </div>
  )
}
