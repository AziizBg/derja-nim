# Tunisian Derja on NVIDIA NIM

A small prompt suite for checking whether a hosted chat model actually speaks Tunisian Arabic (Derja), including Latin-script Tunizi, instead of drifting into Modern Standard Arabic or another dialect.

The scored run from 24 November 2026 is in [results/report.md](results/report.md). The sheet to attach is [results/scores.csv](results/scores.csv). Raw replies are in [results/nim-tunisian-raw.json](results/nim-tunisian-raw.json).

## What to send

Send `results/report.md` for the write-up and `results/scores.csv` for the table. The JSON files are the evidence behind those scores. The API key is not in this repo. Do not paste it into the thread with the team.

## What was asked

Eight prompts, temperature 0.3, thinking switched off (`chat_template_kwargs.enable_thinking: false` and `reasoning_effort: none` when the endpoint accepts it):

- A greeting (`كيفاش الحال؟`)
- A short apology text
- Four everyday Ramadan foods, named the way people in Tunisia say them
- A Latin Tunizi message (`5` = خ, `9` = ق) to decode and answer
- Three set phrases: “I miss you”, “see you later”, “no problem”
- A French/Tunizi voice note about a stopped tram in Cité El Khadra
- A French sentence to say in Derja (`à cause de` should come out as `خاطر`, not `بسبب`)
- An unsteered story set in Tunis, with no dialect system prompt

Steered prompts use a short system prompt: answer as someone from Tunis, in street Derja, Arabic script, and do not slip into Egyptian, Levantine, Moroccan, or Algerian.

## Run it again

The API key is read from the environment. It is not stored in this repo.

```bash
export NVIDIA_API_KEY=nvapi-...
python3 scripts/tunisian_nim_eval.py
```

That rewrites `results/nim-tunisian-raw.json`. Scoring in the report is manual: a reply can contain the letters of a Tunisian word and still be the wrong dialect.

## Models that are gone

`meta/llama-3.3-70b-instruct` is the open model TounsiBench measured. On this API it returns HTTP 410. NVIDIA retired it on 26 August 2026. The same is true of Llama 3.1 70B and the older Qwen and DeepSeek ids that used to appear in the catalog.
