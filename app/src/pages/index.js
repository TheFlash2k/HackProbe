import React, { useEffect, useState } from "react";
import icon from '../../public/favicon.jpg'
import Image from "next/image";
import { ArrowDownward, ArrowDropDown, DoubleArrow, KeyboardArrowDown } from "@mui/icons-material";

function Home() {
  const [containerIndex2, setContainerIndex2] = useState([])
  const [containerIndex, setContainerIndex] = useState([])
  const [copiedIndex2, setCopiedIndex2] = useState(0)
  const [isRotated, setIsRotated] = useState([])
  const [isRotated2, setIsRotated2] = useState([])
  const [copiedIndex, setCopiedIndex] = useState(0)
  const [iconHide, setIconHide] = useState(false)
  const [copied, setCopied] = useState(false)
  const [term, setTerm] = useState([])
  const [data, setData] = useState()

  const termParser = (e) => {
    let terms = e.target.value
    if (terms.length === 0) {
      setTerm("")
    } else {
      setTerm(terms.split(" "))
    }
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
    } else {
      setData(null)
    }
  }, [term])
  return (
    <div>
      <div onClick={() => setIconHide(!iconHide)} className={"flex justify-center items-center cursor-pointer" + (iconHide ? " hidden" : " block")}>
        <Image src={icon} alt="Image" width={200} height={200} />
      </div>
      <div>
        <h1 className="text-4xl font-bold text-center mt-8">HackProbe - A JSON-based search Engine</h1>
      </div>
      <div className="flex justify-center items-center w-full">
        <input type="text" id="search" onChange={termParser} className="shadow border rounded mt-8 mb-6 py-2 px-3 dark:text-gray-300 text-gray-700 leading-tight focus:outline-none focus:shadow-outline w-[60%]" placeholder="Enter tags to search from." />
      </div>

      <div>
        {data && data.results.map((result, index) => {
          return (
            <div key={index} className="border-2 border-white rounded-xl p-8 m-2">
              {result.commands.map((command, index2) => (
                <div key={index2} className="flex w-full">
                  <div className={"relative flex flex-col justify-start items-start mb-4 p-4 rounded-xl bg-gray-700 shadow-xl w-full overflow-hidden"}>
                    <div className="absolute top-0 right-0 p-2">
                      <KeyboardArrowDown className={`cursor-pointer transition-transform transform ${(result.commands.length > 1 ? isRotated2.includes(index2) : isRotated.includes(index)) ? ' -rotate-90' : ' rotate-0'}`}
                        onClick={() => {
                          if (!(result.commands.length > 1 ? isRotated2.includes(index2) : isRotated.includes(index))) {
                            setContainerIndex(prevIndices => [...prevIndices, index]);
                            if (result.commands.length > 1) {
                              console.log(containerIndex2.includes(index2))
                              setContainerIndex2(prevIndices2 => [...prevIndices2, index2]);
                            }

                          }
                          else {
                            setContainerIndex(prevIndices => prevIndices.filter(i => i !== index));
                            if (result.commands.length > 1) {
                              console.log(containerIndex2.includes(index2))
                              setContainerIndex2(prevIndices2 => prevIndices2.filter(i => i !== index2));
                            }
                          }
                          if ((result.commands.length > 1 ? isRotated2.includes(index2) : isRotated.includes(index))) {
                            setIsRotated(prevIndices => prevIndices.filter(i => i !== index));
                            if (result.commands.length > 1) {
                              console.log(containerIndex2.includes(index2))
                              setIsRotated2(prevIndices2 => prevIndices2.filter(i => i !== index2))
                            }
                          } else {
                            setIsRotated(prevIndices => [...prevIndices, index]);
                            if (result.commands.length > 1) {
                              console.log(containerIndex2.includes(index2))
                              setIsRotated2(prevIndices2 => [...prevIndices2, index2]);
                            }
                          }
                        }} />
                    </div>
                    <div className="flex justify-start items-center">
                      <h1 className="font-bold text-xl mr-2">Command: </h1>
                      <div className="bg-[#756f6f38] dark:bg-gray-500 py-1 px-2 w-fit rounded-md hover:cursor-pointer font-mono" onClick={async () => {
                        navigator.clipboard.writeText(command.cmd)
                        setCopied(true)
                        setCopiedIndex(index)
                        setCopiedIndex2(index2)
                        await sleep(3000)
                        setCopied(false)
                      }}>{command.cmd}</div>
                      {index === copiedIndex && index2 === copiedIndex2 ? <div key={index} className="text-green-600 font-bold ml-2">
                        {copied ? "Copied!" : ""}
                      </div> : <></>}
                    </div>
                    {(result.commands.length > 1 ? (containerIndex2.includes(index2)) : containerIndex.includes(index)) ? <></> : <>
                      <div className="flex justify-start items-end mt-4">
                        <h1 className="font-bold text-xl mr-2">Description: </h1>
                        <p>{command.description}</p>
                      </div>
                      <div className="flex justify-start items-center mt-4">
                        <h1 className="font-bold text-xl mr-2">Example: </h1>
                        <p>{command.examples[0]}</p>
                      </div>
                    </>}
                  </div>
                </div>
              ))}
              <div className="flex justify-start items-center my-4">
                <h1 className="font-bold text-xl mr-2">Description: </h1>
                <p>{result.description}</p>
              </div>
              {
                result.tags.map((tag, index) => (
                  <span key={index} className="bg-gray-600 dark:bg-gray-200 rounded-full px-2 py-1 text-sm font-semibold dark:text-gray-700 text-gray-100 mr-2">{tag}</span>
                ))
              }
            </div>

          )
        })}
      </div>
    </div >
  )
}

export default Home