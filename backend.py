import openai
import os
import PyPDF2
import streamlit as st


# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Read the API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def identify_bullet_points(text):
    lines = text.split('\n')
    bullet_point_lines = []
    current_bullet_point = ''
    started = False
    
    for line in lines:
        if not started:
            if line.strip().startswith('-') or line.strip().startswith('•'):
                started = True
                current_bullet_point = line
            continue
        
        if line.strip().startswith('-') or line.strip().startswith('•'):
            if current_bullet_point:
                bullet_point_lines.append(current_bullet_point.strip())
            current_bullet_point = line
        else:
            current_bullet_point += ' ' + line
    
    if current_bullet_point:
        bullet_point_lines.append(current_bullet_point.strip())
    
    return bullet_point_lines



def improve_bullet_points(bullet_points):
    prompt = (
        "you are to help me improve my software engineering resume. "
        "The xyz method refers to a way of formatting/writing bullet points. "
        "In one sentence, it includes what you've accomplished (X) + the qualitative results (Y) + the skills or experience you utilized to achieve the outcome (Z). "
        "Essentially, it's an easy-to-read, concise, and practical way to provide context and flow. "
        "I will give you a series of bullet points, and I need you to rewrite them to follow the xyz method, while keeping things concise. "
        "For every bullet point I give you, I want you to return an improved bullet point that fits the above criteria. "
        "If you don’t know the skills used or qualitative results, make some up but enclose them in these {} brackets so the user knows to replace them later.\n\n"
    )
    
    improved_bullet_points = []

    for point in bullet_points:
        conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "assistant", "content": prompt},
            {"role": "user", "content": point}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            max_tokens=100,
            temperature=0.7
        )
        
        assistant_response = response.choices[-1].message['content']
        improved_bullet_points.append(assistant_response)

    return improved_bullet_points


def main():
    st.set_page_config(page_title="CleverCV",
                       page_icon=":memo:")

    st.title("CleverCV")
    st.caption("Leverage AI to get more interviews!")

    st.sidebar.title("Instructions")
    st.sidebar.write(
        "1. **Upload your resume PDF file.**\n"
        "2. **Chat with CleverCV to get improved bullet points.**"
    )

    st.sidebar.header("FAQ")
    st.sidebar.markdown(
        "**Why do the AI suggestions include words in curly brackets sometimes?**\n"
        "\n"
        "The curly brackets are meant to signify areas that the user will need to put manual fill in. Just off the resume alone, the AI cannot tell what tools you used or achievement metrics for tasks, and so the curly brackets are to prompt you to enter them in yourself.\n"
        "\n"
        "**Why does CleverCV occasionally offer several bullet point suggestions?**\n"
        "\n"
        "Sometimes when your original bullet point contains an excessive amount of information, the GPT-3.5 model will suggest multiple bullets instead for improved clarity and conciseness. This is an intentional feature! Remember the key is that we want to convey as much relevant information as simply as possible.\n"
        "\n"
        "**Does CleverCV store my data? Is it Secure?**\n"
        "\n"
        "CleverCV does not store your data! As soon as you exit or refresh the page, your data will be erased from our history\n"
        "\n"
        "**Is CleverCV free?**\n"
        "\n"
        "Yes, CleverCV is free currently! However, it is important to keep in mind that this is subject to change based on demand; We get charged with each API call, and so high demand could result in changes in the future.\n"
        "\n"
        "**Where can I send suggestions or report bugs?**\n"
        "\n"
        "Please reach out to abhrajyo@ualberta.ca with any queries regarding CleverCV!"
    )


    uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        bullet_point_lines = identify_bullet_points(pdf_text)
        
        # st.write("## Original Bullet Points:")
        # for line in bullet_point_lines:
        #    st.write("**Original:**", line)
        #    st.write()

        with st.spinner("Improving bullet points..."):
            improved_bullet_points = improve_bullet_points(bullet_point_lines)

        st.write("## Improved Bullet Points:")
        for original_point, improved_point in zip(bullet_point_lines, improved_bullet_points):
            st.write("----------------------------------------------------")
            st.write("**Original:**", original_point)
            if improved_point.startswith("•") or improved_point.startswith("-"):
                improved_point = improved_point[1:].strip()
            st.write("**Improved:**", improved_point)
            st.write("----------------------------------------------------")
            st.write()

if __name__ == "__main__":
    main()