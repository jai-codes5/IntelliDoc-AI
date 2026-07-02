import os
import json
import requests
import re
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_pdf_document(pdf_path):
    if not PYPDF_AVAILABLE:
        print("[System Check] ERROR: pypdf library is NOT installed!")
        return None
    try:
        reader = PdfReader(pdf_path)
        buffer_text = []
        for page in reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                buffer_text.append(extracted_text)
        return "\n".join(buffer_text).strip()
    except Exception as e:
        print(f"[PDF Extract Error]: {str(e)}")
        return None

def convert_markdown_to_clean_html(markdown_text):
    lines = markdown_text.split('\n')
    html_output = []
    in_list = False
    
    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            if in_list:
                html_output.append('</ul>')
                in_list = False
            continue
            
        if cleaned_line.startswith('#'):
            if in_list:
                html_output.append('</ul>')
                in_list = False
            header_level = len(cleaned_line) - len(cleaned_line.lstrip('#'))
            header_text = cleaned_line.lstrip('#').strip()
            header_text = re.sub(r'\*\*(.*?)\*\*', r'\1', header_text)
            
            if header_level == 1:
                html_output.append(f'<h1 class="payload-h1">{header_text}</h1>')
            elif header_level == 2:
                html_output.append(f'<h2 class="payload-h2">{header_text}</h2>')
            else:
                html_output.append(f'<h3 class="payload-h3">{header_text}</h3>')
                
        elif cleaned_line.startswith('* ') or cleaned_line.startswith('- '):
            if not in_list:
                html_output.append('<ul class="payload-ul">')
                in_list = True
            list_item_text = cleaned_line[2:].strip()
            list_item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="payload-strong">\1</strong>', list_item_text)
            html_output.append(f'<li class="payload-li">{list_item_text}</li>')
            
        else:
            if in_list:
                html_output.append('</ul>')
                in_list = False
            if cleaned_line and not cleaned_line.startswith('```'):
                cleaned_line = re.sub(r'\*\frac_macro(.*_macro?)\*\*', r'<strong class="payload-strong">\1</strong>', cleaned_line)
                cleaned_line = re.sub(r'\*\*(.*?)\*\*', r'<strong class="payload-strong">\1</strong>', cleaned_line)
                html_output.append(f'<p class="payload-p">{cleaned_line}</p>')
                
    if in_list:
        html_output.append('</ul>')
        
    return '\n'.join(html_output)

@app.route('/')
def interface_index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def process_document_pipeline():
    if 'file' not in request.files:
        return jsonify({'error': 'No file stream found.'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected.'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        destination_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(destination_path)
        
        # 1. Extract text strictly locally
        raw_document_corpus = parse_pdf_document(destination_path)
        
        # If PDF is scanned and has zero text layer, give a clean user error instead of crashing
        if not raw_document_corpus or len(raw_document_corpus.strip()) < 10:
            return jsonify({'error': 'This PDF seems to be a scanned image or empty. Please upload a digital text-based PDF.'}), 422
            
        api_key_payload = os.getenv("GEMINI_API_KEY")
        if not api_key_payload:
            return jsonify({'error': 'API Key is missing in .env file.'}), 500
            
        try:
            # 2. Straightforward Standard Text Generation Endpoint
            execution_url = f"[https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=](https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=){api_key_payload}"
            headers_configuration = {"Content-Type": "application/json"}
            
            payload_payload = {
                "contents": [{
                    "parts": [{
                        "text": f"Analyze this unstructured document text and provide a highly clean structured summary report with bold key sections and clear bullet points:\n\n{raw_document_corpus}"
                    }]
                }]
            }
            
            network_response = requests.post(execution_url, headers=headers_configuration, json=payload_payload)
            response_json_object = network_response.json()
            
            if network_response.status_code != 200:
                raise Exception(response_json_object.get('error', {}).get('message', 'Google API Service Core Fault'))
                
            raw_markdown = response_json_object['candidates'][0]['content']['parts'][0]['text']
            html_formatted_payload = convert_markdown_to_clean_html(raw_markdown)
            
            return jsonify({
                'filename': filename,
                'status': 'Success',
                'analysis_payload': html_formatted_payload
            }), 200
            
        except Exception as system_pipeline_exception:
            print(f"[Fatal Engine Error]: {str(system_pipeline_exception)}")
            return jsonify({'error': str(system_pipeline_exception)}), 500
    else:
        return jsonify({'error': 'Unsupported file format.'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)