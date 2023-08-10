import React, { useEffect, useState } from "react";
import Head from 'next/head'

function Home() {
  const [term, setTerm] = useState([])
  const [data, setData] = useState()
  const [copied, setCopied] = useState(false)
  const [copiedIndex, setCopiedIndex] = useState(0)

  const termParser = (e) => {
    let terms = e.target.value
    setTerm(terms.split(" "))
  }

  const searchTag = async () => {
    let options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ term })
    }
    const res = await fetch('/api/search', options)
    const data = await res.json()
    setData(data)
  }

  const sleep = async (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms));
  }



  useEffect(() => {
    if (term.length !== 0) {
      searchTag()
    }
  }, [term])
  return (
    <div>
      <Head>
        <title>
          HackProbe - The Search Engine
        </title>
        <link rel="shortcut icon" href="/favicon.ico" />
      </Head>
      <div>
        <h1 className="text-4xl font-bold text-center mt-8">HackProbe - A JSON-based search Engine</h1>
      </div>
      <div className="flex justify-center items-center w-full">
        <input type="text" id="search" onChange={termParser} className="shadow border rounded mt-8 mb-6 py-2 px-3 dark:text-gray-300 text-gray-700 leading-tight focus:outline-none focus:shadow-outline w-[60%]" placeholder="Enter tags to search from." />
      </div>

      <div>
        {data && data.results.map((result, index) => {
          return (
            <div key={index} className="border-2 border-red rounded p-8 m-2">
              <div className="flex justify-start items-center">
                <h1 className="font-bold text-xl mr-2">Command: </h1>
                <div className="bg-[#756f6f38] dark:bg-gray-500 py-1 px-2 w-fit rounded-md hover:cursor-pointer font-mono" onClick={async () => {
                  navigator.clipboard.writeText(result.commands[0].cmd)
                  setCopied(true)
                  setCopiedIndex(index)
                  await sleep(3000)
                  setCopied(false)
                }}>{result.commands[0].cmd}</div>
                {index === copiedIndex ? <div key={index} className="text-green-600 font-bold ml-2">
                  {copied ? "Copied!" : ""}
                </div> : <></>}
              </div>
              <div className="flex justify-start items-end mt-4">
                <h1 className="font-bold text-xl mr-2">Description: </h1>
                <p>{result.commands[0].description}</p>
              </div>
              <div className="flex justify-start items-center my-4">
                <h1 className="font-bold text-xl mr-2">Example: </h1>
                <p>{result.commands[0].examples[0]}</p>
              </div>
              {
                result.tags.map((tag, index) => (
                  <span key={index} className="bg-gray-600 dark:bg-gray-200 rounded-full px-2 py-1 text-sm font-semibold dark:text-gray-700 text-gray-100 mr-2">{tag}</span>
                ))
              }
            </div>)
        })}
      </div>
    </div >
  )
}

export default Home