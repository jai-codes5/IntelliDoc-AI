import os
import re
import time
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

load_dotenv()

app = Flask(__name__)
app.secret_key = "cbit_proddatur_placement_dossier_quantum_engine_2026"

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            level = len(cleaned_line) - len(cleaned_line.lstrip('#'))
            text = cleaned_line.lstrip('#').strip()
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
            
            if level == 1:
                html_output.append(f'<h1 class="text-lg font-bold text-blue-400 mt-4 mb-2 border-b border-slate-800 pb-1 font-mono tracking-wide">{text}</h1>')
            elif level == 2:
                html_output.append(f'<h2 class="text-base font-semibold text-indigo-400 mt-3 mb-1.5">{text}</h2>')
            else:
                html_output.append(f'<h3 class="text-sm font-medium text-slate-200 mt-2">{text}</h3>')
                
        elif cleaned_line.startswith('* ') or cleaned_line.startswith('- '):
            if not in_list:
                html_output.append('<ul class="list-disc list-inside space-y-1.5 text-slate-300 ml-4 mb-3 text-xs leading-relaxed">')
                in_list = True
            item_text = cleaned_line[2:].strip()
            item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-emerald-400 font-semibold">\1</strong>', item_text)
            html_output.append(f'<li>{item_text}</li>')
            
        else:
            if in_list:
                html_output.append('</ul>')
                in_list = False
            if cleaned_line and not cleaned_line.startswith('```'):
                cleaned_line = re.sub(r'\*\frac_placeholder_1\*\*(.*?)\*\*', r'<strong class="text-white font-medium">\1</strong>', cleaned_line)
                html_output.append(f'<p class="text-xs text-slate-300 leading-relaxed mb-2 font-sans">{cleaned_line}</p>')
                
    if in_list:
        html_output.append('</ul>')
        
    return '\n'.join(html_output)

def call_gemini_with_retry(model, contents, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return client.models.generate_content(model=model, contents=contents)
        except APIError as e:
            if e.code == 503 and attempt < retries - 1:
                print(f"⚠️ [503 Alert] Retrying node sequence in {delay}s...")
                time.sleep(delay)
                delay *= 2
            else:
                raise e

@app.route('/')
def interface_index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def process_document_pipeline():
    if client is None:
        return jsonify({'error': 'Client Core Inactive.'}), 500
    if 'file' not in request.files:
        return jsonify({'error': 'Empty payload.'}), 400
        
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Illegal file syntax.'}), 400
        
    filename = secure_filename(file.filename)
    destination_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(destination_path)
    
    file_mime = "application/pdf" if filename.lower().endswith('.pdf') else "text/plain"
    
    try:
        print(f"[Core Operational Flow] Syncing file context block: {filename}")
        native_file_ref = client.files.upload(file=destination_path)
        
        session['active_file_uri'] = native_file_ref.uri
        session['active_file_mime'] = file_mime
        
        prompt = """
        Build an enterprise institutional executive intelligence layout. 
        Extract all operational milestones, institutional KPIs, and placement matrices explicitly.
        """
        
        response = call_gemini_with_retry(model='gemini-2.5-flash', contents=[native_file_ref, prompt])
        html_formatted_payload = convert_markdown_to_clean_html(response.text)
        
        return jsonify({'status': 'Success', 'analysis_payload': html_formatted_payload}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def document_intelligence_chat():
    user_query = request.json.get('query')
    file_uri = session.get('active_file_uri')
    file_mime = session.get('active_file_mime')
    
    if not user_query or not file_uri or not file_mime:
        return jsonify({'error': 'Execution Context is missing file binding tokens.'}), 400
        
    try:
        print(f"[Vector Engine Search] Target query intercept: '{user_query}'")
        file_part = types.Part.from_uri(file_uri=file_uri, mime_type=file_mime)
        
        rag_prompt = f"""
        Act as an Advanced Campus Intelligence Bot. Using the document provided, directly and comprehensively answer the user search question: '{user_query}'.
        Do not output markdown code blocks. Highlight figures or core packages using bold tags.
        """
        
        response = call_gemini_with_retry(model='gemini-2.5-flash', contents=[file_part, rag_prompt])
        clean_search_reply = convert_markdown_to_clean_html(response.text)
        return jsonify({'reply': clean_search_reply}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)