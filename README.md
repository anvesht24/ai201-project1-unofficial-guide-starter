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
Student reviews of professors and courses at Florida Atlantic University
Students often pick classes without knowing what they're really like — the official catalog covers the syllabus, not the teaching, grading, or workload. This Unofficial Guide answers questions about professors and courses at Florida Atlantic University using real student reviews, with sources cited for every answer. It turns scattered, hard-to-find student feedback into clear, trustworthy answers students can actually use to plan their semester.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Rate my Professors| Student reviews of Prof. Ali Ibrahim |https://www.ratemyprofessors.com/professor/2832618|
| 2 | Coursicle| Student reviews of Prof. Ankur Agarwal | https://www.coursicle.com/fau/?professor=Ankur+Agarwal&type=reviews |
| 3 | Rate my Professors| Student reviews of Prof. Chang Hwan-Lee | https://www.ratemyprofessors.com/professor/2963915 |
| 4 | Rate my Professors| Student reviews of Prof. Fernando Koch | https://www.ratemyprofessors.com/professor/3026411 |
| 5 | Rate my Professors| Student reviews of Prof. Hanqi Zhuang | https://www.ratemyprofessors.com/professor/1728251 |
| 6 | Rate my Professors| Student reviews of Prof. Juan Yepes | https://www.ratemyprofessors.com/professor/2950560 |
| 7 | Rate my Professors| Student reviews of Prof. Maria Petrie | https://www.ratemyprofessors.com/professor/1347714 |
| 8 | Coursicle | Student reviews of Prof. Mihaela Cardei | https://www.coursicle.com/fau/?professor=Mihaela+Cardei&type=reviews |
| 9 | Rate my Professors| Student reviews of Prof. Veilbor Adzic | https://www.ratemyprofessors.com/professor/2950560 |
| 10 | Rate my Professors| Student reviews of Prof. Taghi Khoshgoftaar | https://www.ratemyprofessors.com/professor/105340

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

Small — one student review per chunk, roughly 300–600 characters.

**Overlap:**
None

**Why these choices fit your documents:**
My documents are collections of individual student reviews, and each review is a short, self-contained opinion — one talks about grading, another about workload, another about teaching style. They don't flow into each other, so I split on the blank lines between reviews, making each review its own chunk. I avoided a fixed character split because it would cut reviews in half or merge two unrelated opinions into one chunk, which would hurt retrieval. I used no overlap because overlap exists to keep a continuous idea from breaking across chunks, but my reviews are already independent, so overlap would only duplicate text and add noise. Before chunking, I also separated the header lines (Source and Professor) from the review text and stored them as metadata, so the professor name and source URL travel with each chunk for citations.

**Final chunk count:**
65 chunks across 10 documents.
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2, via sentence-transformers. I chose it because it runs locally with no API key and no rate limits, it's fast, and it works well on short text like student reviews — which made it a good fit for a free-stack project where my documents are all brief.

**Production tradeoff reflection:**
If real users relied on this and cost wasn't a concern, I'd consider a stronger model for a few reasons. First, accuracy: reviews use slang and sarcasm ("easy A," "weeder class"), and a more advanced model might understand that tone better. Second, context length: MiniLM handles short text well, but if I later added long guides or syllabi, I'd need a model that accepts longer input. Third, local vs API: an API-hosted model might be more accurate, but it adds cost, latency, and a privacy concern, since I'd be sending user questions to an outside server.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
The system prompt tells the model to answer using only the provided reviews, to reply "I don't have enough information on that." if they don't cover it, and not to use outside knowledge. The retrieved chunks are passed in as a labeled "Context:" block before the question, so the documents are the only material it has. Tested with an off-topic question (campus parking). It correctly refused instead of making something up.

**How source attribution is surfaced in the response:**
After retrieval, my code reads each chunk's metadata (professor + URL) and builds a deduplicated source list shown in the "Retrieved from" panel. Because it's built in code from metadata, citations are guaranteed rather than left to the LLM.
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about the dataset sizes and running the assignments in Ali Ibrahim's class? | The datasets are very large and some ML algorithms take a long time to run — one student said an assignment took hours to compile even on a decent computer. | According to the reviews, students mention that the datasets provided by Ali Ibrahim are HUGE, and running some of the machine learning algorithms takes a long time to compile. One student specifically stated that a certain assignment took hours to compile, even with a decent computer. | Relevant  | Accurate |
| 2 | Do Ankur Agarwal respond to emails? | Ankur Agarwal is very slow at replying to emails and slow at grading assignments too. | Says he does not consistently answer emails — one review notes he doesn't reply consistently, another says he gets hundreds of emails a day and rarely answers. | Relevant | Partially accurate |
| 3 | How do students describe Chang Hwan-Lee's lecture? | Fast-paced, very math-heavy, hard to follow with weak explanations; some say attendance dropped to ~5–7 students; one notes lectures are optional since slides are posted. | Says lectures are "a bit hard to follow" due to his accent and "dry as sandpaper," but optional since slides are on Canvas. | Partially relevant | Partially accurate |
| 4 | How do students describe Cardei's teaching of difficult topics? | Clear and organized; makes hard subjects (Automata, Algorithms/Data Structures) easier to grasp and re-explains in office hours. | Describes her as making concepts "easy to grasp," teaching style "clear, organized, and insightful," with online notes, recordings, and open-book tests that help with hard material. | Relevant | Accurate |
| 5 | Do students agree on whether Khoshgoftaar is a good professor? | No — strongly split: some say he's fair, high expectations, you learn a lot; others call him egocentric, biased, disorganized, with unclear grading. | "I don't have enough information on that. There is only one review of Taghi Khoshgoftaar, so I cannot compare opinions." | Off-target | Inaccurate |

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
"Do students agree on whether Khoshgoftaar is a good professor?"

**What the system returned:**
"I don't have enough information on that. There is only one review of Taghi Khoshgoftaar, so I cannot compare opinions."

**Root cause (tied to a specific pipeline stage):**

The failure happened at the retrieval stage, because of my top-k = 5 setting. Khoshgoftaar has far more than five reviews in my corpus, and they're split between people who think he's fair and demanding and people who think he's disorganized and biased. But retrieval only passes the 5 nearest chunks to the LLM, and for this query those 5 happened to land on a narrow slice of his reviews instead of the full range of opinion. So the model never actually saw the disagreement — from the limited context it was handed, there really did look like there was only one viewpoint. And it finally showed the grounding instruction which said it couldn't compare, rather than inventing a balanced answer. 

**What you would change to fix it:**
I would make retrieval adapt to the question. To my opinion, the fix is to raise top-k so more of a professor's reviews reach the model. A better fix is metadata filtering: when a question names a specific professor, retrieve all of that professor's chunks (using the professor metadata I already store) instead of just the global top 5, so the model sees the real spread of opinion before answering. This is also one of the stretch features, so I may implement it as an extension.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
Writing my Chunking Strategy in planning.md before I coded saved me a lot of trial and error. Because I'd already decided "one review = one chunk" based on reading my actual documents, I didn't waste time guessing at character counts when I built the chunker — I just implemented the rule I'd already reasoned out, and the chunk inspection passed on the first try. Having the architecture diagram also meant that at every stage I already knew what came next and which tool to use, so I was never stuck wondering what to build.

**One way your implementation diverged from the spec, and why:**
In planning.md I set top-k to 5 and assumed that was enough for any question. It worked well for specific questions, but my evaluation showed it wasn't enough for broad ones — when I asked whether students agreed about Khoshgoftaar, retrieval only returned 5 chunks that happened to cover one side, so the system thought there was just one opinion and refused to compare. That made me realize my spec's fixed top-k was an assumption that didn't hold for questions needing wide coverage of a single professor, which is something I'd change by adding professor-based filtering.
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

- *What I gave the AI:*My document structure (files of separate, short student reviews) and my Chunking Strategy from planning.md.
- *What it produced:*Its first approach was a fixed character-count split — chunk every ~500 characters.
- *What I changed or overrode:*I pushed back on that, because a blind character split would cut a review in half or merge two unrelated opinions into one chunk. I re-prompted it to split on the blank lines between reviews so each review became its own chunk, and to pull the header lines into metadata so the professor name and source URL stayed attached. After that change, my chunk inspection came back clean at 65 self-contained chunks.

**Instance 2**

- *What I gave the AI:*My grounding requirement — answer only from the retrieved reviews, refuse when the documents don't cover it, and cite sources.
- *What it produced:*A working generation function, but the first version leaned on the LLM to add citations itself and the grounding read more like a suggestion than a rule.
- *What I changed or overrode:*I tightened the system prompt to command it (answer from context only, and a fixed "I don't have enough information on that." refusal), and I moved source attribution into my own code — building the list from each chunk's metadata so citations are guaranteed, not left to the model. I confirmed it worked by asking an off-topic question (campus parking) and watching it refuse instead of inventing an answer.
