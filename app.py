import streamlit as st

from rag.graph.workflow import workflow


# ============================================================
# PAGE CONFIG
# ============================================================

st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .main-caption {
        text-align: center;
        font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">🩺 BasicCare RAG Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-caption">Evidence-grounded healthcare assistant powered by LangGraph + Pinecone</div>',
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []



# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("About")

    st.write(
        """
        This application uses a Retrieval-Augmented Generation (RAG)
        pipeline to answer questions from the BasicCare knowledge base.

        The system shows:
        - Generated answer
        - Source citations
        - Retrieved evidence
        """
    )

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# DISPLAY PREVIOUS CHAT MESSAGES
# ============================================================

for message in st.session_state.messages:

    role = message["role"]

    with st.chat_message(role):

        # ----------------------------------------------------
        # USER MESSAGE
        # ----------------------------------------------------

        if role == "user":

            st.write(message["content"])

        # ----------------------------------------------------
        # ASSISTANT MESSAGE
        # ----------------------------------------------------

        else:

            st.write(message["answer"])

            # ------------------------------------------------
            # CITATIONS
            # ------------------------------------------------

            citations = message.get("citations", [])

            if citations:

                st.markdown("### 📚 Sources")

                for citation in citations:

                    st.markdown(
                        f"- **{citation}**"
                    )

            else:

                st.info("No supporting citation was returned.")


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask a question about the BasicCare guidelines..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    # --------------------------------------------------------
    # DISPLAY USER QUESTION
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.write(question)


    # --------------------------------------------------------
    # RUN LANGGRAPH WORKFLOW
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Searching the knowledge base..."):

            try:

                result = workflow.invoke(
                    {
                        "question": question,
                        "retrieved_docs": [],
                        "answer": "",
                        "citations": []
                    }
                )

                answer = result.get(
                    "answer",
                    "I could not generate an answer."
                )

                citations = result.get(
                    "citations",
                    []
                )

                retrieved_docs = result.get(
                    "retrieved_docs",
                    []
                )


                # ============================================
                # ANSWER
                # ============================================

                st.write(answer)


                # ============================================
                # CITATIONS
                # ============================================

                st.markdown("### 📚 Sources")

                if citations:

                    for citation in citations:

                        st.markdown(
                            f"- **{citation}**"
                        )

                else:

                    st.info(
                        "No supporting citation was returned."
                    )


                # ============================================
                # RETRIEVED EVIDENCE
                # ============================================

                with st.expander(
                    "🔎 View Retrieved Evidence"
                ):

                    if retrieved_docs:

                        for i, doc in enumerate(
                            retrieved_docs,
                            start=1
                        ):

                            metadata = doc.metadata

                            doc_id = metadata.get(
                                "doc_id",
                                "Unknown"
                            )

                            version = metadata.get(
                                "version",
                                "Unknown"
                            )

                            title = metadata.get(
                                "title",
                                metadata.get(
                                    "filename",
                                    "Unknown"
                                )
                            )

                            st.markdown(
                                f"### Evidence {i}"
                            )

                            st.markdown(
                                f"**Document:** `{doc_id}`"
                            )

                            st.markdown(
                                f"**Title:** {title}"
                            )

                            st.markdown(
                                f"**Version:** `{version}`"
                            )

                            if metadata.get("topic"):

                                st.markdown(
                                    f"**Topic:** "
                                    f"`{metadata['topic']}`"
                                )

                            if metadata.get("effective_date"):

                                st.markdown(
                                    f"**Effective Date:** "
                                    f"`{metadata['effective_date']}`"
                                )

                            st.write(
                                doc.page_content
                            )

                            if i < len(retrieved_docs):

                                st.divider()

                    else:

                        st.info(
                            "No retrieved documents were returned."
                        )


                # ============================================
                # SAVE ASSISTANT MESSAGE
                # ============================================

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "answer": answer,
                        "citations": citations
                    }
                )


            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )