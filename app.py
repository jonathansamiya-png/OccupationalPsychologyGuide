from flask import Flask, render_template, jsonify, request
import json
from data import get_guide_content

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def home():
    """דף הבית - סקירה כללית על המדריך"""
    return render_template('index.html')

@app.route('/modules')
def modules():
    """דף המודולים - רשימת כל המודולים"""
    content = get_guide_content()
    return render_template('modules.html', modules=content['modules'])

@app.route('/module/<int:module_id>')
def module_detail(module_id):
    """דף פרטי של מודול"""
    content = get_guide_content()
    for module in content['modules']:
        if module['id'] == module_id:
            return render_template('module_detail.html', module=module)
    return "Module not found", 404

@app.route('/api/modules')
def api_modules():
    """API לקבלת רשימת כל המודולים"""
    content = get_guide_content()
    return jsonify(content['modules'])

@app.route('/api/module/<int:module_id>')
def api_module_detail(module_id):
    """API לקבלת פרטי מודול ספציפי"""
    content = get_guide_content()
    for module in content['modules']:
        if module['id'] == module_id:
            return jsonify(module)
    return jsonify({'error': 'Module not found'}), 404

@app.route('/about')
def about():
    """דף אודות - מידע על המדריך ומקורות"""
    return render_template('about.html')

@app.route('/requirements')
def requirements():
    """דף דרישות התמחות"""
    return render_template('requirements.html')

@app.route('/search')
def search():
    """חיפוש מושגים במודולים"""
    query = request.args.get('q', '').strip()
    results = []
    if query:
        content = get_guide_content()
        q_lower = query.lower()
        for module in content['modules']:
            matched = False
            snippets = []
            # חיפוש בכותרות ונושאים
            if q_lower in module['title'].lower() or q_lower in module.get('description', '').lower():
                matched = True
                snippets.append(module.get('description', ''))
            for topic in module.get('topics', []):
                if q_lower in topic.get('title', '').lower() or q_lower in topic.get('content', '').lower():
                    matched = True
                    snippets.append(f"{topic.get('title','')}: {topic.get('content','')}")
            for outcome in module.get('learning_outcomes', []):
                if q_lower in outcome.lower():
                    matched = True
                    snippets.append(outcome)
            if matched:
                results.append({
                    'module': module,
                    'snippets': snippets[:3]  # כמה שורות להצגה
                })
    return render_template('search.html', query=query, results=results)

@app.route('/final-exam')
def final_exam():
    """מבחן מסכם"""
    content = get_guide_content()
    questions = content.get('final_exam', [])
    return render_template('final_exam.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
