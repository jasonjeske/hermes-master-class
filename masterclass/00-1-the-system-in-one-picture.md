# The System in One Picture

Twelve articles describe nine subsystems. They fit together like this.

**The whole Hermes system, one graph**

```mermaid
flowchart TB
  subgraph INPUT["Ways in"]
    CLI["CLI / TUI / Desktop"]
    GW["Messaging gateways · 20+ platforms"]
    CRON["Cron scheduler · ticks every 60s"]
    API["OpenAI-compatible · API server"]
  end

  subgraph CORE["The agent loop, AIAgent in run_agent.py"]
    ASM["1. Prompt assembly · stable / context / volatile"]
    RES["2. Provider resolution · 18+ providers"]
    CMP["3. Preflight compression · at 50% of window"]
    CALL["4. API call · interruptible, with fallback"]
    PARSE["5. Response parsing"]
  end

  subgraph ACT["Acting on the world"]
    REG["Tool registry · 70+ tools / 28 toolsets"]
    SUB["Subagents · own context + budget"]
    BR["Browser + computer use"]
  end

  subgraph LEARN["What persists"]
    MEM["MEMORY.md + USER.md · ~1,300 tokens"]
    SK["Skills library · progressive disclosure"]
    SESS["Sessions · SQLite + FTS5"]
    KB["Kanban board · SQLite"]
  end

  CLI --> ASM
  GW --> ASM
  CRON --> ASM
  API --> ASM
  ASM --> RES --> CMP --> CALL --> PARSE
  PARSE -->|"text"| OUT["Response delivered"]
  PARSE -->|"tool_call"| REG
  REG --> SUB
  REG --> BR
  REG -->|"results appended"| CALL
  MEM -.->|"volatile tier"| ASM
  SK -.->|"stable tier index"| ASM
  SESS -.->|"history"| ASM
  KB -.->|"open work"| ASM
  OUT --> SESS
  OUT --> REVIEW["Background review · forked agent"]
  REVIEW -.->|"proposes"| MEM
  REVIEW -.->|"proposes"| SK
```

Read it as three rings. The **middle ring is the loop**, and it is the only part that is always running. The **top ring is every way a turn can start**, and the loop cannot tell them apart. The **bottom ring is what survives the turn**, which is the entire reason the system compounds instead of merely responding.

The dotted lines matter as much as the solid ones. Memory, skills, sessions and the board feed *into* prompt assembly, and the background review feeds back into memory and skills. That cycle is the learning system, and it is the difference between an agent and a chatbot with a plugin folder.

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
