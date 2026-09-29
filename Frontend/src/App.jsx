import { useState, useEffect } from "react"
import { supabase } from "./lib/supabase"
import AuthForm from "./components/AuthForm"
import Upload from "./pages/Upload"
import Chat from "./pages/Chat"

export default function App() {
  const [session, setSession] = useState(null)
  const [docId, setDocId] = useState(null)
  const [filename, setFilename] = useState("")

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
    })

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session)
    })

    return () => subscription.unsubscribe()
  }, [])

  function handleUploadSuccess(id, name) {
    setDocId(id)
    setFilename(name)
  }

  if (!session) return <AuthForm />

  if (!docId) {
    return <Upload
      onUploadSuccess={handleUploadSuccess}
      token={session.access_token}
    />
  }

  return <Chat
    docId={docId}
    filename={filename}
    token={session.access_token}
  />
}
