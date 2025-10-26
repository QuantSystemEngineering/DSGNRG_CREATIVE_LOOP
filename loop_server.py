#!/usr/bin/env python3
"""
DSGNRG Creative Loop Web Server
Flask server to serve the dashboard and provide API endpoints
"""

from flask import Flask, jsonify, render_template_string, request, send_file
from flask_cors import CORS
import json
import datetime
from pathlib import Path
from creative_loop_agent import CreativeLoopAgent

app = Flask(__name__)
CORS(app)

# Initialize the creative loop agent
agent = CreativeLoopAgent()

@app.route('/')
def dashboard():
    """Serve the dashboard HTML"""
    dashboard_path = Path(__file__).parent / 'dashboard.html'
    return send_file(dashboard_path)

@app.route('/api/status/daily')
def daily_status():
    """Get daily completion status"""
    return jsonify(agent.get_daily_completion_status())

@app.route('/api/input/today')
def get_today_inputs():
    """Get today's input data for editing"""
    today = datetime.date.today().isoformat()
    inputs_data = agent._load_data(agent.inputs_file)
    today_data = inputs_data.get(today, {})
    return jsonify({
        "date": today,
        "sonic_sketch": today_data.get("sonic_sketch"),
        "visual_moodboard": today_data.get("visual_moodboard"), 
        "lore_fragment": today_data.get("lore_fragment")
    })

@app.route('/api/status/weekly')
def weekly_status():
    """Get weekly progress"""
    return jsonify(agent.get_weekly_progress())

@app.route('/api/status/monthly')
def monthly_status():
    """Get monthly progress"""
    return jsonify(agent.get_monthly_progress())

@app.route('/api/stats')
def stats():
    """Get creative statistics"""
    return jsonify(agent.get_creative_stats())

@app.route('/api/report')
def report():
    """Get full creative report"""
    return jsonify({"report": agent.generate_creative_report()})

# Input endpoints
@app.route('/api/input/sketch', methods=['POST'])
def log_sketch():
    """Log sonic sketch"""
    data = request.json
    try:
        timestamp = agent.log_sonic_sketch(
            data['duration'],
            data['description'],
            data.get('audio_file'),
            data.get('tags', [])
        )
        return jsonify({"success": True, "timestamp": timestamp})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/input/visual', methods=['POST'])
def log_visual():
    """Log visual moodboard"""
    data = request.json
    try:
        timestamp = agent.log_visual_moodboard(
            data['images'],
            data['theme'],
            data.get('color_palette', [])
        )
        return jsonify({"success": True, "timestamp": timestamp})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/input/lore', methods=['POST'])
def log_lore():
    """Log lore fragment"""
    data = request.json
    try:
        timestamp = agent.log_lore_fragment(
            data['character'],
            data['fragment'],
            data['narrative_arc'],
            data.get('world_building_elements', [])
        )
        return jsonify({"success": True, "timestamp": timestamp})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/process', methods=['POST'])
def log_process():
    """Log creative process"""
    data = request.json
    try:
        process_id = agent.log_creative_process(
            data['sample_source'],
            data['remix_approach'],
            data['render_format'],
            data['emotion_tag'],
            data.get('tempo'),
            data.get('lore_arc_connection', '')
        )
        return jsonify({"success": True, "process_id": process_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/output/micro', methods=['POST'])
def log_micro_output():
    """Log micro release"""
    data = request.json
    try:
        output_id = agent.log_micro_release(
            data['title'],
            data['category'],
            data.get('file_path'),
            data.get('description', ''),
            data.get('tags', [])
        )
        return jsonify({"success": True, "output_id": output_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/output/major', methods=['POST'])
def log_major_output():
    """Log major release"""
    data = request.json
    try:
        output_id = agent.log_major_release(
            data['title'],
            data['category'],
            data.get('file_path'),
            data.get('description', ''),
            data.get('tags', [])
        )
        return jsonify({"success": True, "output_id": output_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/output/vst3', methods=['POST'])
def log_vst3():
    """Log VST3 plugin development"""
    data = request.json
    try:
        output_id = agent.log_vst3_plugin(
            data['title'],
            data.get('file_path'),
            data.get('description', ''),
            data.get('tags', [])
        )
        return jsonify({"success": True, "output_id": output_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/output/vst3/<plugin_id>', methods=['PUT'])
def edit_vst3(plugin_id):
    """Edit VST3 plugin"""
    data = request.json
    try:
        success = agent.edit_vst3_plugin(
            plugin_id,
            data.get('title'),
            data.get('file_path'),
            data.get('description'),
            data.get('tags')
        )
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/output/vst3', methods=['GET'])
def list_vst3():
    """List all VST3 plugins"""
    try:
        plugins = agent.list_vst3_plugins()
        return jsonify({"success": True, "plugins": plugins})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/data/all')
def get_all_data():
    """Get all data for dashboard"""
    try:
        return jsonify({
            "daily": agent.get_daily_completion_status(),
            "weekly": agent.get_weekly_progress(),
            "monthly": agent.get_monthly_progress(),
            "stats": agent.get_creative_stats()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/calendar/<int:year>/<int:month>')
def get_calendar(year, month):
    """Get calendar data for a specific month"""
    try:
        calendar_data = agent.get_calendar_data(year, month)
        return jsonify({"success": True, "calendar": calendar_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/calendar/day/<date>')
def get_day_activities(date):
    """Get activities for a specific day"""
    try:
        activities = agent.get_day_activities(date)
        return jsonify({"success": True, "activities": activities})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    print("🔁 Starting DSGNRG Creative Loop Server...")
    print("Dashboard will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)