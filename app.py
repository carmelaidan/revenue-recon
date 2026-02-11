# ... previous code ...

    # --- EXECUTIVE REPORT ---
    st.subheader("📄 Executive Audit Report")
    
    # Initialize session state for the report if it doesn't exist
    if "ai_summary" not in st.session_state:
        st.session_state.ai_summary = None
    if "pdf_file" not in st.session_state:
        st.session_state.pdf_file = None

    # Step 1: Generate the Text
    if st.button("📝 Draft Executive Analysis"):
        with st.spinner("Drafting Strategic Analysis..."):
            st.session_state.ai_summary = generate_audit_narrative(target_name, user_url, score, ssl, ports, seo, tech)
            
            # Auto-generate PDF immediately after text
            st.session_state.pdf_file = create_pdf(target_name, user_url, score, st.session_state.ai_summary, ssl, seo, tech)

    # Step 2: Show and Download (Persistent)
    if st.session_state.ai_summary:
        st.info(st.session_state.ai_summary)
        
        if st.session_state.pdf_file:
            with open(st.session_state.pdf_file, "rb") as f:
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=f,
                    file_name=st.session_state.pdf_file,
                    mime="application/pdf"
                )