# derja-nim

**NVIDIA NIM chat models understand Tunisian Derja better than they speak it. One of them speaks it.**

On 24 November 2026 the same eight prompts went to every general chat model an NVIDIA API key could call. Thinking was off, so the token budget went to the answer. Temperature was 0.3. Each reply was read by hand and scored 0, 1, or 2.

**Call `moonshotai/kimi-k3.1-pro`.** It scored 15/16 and finished every prompt. It says `توحشتك`, `برشا`, `خاطر`, and `لاباس`, and it names a Tunisian ftour (شربة فريك، بريك، سلطة مشوية، لبلابي) without those words being handed to it.

`meta/llama-3.3-70b-instruct` is the open model [TounsiBench](https://aclanthology.org/2025.emnlp-main.1756/) measured. This API returns HTTP 410 for it. NVIDIA retired that id on 26 August 2026.

The lab note is [results/report.md](results/report.md). The sheet is [results/scores.csv](results/scores.csv). The raw replies are the JSON files next to them.

## Scores

A 2 is recognisable Tunisian and the task is done. A 1 is mixed dialect or a partial answer. A 0 is the wrong dialect, the wrong meaning, or a broken reply. Eight prompts, so 16 is the ceiling.

| Model | Total | What to do with it |
| --- | ---: | --- |
| `moonshotai/kimi-k3.1-pro` | **15** | Use this when the product has to speak Derja. About 30–100 seconds a call. |
| `meta/muse-glimmer-30b` | 10 | Best long story (Berges du Lac, the Bardo tram, Hay Et-Tadhamon). Set phrases slip. |
| `nvidia/nemotron-3.5-bolt-e4b` | 10 | Under 3 seconds, often actually Tunisian, with Moroccan leaks (`مزيان`, `حريرة`). |
| `nvidia/nemotron-3-ultra-550b-a55b` | 9 | Best NVIDIA-built model. Greeting and the Tunis story are Derja, then Algerian idioms (`بزاف`, `راني`, `تبي`). |
| `nvidia/nemotron-3.5-super-vl-120b-a12b` | 6 | Understood the tram note. Set the Tunis story in a Paris office. |
| `nvidia/nemotron-3.5-lightning-30b-a3b` | 0 | Egyptian (`كويس`, `دلوقتي`, `بص`). |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | 0 | Looped `الحمد لله`, then Egyptian. |

`mistralai/mistral-large-4-1t-a52b` knows `على خاطر` and then spends hundreds of reasoning tokens before a short line. Four of eight prompts timed out at 180 seconds. `google/gemma-4-31b-it` produced the best single idiom line in the run, `توحشتك، نتلقاو مبعد، وما ثمة حتى مشكل`, then timed out twice and invented the word `مريغل`. Calls took 150–200 seconds.

## What this is not

- Not a substitute for TounsiBench, and not a substitute for the Tunizi study. Those have more items and a defined metric. This is one afternoon on the models a public NIM key can still call.
- Not a leaderboard. One temperature, one run, thinking disabled. A second sample would move a 1.
- Not an automatic score. A reply can contain a Tunisian word and still be Egyptian. The number is a reading of the text.

## The tell

“I miss you” in Tunisia is `توحشتك`. `نحبك` is “I love you”. Most models swapped them.

“Because” is the other one. “I’m late because of the traffic on the road to La Marsa” should come out with `خاطر`, not فصحى `بسبب`.

Kimi:

> سامحني، تأخرت خاطر الزحمة في طريق المرسى.

## Prompts

Seven prompts used this system prompt, and did not list the marker words:

> إنت صاحب تونسي من تونس العاصمة. جاوب كان بالدارجة التونسية اللي يحكوها الناس في الشارع، بالحروف العربية. ممنوع الفصحى. ممنوع اللهجة المصرية والشامية والمغربية والجزائرية. جاوب باختصار، بجمل طبيعية، من غير مقدمة ومن غير ترجمة ومن غير شرح للتعليمات.

The eighth prompt had no system prompt: a short story set in Tunis, about someone leaving work to find the tram stopped.

The set covers a greeting, an apology text, four Ramadan foods named the way people in Tunisia say them, a Latin Tunizi message (`5` is خ, `9` is ق), the three set phrases above, a French/Tunizi voice note from Cité El Khadra, and the La Marsa sentence.

## Run

Python 3, standard library only. The key is read from the environment and is not written to disk.

```sh
export NVIDIA_API_KEY=...
python3 scripts/tunisian_nim_eval.py
```

That rewrites `results/nim-tunisian-raw.json`. It does not rescore. Scoring stays manual.

## References

- TounsiBench: Benchmarking Large Language Models for Tunisian Arabic. EMNLP 2025. <https://aclanthology.org/2025.emnlp-main.1756/>
- How Well Do LLMs Understand Tunisian Arabic? arXiv:2511.16683. <https://arxiv.org/abs/2511.16683>

## License

MIT. Copyright 2026 Ben Ghorbel Mohamed Aziz.
