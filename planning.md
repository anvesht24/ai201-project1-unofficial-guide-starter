# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Student reviews of professors and courses at Florida Atlantic University
Students often pick classes without knowing what they're really like — the official catalog covers the syllabus, not the teaching, grading, or workload. This Unofficial Guide answers questions about professors and courses at Florida Atlantic University using real student reviews, with sources cited for every answer. It turns scattered, hard-to-find student feedback into clear, trustworthy answers students can actually use to plan their semester.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate my Professors| Student reviews of Prof. Ali Ibrahim |https://www.ratemyprofessors.com/professor/2832618|
| 2 | Coursicle| Student reviews of Prof. Ankur Agarwal | https://www.coursicle.com/fau/?professor=Ankur+Agarwal&type=reviews |
| 3 | Rate my Professors| Student reviews of Prof. Chang Hwan-Lee | https://www.ratemyprofessors.com/professor/2963915 |
| 4 | Rate my Professors| Student reviews of Prof. Fernando Koch | https://www.ratemyprofessors.com/professor/3026411 |
| 5 | Rate my Professors| Student reviews of Prof. Hanqi Zhuang | https://www.ratemyprofessors.com/professor/1728251 |
| 6 | Rate my Professors| Student reviews of Prof. Juan Yepes | https://www.ratemyprofessors.com/professor/2950560 |
| 7 | Rate my Professors| Student reviews of Prof. Maria Petrie | https://www.ratemyprofessors.com/professor/1347714 |
| 8 | Coursicle | Student reviews of Prof. Mihaela Cardei | https://www.coursicle.com/fau/?professor=Mihaela+Cardei&type=reviews |
| 9 | Rate my Professors| Student reviews of Prof. Veilbor Adzic | https://www.ratemyprofessors.com/professor/2950560 |
| 10 | Rate my Professors| Student reviews of Prof. Taghi Khoshgoftaar | https://www.ratemyprofessors.com/professor/105340|

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
300–600 characters — one student review

**Overlap:**
none

**Reasoning:**
Each review is a separate, self-contained opinion, so one review = one chunk; a blind character-split would cut reviews in half or merge two unrelated opinions, and overlap would just duplicate text since reviews don't flow into each other.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
all-MiniLM-L6-v2 (via sentence-transformers). I chose it because it runs locally with no API key or cost, it's fast, and it works well on short text like student reviews.
**Top-k:**
5. Each chunk is a single short review, so retrieving 5 gives the model a few different opinions to base its answer on, without adding too much irrelevant text.
**Production tradeoff reflection:**
If real users relied on this and cost wasn't a concern, I'd consider a stronger model for a few reasons. First, accuracy: reviews use slang and sarcasm ("easy A," "weeder class"), and a more advanced model might understand that tone better. Second, context length: MiniLM handles short text well, but if I later added long guides or syllabi, I'd need a model that accepts longer input. Third, local vs API: an API-hosted model might be more accurate, but it adds cost, latency, and a privacy concern, since I'd be sending user questions to an outside server.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about the dataset sizes and running the assignments in Ali Ibrahim's class? | The datasets are very large and some ML algorithms take a long time to run — one student said an assignment took hours to compile even on a decent computer. |
| 2 | Do Ankur Agarwal respond to emails? | Ankur Agarwal is very slow at replying to emails and slow in grading the assignments too. |
| 3 | How do students describe Chang Hwan-Lee's lecture?/teaching style? | Fast-paced, very math-heavy, hard to follow with weak explanations — some say attendance dropped to ~5–7 students; one notes lectures are optional since slides are posted. |
| 4 | How do students describe Cardei's teaching of difficult topics? | Clear and organized; she makes hard subjects (Automata, Algorithms/Data Structures) easier to grasp and re-explains in office hours. |
| 5 | Do students agree on whether Khoshgoftaar is a good professor? | No — strongly split: some say he's fair, high-expectations, and you learn a lot; others call him egocentric, biased, disorganized, with unclear grading. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.Conflicting reviews producing a one-sided answer.
Several of my professors have reviews that directly contradict each other — for example, students are sharply split on Khoshgoftaar, with some calling him fair and others calling him biased and disorganized. When the system retrieves a handful of these at once, it may latch onto one side and present it as the consensus, instead of reflecting that opinion is genuinely divided.
2.Lost source attribution because the professor's name isn't inside the chunk.
In my documents, the professor's name sits in the file header, not inside each individual review. Since I chunk by single review, most chunks contain the opinion but not the professor's name. If I don't attach the source (professor + URL) as metadata to each chunk during ingestion, retrieval could surface a complaint with no way to cite which professor or document it came from — which breaks the required source attribution.
---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
┌──────────────────────────────────────────────────────────────┐
│                  THE UNOFFICIAL GUIDE — PIPELINE               │
└──────────────────────────────────────────────────────────────┘

[1] Document Ingestion
    .txt files in /documents (RateMyProfessors + coursicle)
    Python: load each file, strip the header, keep source URL + professor
         |
         v
[2] Chunking
    Python: split on review boundaries (one review = one chunk)
         |
         v
[3] Embedding + Vector Store
    all-MiniLM-L6-v2 (sentence-transformers)  ->  ChromaDB
    each chunk stored with metadata (professor, source URL)
         |
         v
[4] Retrieval
    embed the query, run top-k = 5 semantic similarity search (ChromaDB)
         |
         v
[5] Generation
    Groq (llama-3.3-70b-versatile)
    grounded prompt: answer only from retrieved chunks + cite sources
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

**Milestone 3 — Ingestion and chunking:**
 I'll give Claude my Chunking Strategy section and ask it to write a function that loads each .txt file, separates the source header from the reviews, and splits the reviews so each one becomes its own chunk. I'll verify by checking the output produces one chunk per review and that each chunk keeps the professor name and source URL attached.
**Milestone 4 — Embedding and retrieval:**
I'll give Claude my Retrieval Approach section and ask it to embed each chunk with all-MiniLM-L6-v2, store the chunks in ChromaDB along with their metadata (professor name and source URL), and run a top-5 semantic similarity search for a query. I'll verify by searching a known complaint — for example "huge datasets that take forever to compile" — and checking that the matching Ali Ibrahim review comes back in the top results with its professor and source attached.
**Milestone 5 — Generation and interface:**
I'll give Claude my Generation plan and ask it to build a grounded prompt that answers only from the retrieved chunks and cites the source for each answer, plus a simple command-line loop where I can type a question and see the response. I'll verify by asking a question the documents don't cover and confirming the system says it doesn't have that information instead of making something up, and by checking that every answer includes a source citation.