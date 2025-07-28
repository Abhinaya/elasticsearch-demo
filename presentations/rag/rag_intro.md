---
marp: true
theme: gaia
paginate: true
class: invert
---

# Retrieval-Augmented Generation (RAG)
#### Empowering LLMs with Real-World, Up-to-Date Knowledge

---

## The Problem with LLMs Alone

LLMs are powerful but have limitations
  - Knowledge is frozen (training cut-off)
  - Cannot access private or recent data
  - Can hallucinate answers when unsure

**Example:**
> Q: Can Khadims Black Slip-On Shoes be washed with deteregent?
> GPT: I'm not familiar with the specific material or care instructions for Khadims Black Slip-On Shoe...

---

##  Enter RAG: Retrieval-Augmented Generation

- Combines search + generation
- Bridges LLMs with your data

### How it works

1. Retrieve relevant docs (e.g. from Elasticsearch)
2. Pass them into the LLM as context
3. LLM generates grounded answers

---
## Real Use Case: E-commerce Product QA

- Corpus: 1000 product reviews
- User question: "Can Khadims Black Slip-On Shoes be washed with deteregent?"

#### Without RAG
vague answer or hallucination

#### With RAG
uses actual product review: "Do not wash with detergent or in washing machine"

---

# Architecture Overview

```
User Query
   |
[Retriever: Elasticsearch or FAISS]
   |
Relevant Documents
   |
[LLM: Groq / GPT / Claude / Mistral]
   |
Generated Answer (grounded in facts)
```

---

# Benefits of RAG

- Uses your private / up-to-date data
- Reduces hallucination
- More trustworthy answers
- No need to fine-tune the LLM

---

# Ideal Datasets for RAG

- Product catalogs
- Support knowledge bases
- Legal documents
- Company policies
- Public FAQs or Wikis

---

# Summary

- LLMs alone = smart, but uninformed
- RAG = smart + informed
- Easy to plug into existing infra (e.g., Elasticsearch)
