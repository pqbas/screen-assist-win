import os

import google.generativeai as genai

from overlay.mcq.config import GEMINI_DEFAULT_MODEL, PROMPT_TEMPLATE

_client = None
_model_name = None


def _load_config(path: str = ".env"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except Exception:
        lines = []

    cfg = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        cfg[k.strip()] = v.strip()

    api_key = cfg.get("GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", "")
    model = cfg.get("GEMINI_MODEL", "") or os.getenv("GEMINI_MODEL", GEMINI_DEFAULT_MODEL)

    if not api_key:
        print("[ERROR] Missing GEMINI_API_KEY in .env (or GEMINI_API_KEY environment variable).")
        return None, None

    return api_key, model


def _ensure_client():
    global _client, _model_name
    if _client is not None and _model_name is not None:
        return _client, _model_name

    api_key, model = _load_config()
    if not api_key or not model:
        return None, None

    try:
        genai.configure(api_key=api_key)
        _client = genai.GenerativeModel(
            model_name=model,
            system_instruction="You are an expert MCQ solver. Reply with ONLY a single capital letter (A, B, C, D, etc).",
        )
        _model_name = model
        print(f"[INFO] Gemini client initialized with model '{model}'.")
        return _client, _model_name
    except Exception as e:
        print("[ERROR] Failed to create Gemini client:", e)
        return None, None


def _extract_text(response) -> str:
    text = (getattr(response, "text", "") or "").strip()
    if text:
        return text

    try:
        for candidate in getattr(response, "candidates", None) or []:
            content = getattr(candidate, "content", None)
            parts = getattr(content, "parts", None) if content else None
            if not parts:
                continue
            for part in parts:
                p_text = (getattr(part, "text", "") or "").strip()
                if p_text:
                    return p_text
    except Exception:
        pass

    return ""


def get_answer(question_text: str) -> str:
    print("[INFO] Sending prompt to Gemini...")
    client, model = _ensure_client()
    if client is None or model is None:
        return "Gemini error: configuration or client not initialized (check .env)."

    try:
        prompt = PROMPT_TEMPLATE.format(question=question_text.strip())
        resp = client.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0),
        )
        text = _extract_text(resp)
        print("[INFO] Gemini responded:", text)
        return text if text else "No response"
    except Exception as e:
        print("[ERROR] Gemini API call failed:", e)
        return f"Gemini error: {e}"
