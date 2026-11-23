
"""
Verified slide content for PaperPilot AI.

Source:
Attention Is All You Need (Vaswani et al., 2017)

These facts are extracted from the original research paper.
The LLM will simplify their wording, not invent new facts.
"""

PAPER_TITLE = "Attention Is All You Need"

PAPER_AUTHORS = (
    "Ashish Vaswani, Noam Shazeer, Niki Parmar, "
    "Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, "
    "Lukasz Kaiser, and Illia Polosukhin"
)

PUBLICATION = "NeurIPS 2017"


SLIDE_CONTENT = [
    {
        "title": "Research Problem",
        "facts": [
            "Traditional recurrent neural networks process input and output sequences sequentially.",
            "Sequential computation limits parallelization during model training.",
            "The Transformer replaces recurrence with attention mechanisms to model dependencies across sequences.",
        ],
        "source": "Abstract and Section 1: Introduction",
    },
    {
        "title": "Transformer Architecture",
        "facts": [
            "The Transformer follows an encoder-decoder architecture.",
            "The encoder and decoder each contain six identical layers in the base model.",
            "The encoder uses self-attention and feed-forward sub-layers, while the decoder adds encoder-decoder attention.",
        ],
        "source": "Section 3 and Section 3.1",
    },
    {
        "title": "Attention Mechanisms",
        "facts": [
            "Attention maps queries and key-value pairs to an output computed as a weighted sum of values.",
            "Scaled dot-product attention calculates query-key similarity and applies softmax to obtain attention weights.",
            "The base Transformer uses eight parallel attention heads to capture information from different representation subspaces.",
        ],
        "source": "Sections 3.2, 3.2.1 and 3.2.2",
    },
    {
        "title": "Technical Components",
        "facts": [
            "Position-wise feed-forward networks use two linear transformations with a ReLU activation between them.",
            "Learned embeddings convert input and output tokens into vectors.",
            "Sinusoidal positional encodings are added to embeddings to provide information about token positions.",
        ],
        "source": "Sections 3.3, 3.4 and 3.5",
    },
    {
        "title": "Training Methodology",
        "facts": [
            "The English-German dataset contains approximately 4.5 million sentence pairs.",
            "The English-French dataset contains approximately 36 million sentences.",
            "Models were trained using eight NVIDIA P100 GPUs; the big model was trained for 300,000 steps over 3.5 days.",
        ],
        "source": "Sections 5.1 and 5.2",
    },
    {
        "title": "Results and Experiments",
        "facts": [
            "The Transformer big model achieved 28.4 BLEU on WMT 2014 English-to-German translation.",
            "The paper's abstract and Table 2 report 41.8 BLEU for English-to-French translation.",
            "The semi-supervised Transformer achieved 92.7 F1 on English constituency parsing.",
        ],
        "source": "Abstract, Tables 2 and 4, Sections 6.1 and 6.3",
        "note": "Section 6.1 reports 41.0 BLEU for English-French, whereas the abstract and Table 2 report 41.8. Preserve this discrepancy for review.",
    },
    {
        "title": "Key Findings",
        "facts": [
            "Self-attention connects sequence positions without requiring recurrent processing.",
            "Multi-head attention allows the model to attend to different representation subspaces.",
            "The experiments demonstrate that the Transformer can also perform English constituency parsing.",
        ],
        "source": "Sections 3.2, 4 and 6.3",
    },
    {
        "title": "Conclusion",
        "facts": [
            "The Transformer is a sequence transduction model based entirely on attention mechanisms.",
            "It achieved strong machine translation results and trained faster than recurrent and convolutional architectures.",
            "The authors proposed exploring attention-based models for other modalities, including images, audio and video.",
        ],
        "source": "Section 7: Conclusion",
    },
]
