#!/usr/bin/env python3
"""Send the Derja / Tunizi prompt set to NVIDIA NIM chat models.

Reads NVIDIA_API_KEY from the environment. The key is never written to disk.
Scores in results/scores.csv are manual. This script only stores replies.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "results" / "nim-tunisian-raw.json"

SYSTEM = (
    "إنت صاحب تونسي من تونس العاصمة. "
    "جاوب كان بالدارجة التونسية اللي يحكوها الناس في الشارع، بالحروف العربية. "
    "ممنوع الفصحى. ممنوع اللهجة المصرية والشامية والمغربية والجزائرية. "
    "جاوب باختصار، بجمل طبيعية، من غير مقدمة ومن غير ترجمة ومن غير شرح للتعليمات."
)

PROMPTS = [
    {
        "id": "greeting",
        "steered": True,
        "task": "Casual greeting. A natural reply uses لاباس and asks back, not فصحى بخير only.",
        "user": "كيفاش الحال؟ شنويا أخبارك توا؟",
    },
    {
        "id": "apology",
        "steered": True,
        "task": "Write a short apology text to a friend who has been waiting.",
        "user": (
            "اكتب مسج قصير لصاحبي سامح باش نعتذرلو على التأخير. "
            "هو يستنى فيا قدام الكافيتيريا من نص ساعة."
        ),
    },
    {
        "id": "ramadan",
        "steered": True,
        "task": "Name everyday Tunisian Ramadan foods the way Tunisians say them.",
        "user": "شنويا ناكلو عادة في الماكرو في رمضان في تونس؟ عطيني أربعة حاجات كيف ما يقولوها التوانسة.",
    },
    {
        "id": "tunizi",
        "steered": True,
        "task": "Decode Latin Tunizi (3/5/7/9) and answer in Arabic-script Derja.",
        "user": (
            "صاحبي كتبلي بالتونزي: "
            "'ya hasra, el match tawa w ana mazelt fel service, bercha 5edma. 9olli nji wala le?'. "
            "شنويا قال، و كيفاش نجاوبو؟ جاوب بالدارجة بالحروف العربية."
        ),
    },
    {
        "id": "phrases",
        "steered": True,
        "task": "Everyday phrases: I miss you, see you later, no problem. Expect توحشتك / نشوفك من بعد / ما فيها باس.",
        "user": (
            "كيفاش نقول بالدارجة: I miss you، see you later، و no problem؟ "
            "عطيني الجمل كيف ما يقولوها في تونس، مش الترجمة الفصحى."
        ),
    },
    {
        "id": "situation",
        "steered": True,
        "task": "Explain a French/Tunizi code-switched voice note.",
        "user": (
            "نفسرلي الموقف هاذا بالدارجة: صاحبي قال "
            "'wallah c'est chaud, el tramway wa9ef w ena mazelt fi cité el khadra, tw nwaslek'. "
            "شنويا صار و شنويا بش يعمل؟"
        ),
    },
    {
        "id": "french",
        "steered": True,
        "task": "Render a French sentence as spoken Derja, not a literal MSA translation.",
        "user": (
            "قولها بالدارجة مش بالفرنسية ومش بالفصحى: "
            "Je suis désolé, je suis en retard à cause des embouteillages sur la route de la Marsa."
        ),
    },
    {
        "id": "unsteered",
        "steered": False,
        "task": "No dialect system prompt. Shows whether the model drifts to MSA on its own.",
        "user": "احكيلي موقف قصير صار في تونس العاصمة، بالدارجة، على واحد توّه خارج من الخدمة و لقى التراموي واقف.",
    },
]

MODELS = [
    "nvidia/nemotron-3-ultra-550b-a55b",
    "nvidia/nemotron-3.5-super-vl-120b-a12b",
    "nvidia/nemotron-3.5-lightning-30b-a3b",
    "nvidia/nemotron-3.5-bolt-e4b",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
    "moonshotai/kimi-k3.1-pro",
    "meta/muse-glimmer-30b",
    "minimaxai/minimax-m3.1-flash",
    "stepfun-ai/step-5-preview",
    "mistralai/mistral-large-4-1t-a52b",
    "google/gemma-4-31b-it",
    "z-ai/glm-5.3-flash",
    "nvidia/ising-calibration-1.5-31b",
]


def post(body: dict, timeout: int = 120) -> dict:
    key = os.environ["NVIDIA_API_KEY"]
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def call(model: str, messages: list[dict], extra: dict | None = None, timeout: int = 120) -> dict:
    body = {
        "model": model,
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.3,
        "stream": False,
    }
    if extra:
        body.update(extra)
    started = time.time()
    try:
        data = post(body, timeout=timeout)
    except urllib.error.HTTPError as e:
        err = e.read().decode()[:500]
        return {
            "ok": False,
            "status": e.code,
            "error": err,
            "latency_s": round(time.time() - started, 2),
        }
    except Exception as e:  # noqa: BLE001
        return {
            "ok": False,
            "status": None,
            "error": f"{type(e).__name__}: {e}",
            "latency_s": round(time.time() - started, 2),
        }
    choice = data["choices"][0]
    message = choice.get("message") or {}
    usage = data.get("usage") or {}
    details = usage.get("completion_tokens_details") or {}
    content = message.get("content") or ""
    reasoning = message.get("reasoning_content") or message.get("reasoning") or ""
    return {
        "ok": True,
        "status": 200,
        "finish_reason": choice.get("finish_reason"),
        "content": content,
        "reasoning_excerpt": (reasoning or "")[:400],
        "reasoning_tokens": details.get("reasoning_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "latency_s": round(time.time() - started, 2),
    }


def payload_for(model: str) -> dict:
    """Thinking-off payload. Mistral's endpoint rejects reasoning_effort."""
    if model.startswith("mistralai/"):
        return {"chat_template_kwargs": {"enable_thinking": False}, "max_tokens": 700}
    return {
        "chat_template_kwargs": {"enable_thinking": False},
        "reasoning_effort": "none",
    }


def probe_model(model: str) -> tuple[str, dict | None, dict]:
    extra = payload_for(model)
    probe = call(
        model,
        [{"role": "user", "content": "قول كلمة: لاباس"}],
        extra,
        timeout=100,
    )
    if not probe["ok"] and probe.get("status") == 400 and "reasoning_effort" in (probe.get("error") or ""):
        extra = {"chat_template_kwargs": {"enable_thinking": False}}
        probe = call(model, [{"role": "user", "content": "قول كلمة: لاباس"}], extra, timeout=100)
    if probe["ok"] and not (probe.get("content") or "").strip():
        extra = {"max_tokens": 1400}
        probe = call(model, [{"role": "user", "content": "قول كلمة: لاباس"}], extra, timeout=150)
    if probe["ok"] and (probe.get("content") or "").strip():
        return model, extra, probe
    return model, None, probe


def run_one(model: str, extra: dict, prompt: dict) -> dict:
    messages = []
    if prompt["steered"]:
        messages.append({"role": "system", "content": SYSTEM})
    messages.append({"role": "user", "content": prompt["user"]})
    # Keep the call budget modest. Reasoning models that ignore the switch
    # still need room for a short visible answer.
    call_extra = dict(extra)
    call_extra.setdefault("max_tokens", 500)
    result = call(model, messages, call_extra, timeout=180)
    if result["ok"] and not (result.get("content") or "").strip():
        # Reasoning ate the budget. One retry with a larger cap.
        retry_extra = dict(call_extra)
        retry_extra["max_tokens"] = 1600
        result = call(model, messages, retry_extra, timeout=180)
        result["retried_empty"] = True
    result["model"] = model
    result["prompt_id"] = prompt["id"]
    result["steered"] = prompt["steered"]
    return result


def main() -> int:
    if not os.environ.get("NVIDIA_API_KEY"):
        print("NVIDIA_API_KEY is not set", file=sys.stderr)
        return 1
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    print("preflight", flush=True)
    extras: dict[str, dict] = {}
    alive: list[str] = []
    skipped: list[dict] = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        probes = list(pool.map(probe_model, MODELS))
    for model, extra, probe in probes:
        if extra is not None:
            extras[model] = extra
            alive.append(model)
            print(f"  live {model} extra={list(extra)} content={probe['content'][:60]!r}", flush=True)
        else:
            skipped.append({"model": model, "probe": probe})
            print(f"  skip {model} {probe.get('status')} {(probe.get('error') or probe.get('content') or '')[:160]}", flush=True)
    alive = [m for m in MODELS if m in extras]

    jobs = [(model, prompt) for model in alive for prompt in PROMPTS]
    rows: list[dict] = []
    print(f"running {len(jobs)} calls", flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(run_one, model, extras[model], prompt) for model, prompt in jobs]
        for i, fut in enumerate(as_completed(futures), 1):
            row = fut.result()
            rows.append(row)
            snippet = (row.get("content") or row.get("error") or "")[:70].replace("\n", " ")
            print(f"  [{i}/{len(jobs)}] {row['model']} {row['prompt_id']} {snippet}", flush=True)

    rows.sort(key=lambda r: (r["model"], r["prompt_id"]))
    payload = {
        "system_prompt": SYSTEM,
        "prompts": PROMPTS,
        "payloads": extras,
        "skipped": skipped,
        "rows": rows,
    }
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT_PATH}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
