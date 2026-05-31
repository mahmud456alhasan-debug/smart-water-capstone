<div align="center">

# 📚 Weekly Lab Reports — Smart Water Lab

**Mahmudul Hasan (4125999049)** · Xi'an Jiaotong University · 2026

*Course lab progression — from first AI script to capstone demo*

[![Lab Sessions](https://img.shields.io/badge/Sessions-16-blue?style=for-the-badge&logo=gitbook&logoColor=white)](#-report-index)
[![PDF Reports](https://img.shields.io/badge/PDF_Reports-16-red?style=for-the-badge&logo=adobe-acrobat-reader&logoColor=white)](#-report-index)
[![Appendix Code](https://img.shields.io/badge/Appendix_Folders-12-success?style=for-the-badge&logo=python&logoColor=white)](#-appendix-code-folders)
[![Back to Repo](https://img.shields.io/badge/←_Main_Repository-Home-lightgrey?style=for-the-badge)](../README.md)

</div>

---

## 🖼️ Lab highlights

<p align="center">
  <img src="week5_session_a_lab1_streamlit.png" alt="Week 5 Lab 1 — Rainfall alert Streamlit dashboard" width="24%" />
  <img src="week5_session_b_lab2_sensitivity.png" alt="Week 5 Lab 2 — SCS-CN runoff sensitivity curve" width="24%" />
  <img src="week6_session_a_lab3_tradeoff.png" alt="Week 6 Lab 3 — Reservoir revenue vs ecology trade-off" width="24%" />
  <img src="week6_session_b_lab4_dem.png" alt="Week 6 Lab 4 — Flood inundation DEM heatmap" width="24%" />
</p>

<p align="center">
  <em>🌧️ Rainfall alerts · 💧 Runoff modeling · ⚖️ Reservoir dispatch · 🌊 Flood mapping</em>
</p>

---

## 📊 At a glance

| | |
|:--|:--|
| 📅 **Duration** | Weeks 1–8 (16 sessions) |
| 📄 **Deliverables** | 16 LaTeX reports + 16 compiled PDFs |
| 🐍 **Appendix code** | 44 Python files · 57 screenshots · prompt logs |
| 🎯 **Outcome** | Foundations for 4 specialized experiments + capstone |

---

## 🗺️ Learning journey

```mermaid
flowchart LR
    W1["🛠️ Week 1–2<br/>AI setup & CoT"]
    W3["🧪 Week 3–4<br/>TDD & refactor"]
    W5["💧 Week 5–6<br/>Labs 1–4"]
    W7["🚀 Week 7–8<br/>Capstone"]
    W1 --> W3 --> W5 --> W7
    W5 --> E1["Exp 1 Rainfall"]
    W5 --> E2["Exp 2 Runoff"]
    W6 --> E3["Exp 3 Reservoir"]
    W6 --> E4["Exp 4 Flood"]
    W7 --> CAP["Capstone app"]
```

| Phase | Weeks | Focus | Emoji |
|-------|:-----:|-------|:-----:|
| **Foundation** | 1–2 | Environment setup, Chain-of-Thought, AGENTS.md | 🧠 |
| **Engineering** | 3–4 | Agile scaffolding, TDD, refactoring, integration | ⚙️ |
| **Specialized labs** | 5–6 | Labs 1–4 → Experiments 1–4 | 💧 |
| **Capstone** | 7–8 | Planning, development, testing, demo & defense | 🏁 |

---

## 📸 Report snapshots

<details open>
<summary><strong>🛠️ Weeks 1–2 — AI foundations</strong></summary>
<br>

<p align="center">
  <img src="week1_session_a_opencode.png" alt="Week 1 Session A — OpenCode setup" width="32%" />
  <img src="week2_session_a_terminal.png" alt="Week 2 Session A — terminal output" width="32%" />
  <img src="week2_session_b_opencode.png" alt="Week 2 Session B — AGENTS.md context" width="32%" />
</p>

| Session | Topic | Open report |
|---------|-------|-------------|
| 1A | Environment setup & first AI script | [📄 PDF](Week1_SessionA_Report.pdf) · [📝 TeX](Week1_SessionA_Report.tex) |
| 1B | AI mental models (Chain-of-Thought) | [📄 PDF](Week1_SessionB_Report.pdf) · [📝 TeX](Week1_SessionB_Report.tex) |
| 2A | Chain-of-Thought prompting | [📄 PDF](Week2_SessionA_Report.pdf) · [📝 TeX](Week2_SessionA_Report.tex) |
| 2B | Context engineering (AGENTS.md) | [📄 PDF](Week2_SessionB_Report.pdf) · [📝 TeX](Week2_SessionB_Report.tex) |

</details>

<details>
<summary><strong>⚙️ Weeks 3–4 — Software engineering practice</strong></summary>
<br>

<p align="center">
  <img src="week3_session_a_terminal.png" alt="Week 3 Session A — pytest output" width="32%" />
  <img src="week3_session_b_terminal_refactor.png" alt="Week 3 Session B — refactor tests" width="32%" />
  <img src="week4_session_b_streamlit.png" alt="Week 4 Session B — Streamlit integration" width="32%" />
</p>

| Session | Topic | Open report |
|---------|-------|-------------|
| 3A | Agile scaffolding practice | [📄 PDF](Week3_SessionA_Report.pdf) · [📝 TeX](Week3_SessionA_Report.tex) |
| 3B | Test-driven development | [📄 PDF](Week3_SessionB_Report.pdf) · [📝 TeX](Week3_SessionB_Report.tex) |
| 4A | Refactoring & migration | [📄 PDF](Week4_SessionA_Report.pdf) · [📝 TeX](Week4_SessionA_Report.tex) |
| 4B | Integration & flow practice | [📄 PDF](Week4_SessionB_Report.pdf) · [📝 TeX](Week4_SessionB_Report.tex) |

📁 Code: [week3_session_a_files/](week3_session_a_files/) · [week3_session_b_files/](week3_session_b_files/) · [week4_session_a_files/](week4_session_a_files/) · [week4_session_b_files/](week4_session_b_files/)

</details>

<details open>
<summary><strong>💧 Weeks 5–6 — Specialized labs (Experiments 1–4)</strong></summary>
<br>

<p align="center">
  <img src="week5_session_a_lab1_streamlit.png" alt="Lab 1 rainfall dashboard" width="23%" />
  <img src="week5_session_b_lab2_sensitivity.png" alt="Lab 2 runoff sensitivity" width="23%" />
  <img src="week6_session_a_lab3_tradeoff.png" alt="Lab 3 reservoir trade-off" width="23%" />
  <img src="week6_session_b_lab4_comparison.png" alt="Lab 4 flood level comparison" width="23%" />
</p>

| Week | Session | Topic | → Experiment | Report |
|:----:|:-------:|-------|:------------:|--------|
| 5 | A | **Lab 1** — Rainfall alert | Exp 1 🌧️ | [📄 PDF](Week5_SessionA_Lab1_Report.pdf) · [📝 TeX](Week5_SessionA_Lab1_Report.tex) |
| 5 | B | **Lab 2** — SCS-CN runoff | Exp 2 💧 | [📄 PDF](Week5_SessionB_Lab2_Report.pdf) · [📝 TeX](Week5_SessionB_Lab2_Report.tex) |
| 6 | A | **Lab 3** — Reservoir optimization | Exp 3 ⚖️ | [📄 PDF](Week6_SessionA_Lab3_Report.pdf) · [📝 TeX](Week6_SessionA_Lab3_Report.tex) |
| 6 | B | **Lab 4** — Flood inundation | Exp 4 🌊 | [📄 PDF](Week6_SessionB_Lab4_Report.pdf) · [📝 TeX](Week6_SessionB_Lab4_Report.tex) |

📁 Code & figures: [week5_session_a_lab1_files/](week5_session_a_lab1_files/) · [week5_session_b_lab2_files/](week5_session_b_lab2_files/) · [week6_session_a_lab3_files/](week6_session_a_lab3_files/) · [week6_session_b_lab4_files/](week6_session_b_lab4_files/)

</details>

<details>
<summary><strong>🚀 Weeks 7–8 — Capstone & demo</strong></summary>
<br>

<p align="center">
  <img src="week7_session_a_github_page_a.png" alt="Week 7 Session A — GitHub project page" width="32%" />
  <img src="week7_session_b_Streamlit_page.png" alt="Week 7 Session B — Capstone Streamlit" width="32%" />
  <img src="week8_session_b_github2.png" alt="Week 8 Session B — final GitHub showcase" width="32%" />
</p>

| Session | Topic | Open report |
|---------|-------|-------------|
| 7A | Capstone project planning | [📄 PDF](Week7_SessionA_Report.pdf) · [📝 TeX](Week7_SessionA_Report.tex) |
| 7B | Capstone core development | [📄 PDF](Week7_SessionB_Report.pdf) · [📝 TeX](Week7_SessionB_Report.tex) |
| 8A | Testing & validation | [📄 PDF](Week8_SessionA_Report.pdf) · [📝 TeX](Week8_SessionA_Report.tex) |
| 8B | Final demo & defense preparation | [📄 PDF](Week8_SessionB_Report.pdf) · [📝 TeX](Week8_SessionB_Report.tex) |

📁 Artifacts: [week7_session_a_files/](week7_session_a_files/) · [week7_session_b_files/](week7_session_b_files/) · [week8_session_a_files/](week8_session_a_files/) · [week8_session_b_files/](week8_session_b_files/)

</details>

---

## 📋 Report index

| Wk | Ses | Topic | PDF | LaTeX |
|:--:|:---:|:------|:---:|:-----:|
| 1 | A | Environment setup & first AI script | [📄](Week1_SessionA_Report.pdf) | [📝](Week1_SessionA_Report.tex) |
| 1 | B | AI mental models (Chain-of-Thought) | [📄](Week1_SessionB_Report.pdf) | [📝](Week1_SessionB_Report.tex) |
| 2 | A | Chain-of-Thought prompting | [📄](Week2_SessionA_Report.pdf) | [📝](Week2_SessionA_Report.tex) |
| 2 | B | Context engineering (AGENTS.md) | [📄](Week2_SessionB_Report.pdf) | [📝](Week2_SessionB_Report.tex) |
| 3 | A | Agile scaffolding practice | [📄](Week3_SessionA_Report.pdf) | [📝](Week3_SessionA_Report.tex) |
| 3 | B | Test-driven development | [📄](Week3_SessionB_Report.pdf) | [📝](Week3_SessionB_Report.tex) |
| 4 | A | Refactoring & migration | [📄](Week4_SessionA_Report.pdf) | [📝](Week4_SessionA_Report.tex) |
| 4 | B | Integration & flow practice | [📄](Week4_SessionB_Report.pdf) | [📝](Week4_SessionB_Report.tex) |
| 5 | A | **Lab 1** — Rainfall alert | [📄](Week5_SessionA_Lab1_Report.pdf) | [📝](Week5_SessionA_Lab1_Report.tex) |
| 5 | B | **Lab 2** — SCS-CN runoff | [📄](Week5_SessionB_Lab2_Report.pdf) | [📝](Week5_SessionB_Lab2_Report.tex) |
| 6 | A | **Lab 3** — Reservoir optimization | [📄](Week6_SessionA_Lab3_Report.pdf) | [📝](Week6_SessionA_Lab3_Report.tex) |
| 6 | B | **Lab 4** — Flood inundation | [📄](Week6_SessionB_Lab4_Report.pdf) | [📝](Week6_SessionB_Lab4_Report.tex) |
| 7 | A | Capstone project planning | [📄](Week7_SessionA_Report.pdf) | [📝](Week7_SessionA_Report.tex) |
| 7 | B | Capstone core development | [📄](Week7_SessionB_Report.pdf) | [📝](Week7_SessionB_Report.tex) |
| 8 | A | Testing & validation | [📄](Week8_SessionA_Report.pdf) | [📝](Week8_SessionA_Report.tex) |
| 8 | B | Final demo & defense preparation | [📄](Week8_SessionB_Report.pdf) | [📝](Week8_SessionB_Report.tex) |

---

## 📁 Appendix code folders

| Folder | Lab | Contents |
|--------|-----|----------|
| [week3_session_a_files/](week3_session_a_files/) | Week 3A | `src/`, `tests/`, prompt logs |
| [week3_session_b_files/](week3_session_b_files/) | Week 3B | TDD green/red/refactor prompts |
| [week4_session_a_files/](week4_session_a_files/) | Week 4A | Legacy vs modern hydrology |
| [week4_session_b_files/](week4_session_b_files/) | Week 4B | Alert system integration |
| [week5_session_a_lab1_files/](week5_session_a_lab1_files/) | Week 5 Lab 1 | Rainfall lab data & code |
| [week5_session_b_lab2_files/](week5_session_b_lab2_files/) | Week 5 Lab 2 | Runoff figures & sensitivity |
| [week6_session_a_lab3_files/](week6_session_a_lab3_files/) | Week 6 Lab 3 | Trade-off plots |
| [week6_session_b_lab4_files/](week6_session_b_lab4_files/) | Week 6 Lab 4 | DEM & flood comparison figures |
| [week7_session_a_files/](week7_session_a_files/) | Week 7A | Capstone planning docs |
| [week7_session_b_files/](week7_session_b_files/) | Week 7B | Development artifacts |
| [week8_session_a_files/](week8_session_a_files/) | Week 8A | Test & validation logs |
| [week8_session_b_files/](week8_session_b_files/) | Week 8B | Demo & GitHub screenshots |

Runnable capstone code: [`../app/`](../app/) · [`../src/`](../src/) · [`../tests/`](../tests/)

---

## 🔗 Path to specialized experiments

```
Week 5 Lab 1  ──►  🌧️ Experiment 1 (Rainfall alert)
Week 5 Lab 2  ──►  💧 Experiment 2 (SCS-CN runoff)
Week 6 Lab 3  ──►  ⚖️ Experiment 3 (Reservoir optimization)
Week 6 Lab 4  ──►  🌊 Experiment 4 (Flood inundation)
Week 7–8      ──►  🚀 Capstone dashboard (app/, src/, tests/)
```

Formal experiment PDFs: **[submission/](../submission/)** · Case study: **[submission/portfolio/](../submission/portfolio/)**

---

## 🔄 Regenerate PDFs

From this folder (`lab_reports/`):

```bash
pdflatex Week5_SessionA_Lab1_Report.tex && pdflatex Week5_SessionA_Lab1_Report.tex
# repeat for each Week*_Report.tex; run twice for references
```

Some reports need PNG screenshots in the same folder — see comments at the top of each `.tex` file.

---

## 🔗 Related

| Resource | Link |
|----------|------|
| 🏠 Main repository | [README](../README.md) |
| 📦 Specialized experiments (PDF + LaTeX) | [submission/](../submission/) |
| 📊 AI engineering case study | [submission/portfolio/](../submission/portfolio/) |
| 🧪 Capstone tests (88) | [tests/](../tests/) |

---

<div align="center">

**16 labs · 8 weeks · 1 integrated smart water pipeline**

[⬆ Back to top](#-weekly-lab-reports--smart-water-lab) · [🏠 Main repo](../README.md)

</div>
