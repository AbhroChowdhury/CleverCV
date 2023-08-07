import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
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
    
    for line in lines:
        if line.strip().startswith('-') or line.strip().startswith('•'):
            if current_bullet_point:
                bullet_point_lines.append(current_bullet_point.strip())
            current_bullet_point = line
        else:
            current_bullet_point += ' ' + line
    
    if current_bullet_point:
        bullet_point_lines.append(current_bullet_point.strip())
    
    return bullet_point_lines

pdf_text = extract_text_from_pdf('resume.pdf')
bullet_point_lines = identify_bullet_points(pdf_text)

for line in bullet_point_lines:
    print(line)
