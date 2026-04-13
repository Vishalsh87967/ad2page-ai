import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🚀 Ad2Page AI Personalizer")

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
        data = scrape_page(url)
        if data:
            result = personalize(ad_text, data)
            st.write("Original:", data)
            st.write("Personalized:", result)
        else:
            st.error("Error fetching page")
