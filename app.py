import streamlit as st


# Import your function
from agents import generate_profile_summary_and_facts_single_step

st.set_page_config(page_title="LinkedIn Profile Summarizer", page_icon="🔍")

st.title("🔍 LinkedIn Profile Summarizer")
st.write("Enter a person's full name to find their LinkedIn summary and interesting facts.")

# Text input
name = st.text_input("Full Name", "")

# Run the agent
if st.button("Generate Summary"):
    if name:
        with st.spinner("Generating... Please wait!"):
            try:
                result = generate_profile_summary_and_facts_single_step(name)
                
                # Display results
                st.success("Profile Summary Generated!")

                # If you have intermediate steps you want to show
                if "intermediate_steps" in result:
                    with st.expander("🔎 See Steps"):
                        for step in result["intermediate_steps"]:
                            st.write(f"**Action:** {step[0]}")
                            st.write(f"**Observation:** {step[1]}")

                # Final Output
                summary = result.get("summary", "No summary available.")
                interesting_facts = result.get("interesting_facts", [])
                profile_pic_url = result.get("profile_pic_url", None)

                st.subheader("📝 LinkedIn Summary")
                st.write(summary)

                st.subheader("✨ Interesting Facts")
                for fact in interesting_facts:
                    st.write(f"• {fact}")

                if profile_pic_url:
                    st.subheader("📷 Profile Picture")
                    st.image(profile_pic_url, width=250)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please enter a full name to proceed.")
