import { useState } from "react"

export default function Chat({ docId, filename }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)

  async function handleAsk() {
    if (!input.trim() || loading) return

    const question = input.trim()
    setInput("")
    setLoading(true)

    setMessages((prev) => [
      ...prev,
      { role: "user", content: question },
      { role: "assistant", content: "" },
    ])

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/chat/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, doc_id: docId }),
      })

      const reader = res.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const token = decoder.decode(value)

        setMessages((prev) => {
          const updated = [...prev]
          updated[updated.length - 1] = {
            role: "assistant",
            content: updated[updated.length - 1].content + token,
          }
          return updated
        })
      }
    } catch (e) {
      setMessages((prev) => {
        const updated = [...prev]
        updated[updated.length - 1] = {
          role: "assistant",
          content: "Something went wrong.",
        }
        return updated
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <div className="bg-white shadow px-6 py-4">
        <h1 className="text-lg font-semibold text-gray-800">Chatting with: {filename}</h1>
      </div>

      <div className="flex-1 overflow-y-auto px-6 py-4 flex flex-col gap-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`max-w-xl px-4 py-3 rounded-2xl text-sm whitespace-pre-wrap ${
              msg.role === "user"
                ? "bg-blue-600 text-white self-end"
                : "bg-white text-gray-800 self-start shadow"
            }`}
          >
            {msg.content}
          </div>
        ))}
      </div>

      <div className="bg-white border-t px-6 py-4 flex gap-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          placeholder="Ask a question about your document..."
          className="flex-1 border rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={handleAsk}
          disabled={loading || !input.trim()}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "..." : "Ask"}
        </button>
      </div>
    </div>
  )
}
