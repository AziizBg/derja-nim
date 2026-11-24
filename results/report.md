# Tunisian Derja on NVIDIA NIM

Calls were made on 24 November 2026 against `https://integrate.api.nvidia.com/v1/chat/completions`. Thinking was turned off so the token budget went to the answer. Temperature was 0.3. Each steered prompt used the same system prompt: reply as someone from Tunis, in street Derja, in Arabic script, and do not drift into Egyptian, Levantine, Moroccan, or Algerian.

`meta/llama-3.3-70b-instruct` is the open model TounsiBench measured. This key gets HTTP 410 for it. NVIDIA retired that id on 26 August 2026, along with Llama 3.1 70B. It could not be scored.

## Ranking

Score is 0, 1, or 2 per prompt. A 2 is recognisable Tunisian and the task is done. A 1 is mixed dialect or a partial answer. A 0 is the wrong dialect, the wrong meaning, or a broken reply. Eight prompts, so 16 is the ceiling.

| Model | Greet | Apology | Ramadan | Tunizi | Phrases | Tram | French | Story | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `moonshotai/kimi-k3.1-pro` | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | **15** |
| `meta/muse-glimmer-30b` | 1 | 2 | 1 | 2 | 0 | 1 | 1 | 2 | **10** |
| `nvidia/nemotron-3.5-bolt-e4b` | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 1 | **10** |
| `nvidia/nemotron-3-ultra-550b-a55b` | 2 | 1 | 1 | 1 | 0 | 1 | 1 | 2 | **9** |
| `nvidia/nemotron-3.5-super-vl-120b-a12b` | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | **6** |
| `nvidia/ising-calibration-1.5-31b` | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | **5** |
| `mistralai/mistral-large-4-1t-a52b` | — | 1 | — | 1 | — | — | 2 | 0 | 4 of the 4 that returned |
| `nvidia/nemotron-3.5-lightning-30b-a3b` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

Use **Kimi K3.1 Pro** if the product has to speak Derja. It was slow (about 30–100 seconds a call) and it finished every prompt.

Use **Muse Glimmer 30B** if you want a long reply that sounds like Tunis and you can tolerate set-phrase mistakes. Use **Nemotron 3 Ultra** if you want to stay on an NVIDIA model: the greeting and the Tunis story are real Derja, then it slips into Algerian on idioms. **Bolt** is the only small model that is sometimes actually Tunisian, and it answers in under 3 seconds. It still says `مزيان` and `حريرة`.

Do not use Lightning or Nano Omni for this. Lightning answers in Egyptian. Nano Omni loops or mixes Egyptian and Moroccan. Ising-Calibration is a qubit-calibration model that happens to accept chat; it is not a dialect model.

## The tell

“I miss you” in Tunisia is `توحشتك`. “I love you” is `نحبك`. Most models swapped them.

| Model | What it said for “I miss you” |
| --- | --- |
| Gemma 4 31B (partial pass) | `توحشتك، نتلقاو مبعد، وما ثمة حتى مشكل` |
| Kimi K3.1 Pro | `توحشتك` |
| Ising-Calibration | `نتوحشّك` |
| Bolt | `نحبك` |
| Nemotron 3 Ultra | `نحس بيك` / `نفتقدك` |
| Super VL | `نحبك بزاف` |
| Muse Glimmer | `نفتقدك` / `تاقتني` |
| Nano Omni | `نحبك قوي` |
| Lightning | `بغيتك`, then said it does not speak Derja |

Kimi’s miss on this prompt is the other half: “see you later” came out as `نراك بعدين` / `نتشاوفو بعدين`. `نتشاوفو` is Algerian. Tunisians say `نشوفك من بعد`. “No problem” was right: `ما فماش مشكل`.

Gemma 4 31B, on a slower second pass, got all three phrases in one line: `توحشتك` (I miss you), `نتلقاو مبعد` (see you later; `مبعد` is the Tunisian “later”), and `ما ثمة حتى مشكل` (no problem at all). That is the most idiomatic phrase triple in the run. The same model then timed out on Tunizi and on the French line, and the greeting invented a word, `مريغل`, next to real `لاباس` and `شنوة`. It also took 150–200 seconds a call, so it is not a usable chat endpoint here even when the dialect is right.

“Because” is the other tell. The French sentence was “I’m sorry I’m late because of the traffic on the road to La Marsa.”

- Kimi: `سامحني، تأخرت خاطر الزحمة في طريق المرسى.`
- Bolt: `سامحني تأخرت خاطر الزحمة في طريق المرسى`
- Mistral, when it finished: `سامحني، تأخرت على خاطر الزحمة في طريق المرسى`
- Ultra and Super VL used `بسبب`, which is فصحى.

## What the winner actually said

Greeting. `لاباس، الحمد لله. إنتي شنوّة أخبارك؟ كل شي مليح؟`

Apology. `سامح خويا، سامحني برشا على التأخير، عارف روحي خليتك تستنى نص ساعة قدام الكافيتيريا. ما تزعلش مني، جايك توّا في أقرب وقت.`

Ramadan, named properly. Chorba frik with fish or chicken, brik with tuna or `عصبان`, `سلطة مشوية`, and `لبلابي` with harissa, cumin, an egg, and tuna. It also mentioned pine-nut tea.

Tunizi. The input was `ya hasra, el match tawa w ana mazelt fel service, bercha 5edma. 9olli nji wala le?` Kimi read `5` as خ and `9` as ق: the match is now, he is still at work, there is a lot of work, should he come or not. The suggested reply stayed in Derja (`على خاطر ماتش`, `ما تخسرش رزقك`).

Tram note. `el tramway wa9ef w ena mazelt fi cité el khadra, tw nwaslek` — the tram is stopped, he is still in Cité El Khadra, and he will still get to you, by taxi or by `كرهبة`. Muse and Ultra understood the place and the stopped tram, then missed `tw nwaslek` and said he could not come.

Unsteered story, no system prompt. Kimi kept `توّه`, `يلقى`, `ماكش باش تمشي`, `كهرباء مقطوعة`, `يلّا`, `على رجلينا`. Muse was as good or better on this one prompt: Berges du Lac, the Bardo tram, Hay Et-Tadhamon, `اللوطو`, `شنوة نعمل`. Ultra set the scene at the Ministry of Commerce, line 4 toward El Menzah, and the newspaper *Essarih*, then the reply hit the 500-token cap. Super VL put the same scene in a Paris office and used `بغى`.

## Where the others leak

Muse’s apology is street Derja (`سامح خويا سامحني برشا… تو نجيك توا`). Its phrase list is not: `نفتقدك`, `تاقتني`, `ماكش مشكلة`. Ramadan included `بغرير`, which is Moroccan, next to real Tunisian items (`شربة فريك`, `ملوخية`).

Ultra’s greeting is the cleanest NVIDIA reply: `الحمد لله لاباس، نخدم ونسعى. إنت كيفاش؟ شنويا جابك لهنا؟` The Tunizi answer then left Tunisia: `شغل بزاف`, `إذا تبيّه`, `راني ناضرك`, `تعشى و تعا`. The apology used `طاح فيا` and `جاي على طول`.

Bolt is uneven in a single breath. `الحمد لله لاباس، كل شي مزيان` pairs the Tunisian greeting with the Moroccan word for “fine”. Ramadan ends on `شوربة حريرة`. The French line and the tram line are right and short.

Lightning, with the same system prompt: `الحال كويس`, `دلوقتي`, `بص`, `لسه`, and `بزاف`. For the phrases it refused and offered Moroccan `بغيتك`. Ramadan was `بريك`, `مخلوق`, `بريكة`, `بسكويت`.

Nano Omni repeated `الحمد لله` until the token limit on the greeting. The phrases were `نحبك قوي` and `بصك لاحر`. It turned La Marsa into `لمارص` and read the apology as the friend wanting to apologise (`باغي`).

Mistral Large 4 rejected `reasoning_effort` and kept a long reasoning trace (often 500–1,400 tokens) before a short answer, so four of eight prompts timed out at 180 seconds. The answers that arrived know `على خاطر` and `شد روحك وجي`. The unsteered story mixed in Chinese `停` and the English word “Heat”. It is not a practical Derja endpoint on this API until thinking can be turned off.

Ising-Calibration introduced itself as a superconducting-qubit model, in فصحى, when asked how it was. The unsteered story was the sentence `أنا هنا! أنا التراموي!` repeated until the limit.

## Models that did not finish a full pass

These ids are on the key’s model list. A first pass with a 100-second cap did not return. A second pass with a 200-second cap got partial text only.

| Model | What came back |
| --- | --- |
| `minimaxai/minimax-m3.1-flash` | Did not know `لاباس` (“what do you mean?” in فصحى). Greeting timed out. Tunizi decode was right, then the suggested reply used Moroccan `ديالك`. “I miss you” was `نشتاقلك` (Levantine). The French line used `بسبب الازدحام`. |
| `stepfun-ai/step-5-preview` | Probe started with `لاباس` and then `كيف يمكنني مساعدتك؟`. Greeting mixed `نحب` / `كيفاش` / `شنويا` with `بخير`. Tunizi, the set phrases, and the French line returned no visible text. |
| `google/gemma-4-31b-it` | Second pass, about 150–200 seconds a call. Greeting: `لاباس الحمد لله… إنت شنوة أحوالك؟ كل شيء مريغل؟` (`مريغل` is not a word). Phrases: `توحشتك، نتلقاو مبعد، وما ثمة حتى مشكل` — the best idiom line in the test. Tunizi and the French line timed out. |
| `z-ai/glm-5.3-flash` | No completion within 200 seconds on the first pass. |

`google/gemma-3-12b-it` and `google/gemma-3-4b-it` are listed by `/v1/models` and return 404 for this account. `nvidia/riva-translate-4b-instruct-v2` translated the instruction into English (“Answer in Tunisian Dinar”) instead of answering. The partial second pass is in [nim-tunisian-retries.json](nim-tunisian-retries.json).

## How to read this against the papers

TounsiBench’s best open model on NVIDIA was Llama 3.3 70B, and that deployment is gone. Nothing in this run is a substitute score for that paper. It is a check of what this key can call today, on prompts that punish فصحى, Egyptian, and Moroccan.

The pattern in the papers still holds. The models understand more Derja than they produce. Kimi is the exception in this catalog: with a short system prompt and thinking off, it produced `برشا`, `توا`, `خاطر`, `لاباس`, `توحشتك`, and the Ramadan dishes without being handed those words in the prompt.
