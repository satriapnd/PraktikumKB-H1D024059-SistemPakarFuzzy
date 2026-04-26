from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import fuzzy_engine
import expert_engine

app = Flask(__name__)
CORS(app)

# --- ROUTES FOR HTML PAGES ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fuzzy')
def fuzzy():
    return render_template('fuzzy.html')

@app.route('/expert')
def expert():
    return render_template('expert.html')

# --- API ENDPOINTS ---
@app.route('/api/fuzzy', methods=['POST'])
def api_fuzzy():
    data = request.json
    try:
        lvr = float(data.get('lvr', 0))
        cvr = float(data.get('cvr', 0))
        arr = float(data.get('arr', 0))
        sharing = float(data.get('sharing', 0))
        
        score, status = fuzzy_engine.evaluate_loyalty(lvr, cvr, arr, sharing)
        
        return jsonify({
            'success': True,
            'score': score,
            'status': status
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/expert', methods=['POST'])
def api_expert():
    data = request.json
    try:
        loyalty_status = data.get('loyalty_status', 'Aktif')
        category = data.get('category', 'lainnya')
        subscriber_tier = data.get('subscriber_tier', 'micro')
        violation_history = data.get('violation_history', 'bersih')
        age_demo = data.get('age_demo', '18-24')
        upload_freq = data.get('upload_freq', 'rutin')
        
        result = expert_engine.evaluate_sponsorship(
            loyalty_status, category, subscriber_tier, violation_history, age_demo, upload_freq
        )
        
        # Format currency
        def format_rupiah(amount):
            return f"Rp {amount:,.0f}".replace(',', '.')
            
        result['formatted_value'] = format_rupiah(result['estimated_value'])
        result['success'] = True
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
