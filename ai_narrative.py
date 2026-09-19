import os

from openai import OpenAI


def generate_release_narrative(
    overall_score,
    overall_decision,
    blocked_modules,
    critical_defects,
    unresolved_risks
):

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not configured. "
            "Please set your OpenAI API key before generating the narrative."
        )

    client = OpenAI(api_key=api_key)

    blocker_text = "\n".join(
        [
            f"- {row['Module']}: "
            f"{'; '.join(row['Reasons'])}"
            for _, row in blocked_modules.iterrows()
        ]
    )

    prompt = f"""
You are a software release quality analyst.

Generate a concise engineering release-readiness narrative
using ONLY the information provided below.

Overall readiness score: {overall_score:.1f}/100
Release decision: {overall_decision}
Total critical defects: {critical_defects}
Total unresolved risks: {unresolved_risks}

Blocked modules:
{blocker_text}

Rules:
- Do not change the release decision.
- Do not calculate a new score.
- Do not invent defects, risks, or metrics.
- Explain the main reasons behind the existing decision.
- Mention the most important blocked modules.
- Keep the response between 3 and 5 sentences.
- Use professional engineering language.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return response.output_text


