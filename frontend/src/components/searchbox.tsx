import { useState } from "react";

type ChatResponse = {
  answer: string;
  source: {
    video_id: string;
    video_title: string;
    timestamp: string;
    youtube_url: string;
    embed_url: string;
    score: number;
  };
};

export default function SearchBox() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState<ChatResponse | null>(null);

  async function handleSubmit() {
    const response = await fetch("http://localhost:8000/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();

    setResult(data);
  }

  return (
    <div className="min-h-screen bg-zinc-950 px-4 py-12 text-white">
      <div className="mx-auto max-w-4xl">

        {/* Hero */}
        <div className="mb-15 text-center">
          <div className="mb-5 mt-20 inline-flex items-center rounded-full border border-zinc-800 bg-zinc-900 px-4 py-2 text-sm text-zinc-400">
            ✦ AI powered YouTube RAG
          </div>

          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
            Ask your playlist
          </h1>

          <p className="mx-auto mt-4 max-w-xl text-zinc-400">
            Ask questions about your YouTube lectures and get answers
            directly from the videos.
          </p>
        </div>

        {/* Search */}
        <div className="rounded-2xl border border-zinc-800 bg-zinc-900/70 p-3 shadow-2xl">
          <div className="flex flex-col gap-3 sm:flex-row">

            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask something about the playlist..."
              className="flex-1 rounded-xl border border-zinc-800 bg-zinc-950 px-5 py-4 text-white placeholder-zinc-600 outline-none transition focus:border-zinc-600"
            />

            <button
              onClick={handleSubmit}
              className="rounded-xl bg-white px-8 py-4 font-semibold text-black transition hover:bg-zinc-200 hover:cursor-pointer"
            >
              Ask →
            </button>

          </div>
        </div>

        {/* Result */}
        {result && (
          <div className="mt-10 space-y-6">

            {/* Answer */}
            <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">

              <div className="mb-4 flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-zinc-800">
                  ✦
                </div>

                <div>
                  <p className="font-semibold">
                    Answer
                  </p>

                  <p className="text-xs text-zinc-500">
                    Based on your playlist
                  </p>
                </div>
              </div>

              <p className="leading-7 text-zinc-300">
                {result.answer}
              </p>

            </div>

            {/* Source */}
            {result.source && (
              <div className="overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900">

                {/* Video */}
                <div className="bg-black">
                  <iframe
                    src={result.source.embed_url}
                    className="aspect-video w-full"
                    allowFullScreen
                    title={result.source.video_title}
                  />
                </div>

                {/* Video Information */}
                <div className="p-6">

                  {/* <div className="mb-5">
                    <p className="mb-2 text-xs font-medium uppercase tracking-wider text-zinc-500">
                      Source Video
                    </p>

                    <h2 className="text-xl font-semibold text-white">
                      {result.source.video_title}
                    </h2>
                  </div> */}

                  {/* Metadata */}
                  <div className="grid grid-cols-5 ">

                    <div >
                      <p className="text-xs text-zinc-500">
                        Timestamp
                      </p>

                      <p className="mt-0 font-mono font-semibold text-white">
                        {result.source.timestamp}
                      </p>
                    </div>

                    {/* <div className="rounded-xl border border-zinc-800 bg-zinc-950 px-4 py-3">
                      <p className="text-xs text-zinc-500">
                        Relevance
                      </p>

                      <p className="mt-1 font-mono font-semibold text-white">
                        {result.source.score.toFixed(3)}
                      </p>
                    </div> */}


                  {/* YouTube Button */}
                  <div>
                  <a
                    href={result.source.youtube_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="h-12  w-50 inline-flex items-center rounded-xl bg-red-500 px-5  text-sm font-semibold text-white transition hover:bg-zinc-200"
                  >
                    Watch on YouTube
                    <span className="ml-2">↗</span>
                  </a>

                  </div>
                  </div>

                </div>
              </div>
            )}

          </div>
        )}

      </div>
    </div>
  );
}