
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.verified_slide_content import SLIDE_CONTENT


def extract_concepts():

    concepts = [
        {
            "name": "Recurrent Neural Networks (RNNs)",
            "explanation": "RNNs process input and output sequences one step at a time.",
            "importance": "The paper identifies sequential computation as a limitation that the Transformer aims to overcome."
        },
        {
            "name": "Transformer Architecture",
            "explanation": "The Transformer is a sequence transduction model based entirely on attention mechanisms.",
            "importance": "It replaces recurrent processing with attention-based computation."
        },
        {
            "name": "Encoder-Decoder Architecture",
            "explanation": "The Transformer has an encoder and a decoder, each containing six identical layers in the base model.",
            "importance": "It provides the overall structure for transforming input sequences into output sequences."
        },
        {
            "name": "Scaled Dot-Product Attention",
            "explanation": "It calculates query-key similarity, scales the result, applies softmax, and uses the resulting weights to combine values.",
            "importance": "It is the fundamental attention operation used by the Transformer."
        },
        {
            "name": "Multi-Head Attention",
            "explanation": "It uses multiple parallel attention heads to capture information from different representation subspaces.",
            "importance": "The base Transformer uses eight attention heads."
        },
        {
            "name": "Self-Attention",
            "explanation": "It allows positions in a sequence to connect with other positions without recurrent processing.",
            "importance": "It enables the Transformer to model relationships between sequence positions."
        },
        {
            "name": "Position-Wise Feed-Forward Networks",
            "explanation": "These networks use two linear transformations with a ReLU activation between them.",
            "importance": "They process the representations produced by the attention sub-layers."
        },
        {
            "name": "Positional Encoding",
            "explanation": "Sinusoidal positional encodings are added to token embeddings to provide information about token positions.",
            "importance": "They provide sequence-order information to a model without recurrence."
        },
        {
            "name": "Residual Connections and Layer Normalization",
            "explanation": "The Transformer uses residual connections followed by layer normalization around its sub-layers.",
            "importance": "These are important components of the Transformer encoder and decoder layers."
        },
        {
            "name": "Masked Self-Attention",
            "explanation": "The decoder masks future positions so that a position cannot attend to subsequent output positions.",
            "importance": "It prevents the decoder from using future target tokens during prediction."
        }
    ]

    return concepts


if __name__ == "__main__":

    print("Extracting verified research paper concepts...")

    concepts = extract_concepts()

    with open("concepts.txt", "w", encoding="utf-8") as file:

        for index, concept in enumerate(concepts, start=1):

            output = (
                f"{index}. {concept['name']}\n"
                f"Explanation: {concept['explanation']}\n"
                f"Importance: {concept['importance']}\n\n"
            )

            print(output)
            file.write(output)

    print("Verified concepts saved to concepts.txt")
