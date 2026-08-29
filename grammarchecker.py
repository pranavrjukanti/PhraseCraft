##UI
import random
from utils import language_corrector
import streamlit as st

word=["Exploring","Reviewing","Analyzing","Understanding","Correcting","Enhancing","Refining","Improving","Polishing","Evaluating"]



def grammar_ui():
    st.title("Grammar Checker")
    st.write("Enter a sentence in any language. You'll get a corrected version "
             "plus an explanation of each mistake, written in that same language.")
    user_input = st.text_area("Your sentence")
    if st.button("Check my sentence"):
        if not user_input.strip():
            st.warning("Please Enter text")
        else:
            with st.spinner(random.choice(word)):
                result = language_corrector(user_input)
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                col1,col2=st.columns(2)
                with col1:
                    st.markdown("### Original Sentence")
                    st.text(result.get("original",""))
                with col2:
                    st.markdown(f"### Language: {result.get('language','unknown')}")
                    st.text(f"status: {result.get('status','unclear')}")
                
                corrected = result.get("corrected","")
                if corrected == "Input Correct":
                    st.success("Perfect! No corrections needed.")
                elif corrected is None:
                    st.warning("Input unclear, could not analyze.")
                else:
                    st.markdown("### Corrected Sentence")
                    st.text(corrected)
                
                if result.get("errors"):
                    st.markdown("### Errors Found")
                    for error in result["errors"]:
                        st.markdown(f"""
                        **{error.get('type', 'Error')}**  
                        `{error.get('original')}` → `{error.get('corrected')}`  
                        *Explanation*: {error.get('explanation')}
                        """)

                if result.get("notes"):
                    st.markdown("### Additional Notes")
                    for note in result["notes"]:
                        st.write(f"- {note}")

                    

   