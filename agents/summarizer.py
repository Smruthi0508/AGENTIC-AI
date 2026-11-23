
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.llm import llm
from agents.verified_slide_content import SLIDE_CONTENT


def build_verified_summary():
    """Generate a structured summary using verified paper facts."""

    sections = []

    for section in SLIDE_CONTENT:
        title = section["title"]
        facts = section["facts"]
        source = section["source"]
        note = section.get("note", "")

        facts_text = "\n".join(f"- {fact}" for fact in facts)

        prompt = f"""
You are an academic research paper assistant.

Rewrite the following verified research facts into a
clear, concise academic explanation.

STRICT RULES:
- Use only the supplied facts.
- Do not add outside knowledge.
- Do not invent results, datasets, or experiments.
- Preserve technical terminology and numerical values.
- Do not change the meaning of any fact.
- Write approximately 50-70 words.
- If a note is supplied, preserve its important details.

SECTION: {title}

VERIFIED FACTS:
{facts_text}

SOURCE: {source}

ADDITIONAL NOTE:
{note if note else "None"}

Write the explanation:
"""

        print(f"Generating: {title}...")

        try:
            response = llm.invoke(prompt)
            explanation = response.content.strip()
        except Exception as error:
            print(f"LLM error in {title}: {error}")
            explanation = facts_text

        # Use fixed, verified explanations for critical sections.
        if title == "Research Problem":
            explanation = (
                "Traditional recurrent neural networks process input "
                "and output sequences sequentially. This sequential "
                "computation limits parallelization during training. "
                "The Transformer, introduced in Attention Is All You Need, "
                "replaces recurrence with attention mechanisms to model "
                "dependencies across sequences."
            )

        
        elif title == "Transformer Architecture":
            explanation = (
                "The Transformer architecture was introduced in the "
                "paper Attention Is All You Need. It follows an "
                "encoder-decoder architecture. Both encoder and decoder "
                "contain six identical layers in the base model. The "
                "encoder uses self-attention and feed-forward sub-layers, "
                "while the decoder additionally uses encoder-decoder "
                "attention. The architecture replaces recurrence "
                "with attention mechanisms."
            )
        

        elif title == "Technical Components":
            explanation = (
                "Position-wise feed-forward networks use two linear "
                "transformations with a ReLU activation between them. "
                "Learned embeddings convert input and output tokens "
                "into vectors. Sinusoidal positional encodings are "
                "added to these embeddings to provide information "
                "about token positions."
            )

        elif title == "Training Methodology":
            explanation = (
                "The English-German training dataset contains "
                "approximately 4.5 million sentence pairs, while "
                "the English-French dataset contains approximately "
                "36 million sentences. The models were trained using "
                "eight NVIDIA P100 GPUs. The big model was trained "
                "for 300,000 steps over 3.5 days."
            )

        elif title == "Results and Experiments":
            explanation = (
                "The Transformer big model achieved 28.4 BLEU on "
                "WMT 2014 English-to-German translation. The abstract "
                "and Table 2 report 41.8 BLEU for English-to-French "
                "translation, while Section 6.1 reports 41.0 BLEU. "
                "This discrepancy is retained for review. The "
                "semi-supervised Transformer achieved 92.7 F1 "
                "on English constituency parsing."
            )

        sections.append(
            f"{title}\n{'-' * len(title)}\n{explanation}\n"
        )

    return "\n".join(sections)


if __name__ == "__main__":

    print("\nGenerating verified research paper summary...\n")

    summary = build_verified_summary()

    print("\n========== PAPERPILOT AI SUMMARY ==========\n")
    print(summary)

    output_path = PROJECT_ROOT / "paper_summary.txt"

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(summary)

    print(f"\nSummary saved to: {output_path}")
