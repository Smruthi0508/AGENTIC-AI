
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.verified_slide_content import (
    PAPER_TITLE,
    PAPER_AUTHORS,
    PUBLICATION,
    SLIDE_CONTENT,
)

OUTPUT_PATH = PROJECT_ROOT / "PaperPilot_Presentation_v5.pptx"



def add_title_slide(prs):
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.shapes import MSO_SHAPE

    # Use a blank slide instead of PowerPoint's default title layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Helper function for centered text
    def add_centered_text(text, y, height, font_size,
                          color, bold=False):
        box = slide.shapes.add_textbox(
            Inches(1.0), Inches(y),
            Inches(11.33), Inches(height)
        )

        frame = box.text_frame
        frame.clear()
        frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        frame.margin_left = Inches(0.1)
        frame.margin_right = Inches(0.1)

        paragraph = frame.paragraphs[0]
        paragraph.text = text
        paragraph.alignment = PP_ALIGN.CENTER
        paragraph.font.size = Pt(font_size)
        paragraph.font.bold = bold
        paragraph.font.color.rgb = RGBColor(*color)

        return box

    # Main title
    add_centered_text(
        PAPER_TITLE,
        2.0, 0.8, 34,
        (31, 78, 121), True
    )

    # Blue accent line
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(5.3), Inches(2.95),
        Inches(2.73), Inches(0.06)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(46, 117, 182)
    line.line.fill.background()

    # Presentation subtitle
    add_centered_text(
        "RESEARCH PAPER PRESENTATION",
        3.25, 0.45, 18,
        (100, 100, 100), False
    )

    # Author
    add_centered_text(
        "Ashish Vaswani et al.",
        4.15, 0.5, 20,
        (60, 60, 60), True
    )

    # Publication
    add_centered_text(
        PUBLICATION,
        4.85, 0.45, 17,
        (100, 100, 100), False
    )

    return slide


def add_architecture_diagram(slide):
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN

    def add_box(x, y, w, h, text, color):
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y),
            Inches(w), Inches(h)
        )

        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*color)
        shape.line.color.rgb = RGBColor(255, 255, 255)

        frame = shape.text_frame
        frame.text = text
        frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        frame.paragraphs[0].font.size = Pt(17)
        frame.paragraphs[0].font.bold = True
        frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    # Input
    add_box(0.8, 3.0, 2.0, 0.9, "Input\nEmbeddings",
            (91, 155, 213))

    # Encoder
    add_box(3.8, 2.3, 2.3, 2.3, "ENCODER\n\n6 Layers\n\nSelf-Attention\nFeed Forward",
            (46, 117, 182))

    # Decoder
    add_box(7.3, 2.3, 2.3, 2.3, "DECODER\n\n6 Layers\n\nMasked Attention\nCross-Attention",
            (112, 173, 71))

    # Output
    add_box(10.5, 3.0, 2.0, 0.9, "Output\nProbabilities",
            (237, 125, 49))

    # Arrows
    def add_arrow(x1, y1, x2, y2):
        line = slide.shapes.add_connector(
            1,
            Inches(x1), Inches(y1),
            Inches(x2), Inches(y2)
        )
        line.line.color.rgb = RGBColor(80, 80, 80)
        line.line.width = Pt(2)
        line.line.end_arrowhead = True

    add_arrow(2.8, 3.45, 3.8, 3.45)
    add_arrow(6.1, 3.45, 7.3, 3.45)
    add_arrow(9.6, 3.45, 10.5, 3.45)


def add_attention_diagram(slide):
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN

    def add_box(x, y, w, h, text, color):
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y),
            Inches(w), Inches(h)
        )

        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*color)
        shape.line.color.rgb = RGBColor(255, 255, 255)

        frame = shape.text_frame
        frame.text = text
        frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        frame.paragraphs[0].font.size = Pt(16)
        frame.paragraphs[0].font.bold = True
        frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    def add_arrow(x1, y1, x2, y2):
        line = slide.shapes.add_connector(
            1,
            Inches(x1), Inches(y1),
            Inches(x2), Inches(y2)
        )
        line.line.color.rgb = RGBColor(80, 80, 80)
        line.line.width = Pt(2)
        line.line.end_arrowhead = True

    # Input vectors
    add_box(0.8, 2.0, 2.0, 0.9, "Queries (Q)", (46, 117, 182))
    add_box(0.8, 3.2, 2.0, 0.9, "Keys (K)", (46, 139, 87))
    add_box(0.8, 4.4, 2.0, 0.9, "Values (V)", (237, 125, 49))

    # Attention calculation
    add_box(
        4.0, 2.7, 3.0, 1.8,
        "Scaled Dot-Product\n\nQKᵀ / √dk\n\nSoftmax",
        (112, 80, 160)
    )

    # Weighted values
    add_box(
        8.2, 2.7, 2.0, 1.8,
        "Attention\nWeights × V",
        (46, 139, 87)
    )

    # Final output
    add_box(
        11.0, 3.1, 1.8, 1.0,
        "Attention\nOutput",
        (31, 78, 121)
    )

    # Connections
    add_arrow(2.8, 2.45, 4.0, 3.0)
    add_arrow(2.8, 3.65, 4.0, 3.55)
    add_arrow(7.0, 3.6, 8.2, 3.6)
    add_arrow(2.8, 4.85, 8.2, 4.2)
    add_arrow(10.2, 3.6, 11.0, 3.6)


def add_technical_diagram(slide):
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN

    def add_box(x, y, w, h, heading, description, color):
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y),
            Inches(w), Inches(h)
        )

        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*color)
        shape.line.color.rgb = RGBColor(255, 255, 255)

        frame = shape.text_frame
        frame.clear()
        frame.word_wrap = True

        p = frame.paragraphs[0]
        p.text = heading
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

        p2 = frame.add_paragraph()
        p2.text = description
        p2.alignment = PP_ALIGN.CENTER
        p2.font.size = Pt(12)
        p2.font.color.rgb = RGBColor(255, 255, 255)

    def add_arrow(x1, y1, x2, y2):
        line = slide.shapes.add_connector(
            1,
            Inches(x1), Inches(y1),
            Inches(x2), Inches(y2)
        )
        line.line.color.rgb = RGBColor(80, 80, 80)
        line.line.width = Pt(2)
        line.line.end_arrowhead = True

    # Three technical components
    add_box(
        0.8, 2.4, 3.3, 1.5,
        "Word Embeddings",
        "Tokens converted into vectors",
        (46, 117, 182)
    )

    add_box(
        5.0, 2.4, 3.3, 1.5,
        "Positional Encoding",
        "Adds token position information",
        (46, 139, 87)
    )

    add_box(
        9.2, 2.4, 3.3, 1.5,
        "Feed-Forward Network",
        "Linear → ReLU → Linear",
        (112, 80, 160)
    )

    # Connect the components
    add_arrow(4.1, 3.15, 5.0, 3.15)
    add_arrow(8.3, 3.15, 9.2, 3.15)



def add_content_slide(prs, content):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Slide title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.25),
        Inches(12.3), Inches(0.7)
    )

    title_frame = title_box.text_frame
    title_frame.text = content["title"]

    title_p = title_frame.paragraphs[0]
    title_p.font.size = Pt(30)
    title_p.font.bold = True
    title_p.font.color.rgb = RGBColor(31, 78, 121)

    # Choose diagram and bullet positions
    if content["title"] == "Transformer Architecture":
        add_architecture_diagram(slide)
        bullet_y = 4.85
        bullet_font = 15

    elif content["title"] == "Attention Mechanisms":
        add_attention_diagram(slide)
        bullet_y = 5.45
        bullet_font = 13

    elif content["title"] == "Technical Components":
        add_technical_diagram(slide)
        bullet_y = 4.6
        bullet_font = 16

    else:
        bullet_y = 1.6
        bullet_font = 22

    # Add bullet points
    text_box = slide.shapes.add_textbox(
        Inches(0.7), Inches(bullet_y),
        Inches(12.0), Inches(1.35)
    )

    text_frame = text_box.text_frame
    text_frame.clear()
    text_frame.word_wrap = True

    for index, fact in enumerate(content["facts"]):
        p = (
            text_frame.paragraphs[0]
            if index == 0
            else text_frame.add_paragraph()
        )

        p.text = "• " + fact
        p.font.size = Pt(bullet_font)
        p.font.color.rgb = RGBColor(40, 40, 40)
        p.space_after = Pt(5)

    # Source footer
    footer = slide.shapes.add_textbox(
        Inches(0.5), Inches(7.05),
        Inches(12.0), Inches(0.2)
    )

    footer.text_frame.text = "Source: " + content["source"]

    footer_p = footer.text_frame.paragraphs[0]
    footer_p.font.size = Pt(9)
    footer_p.font.italic = True
    footer_p.font.color.rgb = RGBColor(100, 100, 100)

    return slide


def create_presentation():
    prs = Presentation()

    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    print("Creating title slide...")
    add_title_slide(prs)

    for number, content in enumerate(SLIDE_CONTENT, start=2):
        print(f"Creating slide {number}/9: {content['title']}")
        add_content_slide(prs, content)

    prs.save(OUTPUT_PATH)

    print("\nPresentation created successfully!")
    print(f"Total slides: {len(prs.slides)}")
    print(f"Saved to: {OUTPUT_PATH}")

    return OUTPUT_PATH


if __name__ == "__main__":
    create_presentation()
