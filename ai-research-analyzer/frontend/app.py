import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"  # Change if deployed

st.title("📄 AI Research Paper Analyzer")

# File Upload
st.header("Upload a Research Paper")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    response = requests.post(f"{API_URL}/api/upload/", files=files)
    
    if response.status_code == 200:
        paper_data = response.json()
        st.write(paper_data)
        st.success(f"File uploaded: {paper_data['file_path']}")

        paper_id = paper_data["paper_id"]

        # Analyze Paper
        if st.button("🔍 Analyze Paper"):
            analysis_response = requests.get(f"{API_URL}/api/analyze/{paper_id}")
            if analysis_response.status_code == 200:
                summary = analysis_response.json()["summary"]
                st.subheader("Summary")
                st.write(summary)
            else:
                st.error("Error analyzing paper")

        # # Recommend Similar Papers
        # if st.button("📌 Recommend Similar Papers"):
        #     rec_response = requests.get(f"{API_URL}/api/recommend/{paper_id}")
        #     if rec_response.status_code == 200:
        #         recommendations = rec_response.json()["recommendations"]
        #         st.subheader("Recommended Papers")
        #         for rec in recommendations:
        #             st.write(f"🔹 {rec['title']}")
        #     else:
        #         st.error("Error fetching recommendations")

        search_type = st.radio("🔍 Search for similar papers:", ["Local Database", "Internet"])
        if st.button("📌 Find Similar Papers"):
            source = "local" if search_type == "Local Database" else "internet"
            response = requests.get(f"{API_URL}/api/recommend/{paper_id}", params={"source": source})

            if response.status_code == 200:
                data = response.json()
                recommendations = data["recommendations"]
                st.subheader(f"🔎 Research Papers Found ({search_type}):")
                for rec in recommendations:
                    if source == "internet":
                        st.markdown(f"🔹 [{rec['title']}]({rec['link']})")
                    else:
                        st.markdown(f"🔹 {rec['title']}")
            else:
                st.error("No recommendations found")

                

    else:
        st.error("Failed to upload file")
