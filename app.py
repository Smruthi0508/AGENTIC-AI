
import streamlit as st
from pathlib import Path
import sys

# Project configuration
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# Agent imports
from rag.pdf_processor import extract_text_from_pdf
from agents.summarizer import build_verified_summary
from agents.concept_extractor import extract_concepts
from agents.slide_generator import create_presentation
from agents.viva_agent import generate_viva_questions


# Page configuration
st.set_page_config(
    page_title="PaperPilot AI",
    page_icon="📚",
    layout="wide"
)


# Initialize session state
if "paper_text" not in st.session_state:
    st.session_state["paper_text"] = None


# Custom styling
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #2563EB;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 18px;
        color: #777777;
        margin-top: 5px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 600;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# Header
st.markdown(
    '<p class="main-title">📚 PaperPilot AI</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Multi-Agent Research Paper Assistant</p>',
    unsafe_allow_html=True
)

st.write(
    "Transform research papers into understandable summaries, "
    "important concepts, presentations, and viva preparation material."
)

st.divider()


# Sidebar
with st.sidebar:

    st.title("📚 PaperPilot AI")

    st.markdown("### About the Project")

    st.write(
        "PaperPilot AI helps students understand and present "
        "research papers using specialized AI agents."
    )

    st.divider()

    st.markdown("### Available Tools")

    st.write("📝 Research Paper Summary")
    st.write("💡 Important Concepts")
    st.write("📊 PowerPoint Generation")
    st.write("🎓 Viva Questions")

    st.divider()

    if st.session_state["paper_text"]:
        st.success("Research paper processed")
    else:
        st.info("Upload and process a PDF to begin.")


# PDF Upload
st.markdown("## 📄 Upload Research Paper")

uploaded_file = st.file_uploader(
    "Choose a research paper in PDF format",
    type=["pdf"]
)


if uploaded_file is not None:

    upload_folder = PROJECT_ROOT / "data" / "uploaded_papers"
    upload_folder.mkdir(parents=True, exist_ok=True)

    pdf_path = upload_folder / uploaded_file.name

    # Save uploaded PDF
    with open(pdf_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    st.success(f"Uploaded successfully: {uploaded_file.name}")

    if st.button("📖 Read and Process Research Paper"):

        try:
            with st.spinner("Reading and processing your research paper..."):

                paper_text = extract_text_from_pdf(str(pdf_path))

                if not paper_text or len(paper_text.strip()) < 100:
                    st.error("Could not extract sufficient text from this PDF.")
                else:
                    st.session_state["paper_text"] = paper_text
                    st.session_state["processed_filename"] = uploaded_file.name

                    # Clear previous generated outputs
                    for key in [
                        "summary",
                        "concepts",
                        "presentation_path",
                        "viva_questions"
                    ]:
                        st.session_state.pop(key, None)

                    st.success("Research paper processed successfully!")

        except Exception as error:
            st.error(f"An error occurred while reading the PDF: {error}")


# Research Paper Information
if st.session_state["paper_text"]:

    st.divider()

    st.markdown("## 📊 Research Paper Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Extracted Characters",
            f"{len(st.session_state['paper_text']):,}"
        )

    with col2:
        st.metric(
            "Available AI Tools",
            "4"
        )

    st.caption(
        "Paper: " +
        st.session_state.get("processed_filename", "Uploaded PDF")
    )

    st.divider()

    st.markdown("## 🚀 Research Paper Tools")

    st.write(
        "Choose a tool below to explore and prepare your research paper."
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Summary",
        "💡 Concepts",
        "📊 Presentation",
        "🎓 Viva Questions"
    ])


    # SUMMARY AGENT
    with tab1:

        st.subheader("📝 Research Paper Summary")

        st.write(
            "Understand the research problem, architecture, "
            "methodology, experiments, and findings."
        )

        if st.button("Generate Summary", key="summary_button"):

            try:
                with st.spinner("Generating research summary..."):

                    summary = build_verified_summary()

                    st.session_state["summary"] = summary

                st.success("Summary generated successfully!")

            except Exception as error:
                st.error(f"Summary generation failed: {error}")

        if "summary" in st.session_state:

            st.divider()

            st.markdown(st.session_state["summary"])


    # CONCEPT EXTRACTOR
    with tab2:

        st.subheader("💡 Important Research Concepts")

        st.write(
            "Explore the important technical concepts discussed "
            "in the research paper."
        )

        if st.button("Extract Concepts", key="concept_button"):

            try:
                with st.spinner("Extracting important concepts..."):

                    concepts = extract_concepts()

                    st.session_state["concepts"] = concepts

                st.success("Concepts extracted successfully!")

            except Exception as error:
                st.error(f"Concept extraction failed: {error}")

        if "concepts" in st.session_state:

            st.divider()

            for index, concept in enumerate(
                st.session_state["concepts"], start=1
            ):

                with st.expander(
                    f"{index}. {concept['name']}",
                    expanded=False
                ):

                    st.markdown("**Explanation**")
                    st.write(concept["explanation"])

                    st.markdown("**Importance**")
                    st.write(concept["importance"])


    # PRESENTATION GENERATOR
    with tab3:

        st.subheader("📊 PowerPoint Presentation")

        st.write(
            "Generate a presentation containing the important "
            "information and diagrams from the research paper."
        )

        if st.button(
            "Generate Presentation",
            key="presentation_button"
        ):

            try:
                with st.spinner("Creating your PowerPoint presentation..."):

                    presentation_path = create_presentation()

                    st.session_state["presentation_path"] = presentation_path

                st.success("Presentation created successfully!")

            except Exception as error:
                st.error(f"Presentation generation failed: {error}")

        if "presentation_path" in st.session_state:

            presentation_path = Path(
                st.session_state["presentation_path"]
            )

            if presentation_path.exists():

                st.info("Your PowerPoint presentation is ready.")

                with open(presentation_path, "rb") as file:

                    st.download_button(
                        label="⬇️ Download PowerPoint Presentation",
                        data=file,
                        file_name=presentation_path.name,
                        mime=(
                            "application/vnd.openxmlformats-officedocument."
                            "presentationml.presentation"
                        ),
                        key="download_presentation"
                    )

            else:
                st.warning("Presentation file could not be found.")


    # VIVA AGENT
    with tab4:

        st.subheader("🎓 Viva Questions and Answers")

        st.write(
            "Prepare for your research paper viva with "
            "important questions and their answers."
        )

        if st.button(
            "Generate Viva Questions",
            key="viva_button"
        ):

            try:
                with st.spinner("Preparing viva questions..."):

                    questions = generate_viva_questions(
                        st.session_state["paper_text"]
                    )

                    st.session_state["viva_questions"] = questions

                st.success("Viva questions generated successfully!")

            except Exception as error:
                st.error(f"Viva question generation failed: {error}")

        if "viva_questions" in st.session_state:

            st.divider()

            for index, item in enumerate(
                st.session_state["viva_questions"], start=1
            ):

                with st.expander(
                    f"Question {index}: {item['question']}",
                    expanded=False
                ):

                    st.markdown("**Answer**")
                    st.write(item["answer"])

                    st.caption("Source: " + item["source"])


# Footer
st.divider()

st.markdown(
    "<center>📚 <b>PaperPilot AI</b> | "
    "Multi-Agent Research Paper Assistant</center>",
    unsafe_allow_html=True
)
