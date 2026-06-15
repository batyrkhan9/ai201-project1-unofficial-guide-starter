# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
This project builds an unofficial guide to Minerva University professors using student reviews collected from Rate My Professors. The domain covers 14 professors across Computer Science, Social Sciences, Arts and Humanities, and Business. This knowledge is valuable because it gives students honest insight into teaching style, exam difficulty, and grading fairness — information that is never shared through official Minerva channels because it is too candid and informal to appear in any university publication
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professors| Prof Subasic | https://www.ratemyprofessors.com/professor/3158936 |
| 2 | Rate My Professors| Prof Digby | https://www.ratemyprofessors.com/professor/2965507 |
| 3 | Rate My Professors| Prof Gale | https://www.ratemyprofessors.com/professor/2965451 |
| 4 | Rate My Professors| Prof Morar | https://www.ratemyprofessors.com/professor/2977249 |
| 5 | Rate My Professors| Prof Perry | https://www.ratemyprofessors.com/professor/2965452 |
| 6 | Rate My Professors| Prof Powers| https://www.ratemyprofessors.com/professor/2983398 |
| 7 | Rate My Professors| Prof Rios | https://www.ratemyprofessors.com/professor/3075440 |
| 8 | Rate My Professors| Prof Sealfon | https://www.ratemyprofessors.com/professor/3106280 |
| 9 | Rate My Professors| Prof Terrana | https://www.ratemyprofessors.com/professor/2962445 |
| 10 | Rate My Professors| Prof Volkan | https://www.ratemyprofessors.com/professor/2977238 |
| 11 | Rate My Professors| Prof Doering | https://www.ratemyprofessors.com/professor/2977244 |
| 12 | Rate My Professors| Prof Bentsen | https://www.ratemyprofessors.com/professor/2983399 |
| 13 | Rate My Professors| Prof Singh | https://www.ratemyprofessors.com/professor/2962474 |
| 14 | Rate My Professors| Prof Lawry | https://www.ratemyprofessors.com/professor/2965450 |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->
Each review is treated as a single chunk, split on the --- separator. Since reviews average 2 sentences and useful information is spread across both sentences, splitting smaller would destroy meaning. Chunk size is approximately 50-150 characters. No overlap is needed because reviews are independent opinions, the end of one review has no contextual relationship to the start of the next.


---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->
The embedding model used is all-MiniLM-L6-v2 via sentence-transformers, which runs locally with no API key required. For each query, the top 5 chunks (k=5) will be retrieved using cosine similarity search in ChromaDB. For a production system, tradeoffs to consider would include: OpenAI's text-embedding-ada-002 for higher accuracy at a cost, multilingual models if the student base is international, and context length limits for longer documents. 

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Which professor is considered the hardest at Minerva? | Not possible to get it from reviews, not enough info but closest ones are Prof Subasic and Prof Terrana |
| 2 | Which professor gives the most useful feedback? | Prof Rios |
| 3 | Who is the harshest grader at Minerva? | Prof Subasic or Prof Terrana |
| 4 | Which professor is the friendliest? | Prof Morar |
| 5 | What do students say about exam difficulty at Minerva? | Generally varies depending on the professor, but not possible to get from prof reviews. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Short reviews may not carry enough semantic signal for the embedding model to distinguish between professors accurately, leading to off-topic retrieval. 
2. Some professors have less reviews, meaning the system may not have enough content to answer questions about them confidently.
---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
I included it in the repo

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->
1. Ingestion and chunking: I will provide Claude with my Documents section and Chunking Strategy and ask it to implement a script that loads .txt files from the data folder, splits on ---, and outputs clean chunks with source metadata. 
2. Embedding and retrieval: I will provide Claude with my Retrieval Approach section and ask it to implement embedding with all-MiniLM-L6-v2 and storage in ChromaDB with source filenames as metadata. 
3. Generation: I will provide Claude with my grounding requirement and ask it to implement a prompt template that forces the LLM to answer only from retrieved chunks and append source citations.

