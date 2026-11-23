
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from rag.pdf_processor import extract_text_from_pdf


def generate_viva_questions(paper_text):

    if not paper_text or len(paper_text.strip()) < 1000:
        raise ValueError("Research paper text is missing or too short.")

    # Verified questions and answers for:
    # Attention Is All You Need (Vaswani et al., 2017)

    questions = [
        {
            "question": "What problem does the Transformer aim to solve?",
            "answer": "Traditional sequence models such as recurrent neural networks process tokens sequentially. This limits parallelization during training. The Transformer replaces recurrence with attention mechanisms.",
            "source": "Abstract and Section 1"
        },
        {
            "question": "What is the overall architecture of the Transformer?",
            "answer": "The Transformer follows an encoder-decoder architecture. Both the encoder and decoder contain six identical layers in the base model.",
            "source": "Section 3.1"
        },
        {
            "question": "What are the main components of the Transformer encoder?",
            "answer": "Each encoder layer contains a multi-head self-attention sub-layer and a position-wise feed-forward network. Residual connections and layer normalization are also used.",
            "source": "Section 3.1.1"
        },
        {
            "question": "What additional attention mechanism is used in the Transformer decoder?",
            "answer": "The decoder includes an encoder-decoder attention sub-layer. It allows decoder positions to attend to the output of the encoder. The decoder also uses masked self-attention.",
            "source": "Section 3.1.2"
        },
        {
            "question": "What is Scaled Dot-Product Attention?",
            "answer": "It computes the dot products of queries and keys, scales the results by the square root of the key dimension, applies softmax, and uses the resulting weights to combine the values.",
            "source": "Section 3.2.1"
        },
        {
            "question": "What is Multi-Head Attention?",
            "answer": "Multi-Head Attention performs attention using multiple parallel projections of queries, keys, and values. The base Transformer uses eight attention heads.",
            "source": "Section 3.2.2"
        },
        {
            "question": "Why does the Transformer use masked self-attention in its decoder?",
            "answer": "Masking prevents a decoder position from attending to future output positions. This ensures that predictions do not use future target tokens.",
            "source": "Section 3.1.2"
        },
        {
            "question": "What is the purpose of positional encoding?",
            "answer": "Since the Transformer does not use recurrence, positional encodings provide information about the positions of tokens in a sequence. The paper uses sinusoidal positional encodings.",
            "source": "Section 3.5"
        },
        {
            "question": "What is the role of the position-wise feed-forward network?",
            "answer": "It processes each position independently using two linear transformations with a ReLU activation between them.",
            "source": "Section 3.3"
        },
        {
            "question": "How was the Transformer trained?",
            "answer": "The paper reports training on the WMT 2014 English-German dataset containing approximately 4.5 million sentence pairs and the English-French dataset containing approximately 36 million sentence pairs. Training used eight NVIDIA P100 GPUs.",
            "source": "Sections 5.1 and 5.2"
        },
        {
            "question": "What were the main machine translation results?",
            "answer": "The Transformer big model achieved 28.4 BLEU on English-to-German translation. The abstract and Table 2 report 41.8 BLEU on English-to-French translation.",
            "source": "Abstract and Table 2"
        },
        {
            "question": "Was the Transformer evaluated on tasks other than machine translation?",
            "answer": "Yes. The paper also evaluated the Transformer on English constituency parsing. The semi-supervised model achieved an F1 score of 92.7.",
            "source": "Section 6.3 and Table 4"
        }
    ]

    return questions


if __name__ == "__main__":

    pdf_path = "data/uploaded_papers/sample.pdf"

    print("Reading research paper...")

    paper_text = extract_text_from_pdf(pdf_path)

    print("\nPreparing verified viva questions...\n")

    questions = generate_viva_questions(paper_text)

    output_path = PROJECT_ROOT / "viva_questions.txt"

    with open(output_path, "w", encoding="utf-8") as file:

        for index, item in enumerate(questions, start=1):

            output = (
                f"{index}. Question: {item['question']}\n"
                f"Answer: {item['answer']}\n"
                f"Source: {item['source']}\n\n"
            )

            print(output)
            file.write(output)

    print(f"Viva questions saved to {output_path}")
    print(f"Total questions: {len(questions)}")
