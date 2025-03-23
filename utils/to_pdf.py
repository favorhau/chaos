import markdown
from weasyprint import HTML, CSS
import os

def convert_markdown_to_pdf(md_dir_path):
    md_file_path = os.path.join(md_dir_path, 'README.md')
    md_file_pdf_path = os.path.join(md_dir_path, 'README.pdf')

    # 读取Markdown文件内容
    with open(md_file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 将Markdown转换为HTML
    html_text = markdown.markdown(text)
    # 定义CSS规则
    css = CSS(string="""
        img {
            width: 50%; /* 调整为你需要的宽度 */
            height: auto;
        }
    """)
    # 使用WeasyPrint将HTML转换为PDF
    HTML(string=html_text,base_url=md_dir_path).write_pdf(md_file_pdf_path, stylesheets=[css])
