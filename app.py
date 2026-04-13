import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🚀 Ad2Page AI Personalizer")
st.caption("Turn your ads into high-converting landing pages using AI + CRO")

ad_text = st.text_area("Paste Ad Creative")
url = st.text_input("Enter Landing Page URL")

def scrape_page(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.title.string if soup.title else ""
        h1 = soup.find("h1")
        h1_text = h1.text if h1 else ""

        p = soup.find("p")
        p_text = p.text if p else ""

        return {
            "title": title,
            "headline": h1_text,
            "description": p_text
        }
    except:
        return None

def personalize(ad, page_data):
    prompt = f"""
Ad:
{ad}

Page:
Title: {page_data['title']}
Headline: {page_data['headline']}
Description: {page_data['description']}

Rewrite headline, description and CTA.
Return JSON:
{{"headline":"","description":"","cta":""}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

if st.button("Generate"):
    if ad_text and url:
        with st.spinner("Analyzing ad + optimizing page..."):
            data = scrape_page(url)
            if data:
                result = personalize(ad_text, data)

                import json

                st.subheader("🔍 Before vs After")

                try:
                    parsed = json.loads(result)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### ❌ Original Page")
                        st.write("**Headline:**", data["headline"])
                        st.write("**Description:**", data["description"])

                    with col2:
                        st.markdown("### ✅ Personalized Page")
                        st.write("**Headline:**", parsed["headline"])
                        st.write("**Description:**", parsed["description"])
                        st.write("**CTA:**", parsed["cta"])

                except:
                    st.write(result)

            else:
                st.error("Error fetching page")
                st.markdown("---")
st.markdown("### 💡 Why this works")
st.write("""
- Ensures message match between ad and landing page  
- Improves conversion rates  
- Applies CRO principles like urgency & clarity  
""")
