# Amai — Data Cleaner Web App

> A fast, browser-based data cleaning and visualization workspace powered by Streamlit, Pandas, and AI.

[![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📸 Screenshots

### Data Table & Sidebar Controls
![Data table view with sidebar](https://github.com/user-attachments/assets/26d1405b-f586-499f-a783-bc70f85bfe22)

### Summarized Data — Correlation Matrix
![Correlation heatmap](https://github.com/user-attachments/assets/67b42f4e-2cd0-4857-97a1-e4cdee719c98)

### Interactive Data Plotting
![Scatter plot of HP vs Attack](https://github.com/user-attachments/assets/f557bf48-307c-45f1-8ee4-16a039558f76)

### Amai AI Chat
![AI chat panel](https://github.com/user-attachments/assets/31d02911-fdda-43a6-97e3-f121c0247057)

---

## ✨ Features

### 📂 File Upload
- Upload **CSV** or **Excel (.xlsx)** files up to 200 MB.
- Optional **password-protected Excel** file support via `msoffcrypto`.

### 🔍 Pick Values To Show
- Show the **first N rows** of your dataset using a slider.
- Show a **custom row range** (e.g. rows 100–500) using a range slider.

### 🏗️ Column Modification
| Sub-feature | What it does |
|---|---|
| **Rename Column** | Pick any column and give it a new name |
| **Make New Column With Function** | Create a derived column by applying `×`, `+`, `−`, or `÷` between two existing columns |
| **Drop Columns** | Select one or more columns to permanently remove |
| **Add or Remove Suffix/Prefix** | Batch-add or batch-strip a prefix and/or suffix on any set of columns |

### 🔧 Values Modification
| Sub-feature | What it does |
|---|---|
| **Replace Empty Values** | Fill `NaN` / blank cells in selected columns with a custom value |
| **Remove Rows/Columns with Missing Values** | Drop all rows **or** all columns that contain at least one `NaN` |
| **Replace String in Column** | Find-and-replace any text (case-sensitive) across one or more columns |

### 🔀 Sorting
- Sort the entire dataset **ascending** or **descending** by any column.

### 🎲 Shuffle Data
- Randomly shuffle all rows (useful for anonymization or ML dataset preparation).

### ⚙️ Extras
| Sub-feature | What it does |
|---|---|
| **Filter** | Keep only rows where a column satisfies `>`, `<`, `=`, or `≠` a given value (works for both numbers and text) |
| **Format Columns** | Apply **Capitalize**, **Phone Format** (`xxx-xxx-xxxx`), or **Remove Extra Spaces** to selected columns |
| **Drop Duplicate Rows** | Remove all exact duplicate rows in one click |

### 📊 Plot Your Data
Choose from **8 chart types**, all rendered with Plotly:

| Chart | Dimensions |
|---|---|
| Line Plot | 2D |
| Scatter Plot | 2D |
| Bar Chart | 2D |
| Horizontal Bar Chart | 2D |
| Stacked Area Plot | 2D |
| Histogram | 1D |
| Box Plot | 1D |
| Map Plot | Latitude / Longitude |

- Select any column as the **color/label** axis for categorical grouping.
- For map plots, pick dedicated **latitude** and **longitude** columns.

### 📋 Summarized Data
Switch between two views:
- **Summary** — pandas `describe()` table covering count, mean, std, min, quartiles, and max for every column.
- **Correlation** — interactive grayscale **heatmap** of numeric column correlations (Pearson), built with Plotly.

### 🤖 Chat with Amai AI *(Beta)*
An AI assistant that reads the first 20 rows and a full statistical summary of your dataset and answers natural-language questions about it.

**Available models:**

| Model | Provider | Best for |
|---|---|---|
| `openai/gpt-oss-120b` | Groq | Deep logic & analysis (recommended) |
| `qwen/qwen3-32b` | Groq | Balanced speed + reasoning |
| `moonshotai/kimi-k2-instruct` | Groq | Following complex instructions |
| `gpt-oss:20b-cloud` | Ollama | Fast, precise responses |

- Adjustable **creativity slider** (0.1 = most factual → 0.9 = most creative).
- On first load, Amai automatically generates a **high-level executive summary** of your data.
- Full **chat history** is preserved during the session.

### 💾 Session Controls

| Button | Action |
|---|---|
| **Commit** | Save the current state as a checkpoint |
| **Undo To Last Commit** | Roll back all changes since the last commit |
| **Reset All** | Restore the original uploaded file |
| **Download Cleaned Data as CSV** | Export the current state as a named `.csv` file |
| **Clear Cache** | Free Streamlit's cache (recommended before closing the tab) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- A [Groq API key](https://console.groq.com) (for the AI chat feature)
- An Ollama Cloud token (optional, for Ollama models)

### Installation

```bash
git clone https://github.com/hqwn/Data-Cleaner--Web.git
cd Data-Cleaner--Web
pip install -r requirements.txt
```

### Configure Secrets

Create a `.streamlit/secrets.toml` file with your API keys:

```toml
Groq = "your-groq-api-key"
OLLAMA_KEY = "your-ollama-api-key"   # optional
```

### Run the App

```bash
streamlit run main.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI framework |
| [Pandas](https://pandas.pydata.org) | Data manipulation |
| [Plotly Express](https://plotly.com/python/plotly-express/) | Interactive charts |
| [NumPy](https://numpy.org) | Numerical operations |
| [msoffcrypto-tool](https://github.com/nolze/msoffcrypto-tool) | Password-protected Excel support |
| [Groq](https://groq.com) | LLM inference (cloud) |
| [Ollama](https://ollama.com) | LLM inference (self-hosted / cloud) |
| [openpyxl](https://openpyxl.readthedocs.io) | Excel file reading/writing |
| [tabulate](https://pypi.org/project/tabulate/) | Markdown table formatting for AI context |

---

## 📖 Learn More

Watch the tutorial on YouTube: [**Learn How To Use Amai**](https://youtu.be/ZZrf9-v7QsA)

---

## 🐛 Reporting Issues

Found a bug? [Open an issue on GitHub](https://github.com/hqwn/Data-Cleaner--Web/issues).
