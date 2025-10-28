#!/usr/bin/env python3
"""
DSGNRG Creative Loop Web Server
Flask server to serve the dashboard and provide API endpoints
"""

from flask import Flask, jsonify, render_template_string, request, send_file, send_from_directory
from flask_cors import CORS
import json
import datetime
import os
import shutil
from pathlib import Path
from werkzeug.utils import secure_filename
from creative_loop_agent import CreativeLoopAgent
import quotes

app = Flask(__name__)
CORS(app)

def get_date_folder(base_dir, date_str=None):
    """Create and return date-specific folder path"""
    if date_str is None:
        date_str = datetime.date.today().isoformat()
    
    date_folder = Path(base_dir) / date_str
    date_folder.mkdir(parents=True, exist_ok=True)
    return date_folder

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
    """Log sonic sketch with file upload"""
    try:
        duration = int(request.form.get('duration', 30))
        description = request.form.get('description', '')
        tags_str = request.form.get('tags', '')
        
        # Parse tags
        tags = []
        if tags_str:
            tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        
        # Handle audio file upload
        audio_filename = None
        existing_audio = request.form.get('existing_audio', '')
        # Allow client to specify a target date (for editing past days)
        date_str = request.form.get('date', None)
        if not date_str:
            date_str = datetime.date.today().isoformat()
        
        # Check if new audio file uploaded
        if 'audio_file' in request.files:
            file = request.files['audio_file']
            if file and file.filename:
                # Create date-specific audio directory
                audio_dir = get_date_folder('loop_data/audio', date_str)
                
                # Secure filename and save
                filename = secure_filename(file.filename)
                timestamp = datetime.datetime.now().strftime('%H%M%S')  # Just time since date is in folder
                unique_filename = f"{timestamp}_{filename}"
                filepath = audio_dir / unique_filename
                
                file.save(str(filepath))
                # Store relative path including date folder for retrieval
                audio_filename = f"{date_str}/{unique_filename}"
        elif existing_audio:
            # Keep existing audio file
            audio_filename = existing_audio
        
        timestamp = agent.log_sonic_sketch(
            duration,
            description,
            audio_filename,
            tags,
            date_str
        )
        return jsonify({"success": True, "timestamp": timestamp})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/input/visual', methods=['POST'])
def log_visual():
    """Log visual moodboard with file uploads"""
    try:
        theme = request.form.get('theme', '')
        color_palette_str = request.form.get('color_palette', '')
        
        # Parse color palette
        color_palette = []
        if color_palette_str:
            color_palette = [c.strip() for c in color_palette_str.split(',') if c.strip()]
        
        # Start with existing images if provided
        image_filenames = []
        existing_images_str = request.form.get('existing_images', '')
        if existing_images_str:
            try:
                existing_images = json.loads(existing_images_str)
                image_filenames.extend(existing_images)
            except json.JSONDecodeError:
                pass  # Ignore invalid JSON, will just use new images
        
        # Handle newly uploaded image files
        uploaded_files = request.files.getlist('images')
        
        # Create date-specific images directory
        today = datetime.date.today().isoformat()
        images_dir = get_date_folder('loop_data/images', today)
        
        # Save newly uploaded files
        for file in uploaded_files:
            if file and file.filename:
                # Secure filename and save
                filename = secure_filename(file.filename)
                timestamp = datetime.datetime.now().strftime('%H%M%S')
                unique_filename = f"{timestamp}_{filename}"
                filepath = images_dir / unique_filename
                
                file.save(str(filepath))
                # Store relative path including date folder for retrieval
                image_filenames.append(f"{today}/{unique_filename}")
        
        # Log the visual moodboard
        timestamp = agent.log_visual_moodboard(
            image_filenames,
            theme,
            color_palette
        )
        
        return jsonify({
            "success": True, 
            "timestamp": timestamp,
            "saved_images": len(image_filenames)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/images/<path:filename>')
def serve_image(filename):
    """Serve uploaded images (supports date-specific paths like 2025-10-27/image.jpg)"""
    try:
        images_dir = Path('loop_data/images')
        # Handle both old flat structure and new date-organized structure
        if '/' in filename:
            # New format: date/filename
            return send_from_directory(str(images_dir), filename)
        else:
            # Old format: filename only - check current date first, then fall back to flat
            today = datetime.date.today().isoformat()
            date_specific_path = images_dir / today / filename
            if date_specific_path.exists():
                return send_from_directory(str(images_dir / today), filename)
            else:
                # Fall back to flat directory for old files
                return send_from_directory(str(images_dir), filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/api/audio/<path:filename>')
def serve_audio(filename):
    """Serve uploaded audio files (supports date-specific paths like 2025-10-27/audio.mp3)"""
    try:
        audio_dir = Path('loop_data/audio')
        # Handle both old flat structure and new date-organized structure
        if '/' in filename:
            # New format: date/filename
            return send_from_directory(str(audio_dir), filename)
        else:
            # Old format: filename only - check current date first, then fall back to flat
            today = datetime.date.today().isoformat()
            date_specific_path = audio_dir / today / filename
            if date_specific_path.exists():
                return send_from_directory(str(audio_dir / today), filename)
            else:
                # Fall back to flat directory for old files
                return send_from_directory(str(audio_dir), filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

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

# Task Management API Endpoints
@app.route('/api/tasks/<task_type>')
def get_tasks(task_type):
    """Get all tasks for a specific type (weekly/monthly)"""
    try:
        tasks = agent.get_tasks(task_type)
        return jsonify({"success": True, "tasks": tasks})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/tasks/<task_type>', methods=['POST'])
def add_task(task_type):
    """Add a new task"""
    try:
        data = request.json
        task = agent.add_task(task_type, data['text'], data.get('priority', 'medium'))
        return jsonify({"success": True, "task": task})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/tasks/<task_type>/<task_id>', methods=['PUT'])
def update_task(task_type, task_id):
    """Update a task (toggle completion or edit text)"""
    try:
        data = request.json
        task = agent.update_task(task_type, task_id, data)
        return jsonify({"success": True, "task": task})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/tasks/<task_type>/<task_id>', methods=['DELETE'])
def delete_task(task_type, task_id):
    """Delete a task"""
    try:
        agent.delete_task(task_type, task_id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# Payment Management Endpoints
@app.route('/api/payments')
def get_payments():
    """Get all payments"""
    try:
        payments = agent.get_payments()
        return jsonify({"success": True, "payments": payments})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/payments', methods=['POST'])
def add_payment():
    """Add a new payment"""
    try:
        data = request.json
        payment_id = agent.add_payment(
            data['name'],
            data['amount'], 
            data['category'],
            data.get('notes', '')
        )
        return jsonify({"success": True, "payment_id": payment_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/payments/<payment_id>', methods=['PUT'])
def update_payment(payment_id):
    """Update a payment"""
    try:
        data = request.json
        agent.update_payment(
            payment_id,
            data['name'],
            data['amount'],
            data['category'], 
            data.get('notes', '')
        )
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/payments/<payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    """Delete a payment"""
    try:
        agent.delete_payment(payment_id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/quote')
def get_motivational_quote():
    """Get a random motivational quote"""
    try:
        # Try using quotes library
        import quotes
        q = quotes.Quotes()
        quote_data = q.random()
        # quote_data is a tuple: (category, quote_text)
        return jsonify({
            "success": True,
            "quote": quote_data[1],  # The actual quote text
            "author": quote_data[0]  # Use category as "author" for now
        })
    except Exception:
        # Fallback quotes if library not available
        fallback_quotes = [
            ("The way to get started is to quit talking and begin doing.", "Walt Disney"),
            ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
            ("Life is what happens to you while you're busy making other plans.", "John Lennon"),
            ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
            ("Your limitation—it's only your imagination.", "Unknown"),
            ("Great things never come from comfort zones.", "Unknown"),
            ("Dream it. Believe it. Build it.", "Unknown"),
            ("Success doesn't just find you. You have to go out and get it.", "Unknown"),
            ("The harder you work for something, the greater you'll feel when you achieve it.", "Unknown"),
            ("Don't stop when you're tired. Stop when you're done.", "Unknown")
        ]
        import random
        quote_data = random.choice(fallback_quotes)
        return jsonify({
            "success": True,
            "quote": quote_data[0],
            "author": quote_data[1]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/calendar/<int:year>/<int:month>')
def get_calendar_data(year, month):
    """Get calendar data for a specific year and month"""
    try:
        # Load calendar data from file
        calendar_data = agent._load_data(agent.calendar_file)
        
        # Get data for the requested year-month
        year_key = str(year)
        month_key = str(month).zfill(2)  # Pad with zeros (e.g., "01", "02")
        
        month_data = {}
        if year_key in calendar_data:
            # Look for both padded and unpadded month keys
            if month_key in calendar_data[year_key]:
                month_data = calendar_data[year_key][month_key]
            elif str(month) in calendar_data[year_key]:
                month_data = calendar_data[year_key][str(month)]
        
        return jsonify({
            "success": True,
            "year": year,
            "month": month,
            "calendar": month_data
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/calendar/<int:year>/<int:month>/<int:day>')
def get_day_data(year, month, day):
    """Get detailed data for a specific day"""
    try:
        # Load calendar data
        calendar_data = agent._load_data(agent.calendar_file)
        
        # Get data for the requested date
        year_key = str(year)
        month_key = str(month).zfill(2)
        day_key = str(day).zfill(2)
        
        day_data = {}
        if year_key in calendar_data:
            month_data = calendar_data[year_key].get(month_key) or calendar_data[year_key].get(str(month), {})
            day_data = month_data.get(day_key) or month_data.get(str(day), {})
        
        # Also load inputs data for the specific date
        inputs_data = agent._load_data(agent.inputs_file)
        date_key = f"{year}-{month_key}-{day_key}"
        input_data = inputs_data.get(date_key, {})
        
        # Combine calendar and input data
        combined_data = {
            "date": date_key,
            "calendar_data": day_data,
            "input_data": input_data,
            "sonic_sketch": input_data.get("sonic_sketch"),
            "visual_moodboard": input_data.get("visual_moodboard"),
            "lore_fragment": input_data.get("lore_fragment")
        }
        
        return jsonify({
            "success": True,
            "date": date_key,
            "data": combined_data
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# Document Management API Endpoints
@app.route('/api/list_documents')
def list_documents():
    """List all available documents"""
    try:
        documents_dir = Path('loop_data/documents')
        documents_dir.mkdir(parents=True, exist_ok=True)
        
        # Get all .txt files in the documents directory
        documents = []
        for file_path in documents_dir.glob('*.txt'):
            documents.append(file_path.name)
        
        documents.sort()  # Sort alphabetically
        
        return jsonify({
            "success": True,
            "documents": documents
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/load_document', methods=['POST'])
def load_document():
    """Load a specific document"""
    try:
        data = request.json
        filename = data.get('filename')
        
        if not filename:
            return jsonify({"success": False, "error": "Filename is required"}), 400
        
        # Secure the filename
        secure_name = secure_filename(filename)
        documents_dir = Path('loop_data/documents')
        file_path = documents_dir / secure_name
        
        if not file_path.exists():
            return jsonify({"success": False, "error": "Document not found"}), 404
        
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            "success": True,
            "filename": filename,
            "content": content
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/save_document', methods=['POST'])
def save_document():
    """Save a document"""
    try:
        data = request.json
        filename = data.get('filename')
        content = data.get('content', '')
        
        if not filename:
            return jsonify({"success": False, "error": "Filename is required"}), 400
        
        # Secure the filename and ensure .txt extension
        secure_name = secure_filename(filename)
        if not secure_name.endswith('.txt'):
            secure_name += '.txt'
        
        documents_dir = Path('loop_data/documents')
        documents_dir.mkdir(parents=True, exist_ok=True)
        file_path = documents_dir / secure_name
        
        # Write the file content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return jsonify({
            "success": True,
            "filename": secure_name,
            "message": f"Document '{secure_name}' saved successfully"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/delete_document', methods=['POST'])
def delete_document():
    """Delete a document"""
    try:
        data = request.json
        filename = data.get('filename')
        
        if not filename:
            return jsonify({"success": False, "error": "Filename is required"}), 400
        
        # Secure the filename
        secure_name = secure_filename(filename)
        documents_dir = Path('loop_data/documents')
        file_path = documents_dir / secure_name
        
        if not file_path.exists():
            return jsonify({"success": False, "error": "Document not found"}), 404
        
        # Delete the file
        file_path.unlink()
        
        return jsonify({
            "success": True,
            "filename": secure_name,
            "message": f"Document '{secure_name}' deleted successfully"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    print("🔁 Starting DSGNRG Creative Loop Server...")
    print("Dashboard will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)