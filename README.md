# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
This project builds an unofficial guide to Minerva University professors using student reviews collected from Rate My Professors. The domain covers 14 professors across Computer Science, Social Sciences, Arts and Humanities, and Business. This knowledge is valuable because it gives students honest insight into teaching style, exam difficulty, and grading fairness, information that is never shared through official Minerva channels because it is too candid and informal to appear in any university publication.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
Each review is one chunk, approximately 50-150 characters. Split on --- separator.
**Overlap:**
No overlap. Reviews are independent opinions with no contextual relationship between them.
**Why these choices fit your documents:**
Reviews average 2 sentences and useful information is spread across both sentences. Splitting smaller would destroy meaning. Since each review stands alone, overlap would add noise rather than context.
**Final chunk count:**
40 chunks across 14 documents.
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 via sentence-transformers. Runs locally with no API key or rate limits.

**Production tradeoff reflection:**
For a production deployment, I would consider OpenAI's text-embedding-ada-002 for higher accuracy at a per-token cost. Since Minerva is an international university with students from many countries, multilingual support would also be important, a model like multilingual-e5-large would handle non-English reviews better. The main tradeoff is cost and latency versus accuracy. all-MiniLM-L6-v2 is fast and free but was trained on general text, not student reviews specifically, which may reduce accuracy on domain-specific language.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
You are an assistant for Minerva University students.
Answer the question using ONLY the information provided in the documents below.
If the documents don't contain enough information to answer, say 'I don't have enough information on that.'
Always be specific and cite which professor you are referring to.
**How source attribution is surfaced in the response:**
Source filenames are collected from ChromaDB metadata for each retrieved chunk and returned alongside the answer. The Gradio interface displays them in a separate "Retrieved from" field.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which professor is considered the hardest at Minerva? | Either Prof Subasic or Terrana |Found Terrana but hedged, said couldn't confirm definitively|Partially relevant | Partially accurate |
| 2 | Which professor gives the most useful feedback? | Prof Rios | Couldn't identify professor by name, quoted review without attribution | Off-target | Inaccurate |
| 3 | Who is the harshest grader at Minerva? | Either Prof Subasic or Terrana | Correctly identified Terrana | Relevant | Accurate |
| 4 | Which professor is the friendliest? | Prof Perry or Rios | Found friendly descriptions but couldn't name the professor | Partially relevant | Partially Accurate |
| 5 | What do students say about exam difficulty at Minerva? | Not possible to understand from prof reviews, but not easy exams | Returned no relevant information, said insufficient data | Off-target | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Which professor gives the most useful feedback?
**What the system returned:**
The system found a review mentioning "gives really helpful feedback" but could not identify which professor it referred to, returning a vague answer without a name.
**Root cause (tied to a specific pipeline stage):**
The failure occurred at the chunking stage. Original chunks contained only review text without professor names embedded in the chunk itself. The professor name only existed in the filename metadata, which the LLM cannot see directly, it only receives the chunk text. This meant retrieved chunks had relevant content but no attribution. After adding "Professor: [name]" to each review, results improved for some questions but not all, because some reviews still used indirect references like "this prof" rather than explicit names.
**What you would change to fix it:**
Ensure every chunk explicitly contains the professor's name in the text. Additionally, use a larger k value to retrieve more chunks, increasing the chance that at least one chunk contains both the professor's name and the relevant information.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
Writing the chunking strategy in planning.md before coding forced me to think about the structure of my documents first. Because I had decided that each review should be one chunk split on ---, implementing the ingestion script was straightforward, I knew exactly what the output should look like before writing a single line of code.

**One way your implementation diverged from the spec, and why:**
The spec did not anticipate that professor names would be missing from chunk text, only present in filenames. This caused retrieval failures where the system found relevant content but couldn't attribute it to a specific professor. I had to go back and modify all 14 .txt files to prepend "Professor: [name]" to each review, a preprocessing step not in the original plan.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* My chunking strategy from planning.md and document structure (short reviews separated by ---) 
- *What it produced:* An ingest.py script that loads .txt files, splits on ---, filters empty chunks, and attaches source filename as metadata
- *What I changed or overrode:* Added professor names to each review after discovering the system couldn't attribute retrieved chunks to specific professors

**Instance 2**

- *What I gave the AI:* What I gave the AI: My grounding requirement and retrieval approach from planning.md
- *What it produced:* A query.py script with a system prompt enforcing grounded generation, ChromaDB retrieval, and Groq LLM integration
- *What I changed or overrode:* Kept k=5 for retrieval after testing showed it returned a good balance of relevant and diverse chunks