# TD 1 comparison matrix

Final verdict per cell. See [comparison CSV](../kit-td1/model-question-comparison-en.csv) for values and causes.

C = correct; I = incorrect; R = SQL rejected. Dots C07/C08 are additions from 30 October.

| Model | C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | C15 | C16 | C17 | C18 | C19 | C20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| groq:openai/gpt-oss-120b | C | C | C | C | C | C | C | C | C | C | C | C | C | C | C | C | C | C | I | C |
| groq:openai/gpt-oss-20b | C | I | C | C | C | C | C | C | C | C | I | C | C | C | C | C | C | C | C | C |
| openrouter:cohere/north-mini-code:free | C | I | C | C | C | C | C | I | I | I | I | C | C | C | C | C | I | C | I | C |
| groq:qwen/qwen3.8-27b | C | C | R | C | C | C | C | C | I | R | C | C | C | C | I | I | I | C | I | C |
| openrouter:dots-studio/dots-3-note-preview:free | C | I | C | C | C | C | C | C | I | I | C | C | C | C | C | I | C | I | C | C |
