# MoodMate — an emotion-aware companion

**MoodMate detects the emotion behind your words using a transformer fine-tuned on Google's GoEmotions dataset, and responds like a friend who actually listens — built for people who find it hard to open up.**

 **Live demo:** https://moodmate-aolrddhkapglkkpzovxhgf.streamlit.app/

**Work Demo:**

![Chat screenshot](assets/chat.png)
![Mood dashboard](assets/dashboard.png)

---

## Why this exists

Many people especially those who struggle to verbalize what they feel, even to themselves find it hard to open up. MoodMate doesn't ask you to explain your emotions; it detects them from what you naturally type, responds with validation instead of advice, and quietly builds a picture of your emotional patterns over time that you can see on a dashboard.

## How it works

```
User message
     │
     ▼
[Safety check] ──crisis detected──► helpline resources shown, chat pauses
     │ ok
     ▼
[Emotion classifier]  ← DistilRoBERTa fine-tuned on GoEmotions (27 emotions)
     │  e.g. {"sadness": 0.81, "loneliness": 0.64}
     ▼
[LLM responder]  ← detected emotions injected into an empathetic system prompt
     ▼
[Mood journal]  → SQLite log → Plotly trend dashboard
```

## The ML part

- **Dataset:** [GoEmotions](https://huggingface.co/datasets/google-research-datasets/go_emotions) — 58k Reddit comments hand-labeled with 27 emotions + neutral, by Google Research. Chosen because real, messy, conversational text matches what users actually type (unlike formal sentiment datasets).
- **Model:** `distilroberta-base` fine-tuned for multi-label classification (a message can be *sad and anxious at once*), trained for 2 epochs on a T4 GPU in Colab.
- **Results on the GoEmotions test split** (threshold 0.3):

| Metric | Score |
|---|---|
| Micro F1 | 0.592 |
| Macro F1 | 0.375 |

Rare emotions (e.g. *grief*, *relief*) score lower due to class imbalance — a known GoEmotions challenge and an area for future work (class weighting / focal loss).

Training code and full per-emotion results: [`notebooks/finetune_goemotions.ipynb`](notebooks/finetune_goemotions.ipynb)

## Tech stack

Python · Hugging Face Transformers · PyTorch · Streamlit · Plotly · SQLite · Groq/Anthropic LLM API · pytest

## Run it locally

```bash
git clone https://github.com/hars8694-lab/MoodMate.git
cd MoodMate
python -m venv .venv
.venv\Scripts\activate            # Windows  (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env            # then paste your API key into .env
streamlit run app.py
```

Run the tests: `python -m pytest`

## Reproducing the emotion model

The fine-tuned model (~300 MB) is not stored in this repo due to GitHub's 100 MB file limit. Two options:

1. **Recreate it:** open `notebooks/finetune_goemotions.ipynb` in Google Colab (T4 GPU runtime), run all cells (~25 min), download the resulting folder to `models/moodmate-emotion-model/`.
2. **Or do nothing:** the app automatically falls back to the public pretrained model `j-hartmann/emotion-english-distilroberta-base` when no local model is found.

## Limitations & ethics

- **MoodMate is a companion app, not a substitute for professional mental-health care.** A persistent disclaimer states this in the UI.
- Messages indicating crisis-level distress bypass the normal chat flow and surface helpline resources (Tele-MANAS 14416 for India, findahelpline.com internationally). This layer is covered by unit tests.
- The emotion classifier is trained on English Reddit data and may perform worse on other dialects, code-mixed text, or non-Western emotional expression.
- Conversations are stored only in a local SQLite file on the user's machine; nothing is sent anywhere except the LLM API call itself.

## What I'd build next

- Retrieval over the EmpatheticDialogues dataset to ground replies in similar real situations
- Class-imbalance handling to lift macro F1 on rare emotions
- Weekly mood summaries generated from the journal