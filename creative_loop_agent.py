#!/usr/bin/env python3
"""
DSGNRG Creative Loop Agent
A modular system to track and maintain creative consistency as an artist/producer/DJ
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

class CreativePhase(Enum):
    INPUT = "input"
    PROCESS = "process"
    OUTPUT = "output"

class OutputType(Enum):
    MICRO = "micro"  # weekly
    MAJOR = "major"  # monthly
    VST3 = "vst3"    # weekly (4 per month)

@dataclass
class SonicSketch:
    duration_minutes: int
    description: str
    audio_file: Optional[str] = None
    tags: List[str] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.datetime.now().isoformat()
        if self.tags is None:
            self.tags = []

@dataclass
class VisualMoodboard:
    images: List[str]  # file paths or URLs
    theme: str
    color_palette: List[str] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.datetime.now().isoformat()
        if self.color_palette is None:
            self.color_palette = []

@dataclass
class LoreFragment:
    character: str
    fragment: str
    narrative_arc: str
    world_building_elements: List[str] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.datetime.now().isoformat()
        if self.world_building_elements is None:
            self.world_building_elements = []

@dataclass
class CreativeInput:
    date: str
    sonic_sketch: Optional[SonicSketch] = None
    visual_moodboard: Optional[VisualMoodboard] = None
    lore_fragment: Optional[LoreFragment] = None
    
    def is_complete(self) -> bool:
        return all([self.sonic_sketch, self.visual_moodboard, self.lore_fragment])

@dataclass
class CreativeProcess:
    sample_source: str
    remix_approach: str
    render_format: str
    emotion_tag: str
    tempo: Optional[int] = None
    lore_arc_connection: str = ""
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.datetime.now().isoformat()

@dataclass
class CreativeOutput:
    title: str
    output_type: OutputType
    category: str  # beat, visual, lore drop, track, video, plugin
    file_path: Optional[str] = None
    description: str = ""
    release_date: str = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.release_date is None:
            self.release_date = datetime.datetime.now().isoformat()
        if self.tags is None:
            self.tags = []

class CreativeLoopAgent:
    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path) if workspace_path else Path.cwd()
        self.data_dir = self.workspace_path / "loop_data"
        self.data_dir.mkdir(exist_ok=True)
        
        # Data storage files
        self.inputs_file = self.data_dir / "inputs.json"
        self.processes_file = self.data_dir / "processes.json"
        self.outputs_file = self.data_dir / "outputs.json"
        self.stats_file = self.data_dir / "stats.json"
        self.calendar_file = self.data_dir / "calendar.json"
        
        self._initialize_data_files()
    
    def _initialize_data_files(self):
        """Initialize JSON data files if they don't exist"""
        for file_path in [self.inputs_file, self.processes_file, self.outputs_file, self.stats_file, self.calendar_file]:
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    json.dump({}, f)
    
    def _load_data(self, file_path: Path) -> Dict:
        """Load data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_data(self, file_path: Path, data: Dict):
        """Save data to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    # INPUT METHODS
    def log_sonic_sketch(self, duration_minutes: int, description: str, 
                        audio_file: str = None, tags: List[str] = None, date: str = None) -> str:
        """Log a daily sonic sketch"""
        sketch = SonicSketch(duration_minutes, description, audio_file, tags or [])
        # Allow logging for a specific date (YYYY-MM-DD) when provided, otherwise use today
        if date:
            today = date
        else:
            today = datetime.date.today().isoformat()
        
        inputs = self._load_data(self.inputs_file)
        if today not in inputs:
            inputs[today] = asdict(CreativeInput(today))
        
        inputs[today]["sonic_sketch"] = asdict(sketch)
        self._save_data(self.inputs_file, inputs)
        
        # Update calendar
        self.update_calendar_entry(
            today, "inputs", 
            {"type": "sonic_sketch", "duration": duration_minutes, "description": description}
        )
        
        print(f"✅ Sonic sketch logged for {today}")
        return sketch.timestamp
    
    def log_visual_moodboard(self, images: List[str], theme: str, 
                           color_palette: List[str] = None) -> str:
        """Log visual moodboard (5 images recommended)"""
        moodboard = VisualMoodboard(images, theme, color_palette or [])
        today = datetime.date.today().isoformat()
        
        inputs = self._load_data(self.inputs_file)
        if today not in inputs:
            inputs[today] = asdict(CreativeInput(today))
        
        inputs[today]["visual_moodboard"] = asdict(moodboard)
        self._save_data(self.inputs_file, inputs)
        
        print(f"✅ Visual moodboard logged for {today}")
        return moodboard.timestamp
    
    def log_lore_fragment(self, character: str, fragment: str, narrative_arc: str,
                         world_building_elements: List[str] = None) -> str:
        """Log a lore fragment or character riff"""
        lore = LoreFragment(character, fragment, narrative_arc, world_building_elements or [])
        today = datetime.date.today().isoformat()
        
        inputs = self._load_data(self.inputs_file)
        if today not in inputs:
            inputs[today] = asdict(CreativeInput(today))
        
        inputs[today]["lore_fragment"] = asdict(lore)
        self._save_data(self.inputs_file, inputs)
        
        print(f"✅ Lore fragment logged for {today}")
        return lore.timestamp
    
    # PROCESS METHODS
    def log_creative_process(self, sample_source: str, remix_approach: str, 
                           render_format: str, emotion_tag: str, 
                           tempo: int = None, lore_arc_connection: str = "") -> str:
        """Log the creative process: Sample → Remix → Render"""
        process = CreativeProcess(
            sample_source, remix_approach, render_format, 
            emotion_tag, tempo, lore_arc_connection
        )
        
        processes = self._load_data(self.processes_file)
        process_id = f"proc_{len(processes) + 1}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        processes[process_id] = asdict(process)
        self._save_data(self.processes_file, processes)
        
        print(f"✅ Creative process logged: {process_id}")
        return process_id
    
    # OUTPUT METHODS
    def log_micro_release(self, title: str, category: str, file_path: str = None,
                         description: str = "", tags: List[str] = None) -> str:
        """Log a micro-release (weekly): beat, visual, or lore drop"""
        output = CreativeOutput(
            title, OutputType.MICRO, category, file_path, description, tags=tags or []
        )
        
        outputs = self._load_data(self.outputs_file)
        output_dict = asdict(output)
        output_dict['output_type'] = output.output_type.value  # Convert enum to string value
        output_id = f"micro_{len([o for o in outputs.values() if o.get('output_type') == 'micro']) + 1}"
        outputs[output_id] = output_dict
        self._save_data(self.outputs_file, outputs)
        
        print(f"✅ Micro-release logged: {title}")
        return output_id
    
    def log_major_release(self, title: str, category: str, file_path: str = None,
                         description: str = "", tags: List[str] = None) -> str:
        """Log a major release (monthly): track, video, or plugin"""
        output = CreativeOutput(
            title, OutputType.MAJOR, category, file_path, description, tags=tags or []
        )
        
        outputs = self._load_data(self.outputs_file)
        output_dict = asdict(output)
        output_dict['output_type'] = output.output_type.value  # Convert enum to string value
        output_id = f"major_{len([o for o in outputs.values() if o.get('output_type') == 'major']) + 1}"
        outputs[output_id] = output_dict
        self._save_data(self.outputs_file, outputs)
        
        print(f"✅ Major release logged: {title}")
        return output_id
    
    def log_vst3_plugin(self, title: str, file_path: str = None,
                       description: str = "", tags: List[str] = None) -> str:
        """Log a VST3 plugin (weekly): 1 per week, 4 per month"""
        output = CreativeOutput(
            title, OutputType.VST3, "plugin", file_path, description, tags=tags or []
        )
        
        outputs = self._load_data(self.outputs_file)
        output_dict = asdict(output)
        output_dict['output_type'] = output.output_type.value  # Convert enum to string value
        output_id = f"vst3_{len([o for o in outputs.values() if o.get('output_type') == 'vst3']) + 1}"
        outputs[output_id] = output_dict
        self._save_data(self.outputs_file, outputs)
        
        # Update calendar
        today = datetime.date.today().isoformat()
        self.update_calendar_entry(
            today, "outputs", 
            {"type": "vst3", "title": title, "description": description}
        )
        
        print(f"✅ VST3 plugin logged: {title}")
        return output_id
    
    def edit_vst3_plugin(self, plugin_id: str, title: str = None, file_path: str = None,
                         description: str = None, tags: List[str] = None) -> bool:
        """Edit an existing VST3 plugin entry"""
        outputs = self._load_data(self.outputs_file)
        
        if plugin_id not in outputs:
            print(f"❌ VST3 plugin '{plugin_id}' not found")
            return False
            
        if outputs[plugin_id].get("output_type") != "vst3":
            print(f"❌ '{plugin_id}' is not a VST3 plugin")
            return False
        
        # Update only provided fields
        if title is not None:
            outputs[plugin_id]["title"] = title
        if file_path is not None:
            outputs[plugin_id]["file_path"] = file_path
        if description is not None:
            outputs[plugin_id]["description"] = description
        if tags is not None:
            outputs[plugin_id]["tags"] = tags
            
        # Update modified date
        outputs[plugin_id]["modified_date"] = datetime.datetime.now().isoformat()
        
        self._save_data(self.outputs_file, outputs)
        print(f"✅ VST3 plugin '{plugin_id}' updated")
        return True
    
    def list_vst3_plugins(self) -> List[Dict]:
        """List all VST3 plugins"""
        outputs = self._load_data(self.outputs_file)
        vst3_plugins = []
        
        for plugin_id, data in outputs.items():
            if data.get("output_type") == "vst3":
                vst3_plugins.append({
                    "id": plugin_id,
                    "title": data["title"],
                    "description": data["description"],
                    "file_path": data.get("file_path"),
                    "release_date": data["release_date"],
                    "tags": data.get("tags", [])
                })
        
        return sorted(vst3_plugins, key=lambda x: x["release_date"], reverse=True)
    
    # CALENDAR TRACKING
    def get_calendar_data(self, year: int = None, month: int = None) -> Dict:
        """Get calendar data for a specific month/year"""
        if year is None:
            year = datetime.date.today().year
        if month is None:
            month = datetime.date.today().month
            
        calendar_data = self._load_data(self.calendar_file)
        month_key = f"{year}-{month:02d}"
        
        if month_key not in calendar_data:
            calendar_data[month_key] = {}
            
        return calendar_data.get(month_key, {})
    
    def update_calendar_entry(self, date: str, activity_type: str, activity_data: Dict) -> None:
        """Update calendar entry for a specific date"""
        calendar_data = self._load_data(self.calendar_file)
        
        # Parse date to extract year-month
        date_obj = datetime.datetime.fromisoformat(date.replace('Z', '+00:00') if 'Z' in date else date)
        month_key = f"{date_obj.year}-{date_obj.month:02d}"
        day_key = f"{date_obj.day:02d}"
        
        if month_key not in calendar_data:
            calendar_data[month_key] = {}
        if day_key not in calendar_data[month_key]:
            calendar_data[month_key][day_key] = {}
        if activity_type not in calendar_data[month_key][day_key]:
            calendar_data[month_key][day_key][activity_type] = []
            
        calendar_data[month_key][day_key][activity_type].append(activity_data)
        self._save_data(self.calendar_file, calendar_data)
    
    def get_day_activities(self, date: str) -> Dict:
        """Get all activities for a specific day"""
        date_obj = datetime.datetime.fromisoformat(date.replace('Z', '+00:00') if 'Z' in date else date)
        month_key = f"{date_obj.year}-{date_obj.month:02d}"
        day_key = f"{date_obj.day:02d}"
        
        calendar_data = self._load_data(self.calendar_file)
        return calendar_data.get(month_key, {}).get(day_key, {})
    
    # ANALYTICS & TRACKING
    def get_daily_completion_status(self, date: str = None) -> Dict:
        """Check if daily creative input loop is complete"""
        if date is None:
            date = datetime.date.today().isoformat()
        
        inputs = self._load_data(self.inputs_file)
        day_input = inputs.get(date, {})
        
        return {
            "date": date,
            "sonic_sketch_complete": day_input.get("sonic_sketch") is not None,
            "visual_moodboard_complete": day_input.get("visual_moodboard") is not None,
            "lore_fragment_complete": day_input.get("lore_fragment") is not None,
            "daily_loop_complete": all([
                day_input.get("sonic_sketch"),
                day_input.get("visual_moodboard"),
                day_input.get("lore_fragment")
            ])
        }
    
    def get_weekly_progress(self) -> Dict:
        """Check weekly micro-release and VST3 plugin progress"""
        today = datetime.date.today()
        week_start = today - datetime.timedelta(days=today.weekday())
        
        outputs = self._load_data(self.outputs_file)
        this_week_micros = []
        this_week_vst3 = []
        
        for output_id, output_data in outputs.items():
            release_date = datetime.datetime.fromisoformat(output_data["release_date"]).date()
            if release_date >= week_start:
                if output_data.get("output_type") == "micro":
                    this_week_micros.append(output_data)
                elif output_data.get("output_type") == "vst3":
                    this_week_vst3.append(output_data)
        
        return {
            "week_start": week_start.isoformat(),
            "micro_releases_this_week": len(this_week_micros),
            "vst3_plugins_this_week": len(this_week_vst3),
            "target_micro_releases": 1,
            "target_vst3_plugins": 1,
            "weekly_goal_met": len(this_week_micros) >= 1 and len(this_week_vst3) >= 1,
            "micro_releases": this_week_micros,
            "vst3_plugins": this_week_vst3
        }
    
    def get_monthly_progress(self) -> Dict:
        """Check monthly major release and VST3 plugin progress"""
        today = datetime.date.today()
        month_start = today.replace(day=1)
        
        outputs = self._load_data(self.outputs_file)
        this_month_majors = []
        this_month_vst3 = []
        
        for output_id, output_data in outputs.items():
            release_date = datetime.datetime.fromisoformat(output_data["release_date"]).date()
            if release_date >= month_start:
                if output_data.get("output_type") == "major":
                    this_month_majors.append(output_data)
                elif output_data.get("output_type") == "vst3":
                    this_month_vst3.append(output_data)
        
        return {
            "month_start": month_start.isoformat(),
            "major_releases_this_month": len(this_month_majors),
            "vst3_plugins_this_month": len(this_month_vst3),
            "target_major_releases": 1,
            "target_vst3_plugins": 4,
            "monthly_goal_met": len(this_month_majors) >= 1 and len(this_month_vst3) >= 4,
            "major_releases": this_month_majors,
            "vst3_plugins": this_month_vst3
        }
    
    def generate_creative_report(self) -> str:
        """Generate a comprehensive creative loop report"""
        daily_status = self.get_daily_completion_status()
        weekly_progress = self.get_weekly_progress()
        monthly_progress = self.get_monthly_progress()
        
        report = f"""
🔁 DSGNRG CREATIVE LOOP REPORT
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📅 TODAY'S INPUT LOOP ({daily_status['date']})
{'✅' if daily_status['sonic_sketch_complete'] else '❌'} Sonic Sketch (30 min)
{'✅' if daily_status['visual_moodboard_complete'] else '❌'} Visual Moodboard (5 images)
{'✅' if daily_status['lore_fragment_complete'] else '❌'} Lore Fragment
{'🎯 COMPLETE' if daily_status['daily_loop_complete'] else '⚠️  INCOMPLETE'} Daily Loop Status

📊 WEEKLY PROGRESS
Micro-Releases: {weekly_progress['micro_releases_this_week']}/1
VST3 Plugins: {weekly_progress['vst3_plugins_this_week']}/1
Status: {'✅ ON TRACK' if weekly_progress['weekly_goal_met'] else '⚠️  BEHIND'}

📈 MONTHLY PROGRESS
Major Releases: {monthly_progress['major_releases_this_month']}/1
VST3 Plugins: {monthly_progress['vst3_plugins_this_month']}/4 (1 per week)
Status: {'✅ ON TRACK' if monthly_progress['monthly_goal_met'] else '⚠️  BEHIND'}

🎵 CREATIVE MOMENTUM
Consistency is key! Keep feeding the loop daily.
"""
        return report
    
    def get_creative_stats(self) -> Dict:
        """Get comprehensive creative statistics"""
        inputs = self._load_data(self.inputs_file)
        processes = self._load_data(self.processes_file)
        outputs = self._load_data(self.outputs_file)
        
        # Calculate completion streaks
        completed_days = [date for date, data in inputs.items() if all([
            data.get("sonic_sketch"),
            data.get("visual_moodboard"),
            data.get("lore_fragment")
        ])]
        
        micro_outputs = [o for o in outputs.values() if o.get("output_type") == "micro"]
        major_outputs = [o for o in outputs.values() if o.get("output_type") == "major"]
        vst3_outputs = [o for o in outputs.values() if o.get("output_type") == "vst3"]
        
        return {
            "total_input_days": len(inputs),
            "completed_input_days": len(completed_days),
            "completion_rate": len(completed_days) / max(len(inputs), 1) * 100,
            "total_processes": len(processes),
            "total_micro_releases": len(micro_outputs),
            "total_major_releases": len(major_outputs),
            "total_vst3_plugins": len(vst3_outputs),
            "current_streak": self._calculate_current_streak(completed_days)
        }
    
    def _calculate_current_streak(self, completed_days: List[str]) -> int:
        """Calculate current completion streak"""
        if not completed_days:
            return 0
        
        completed_dates = sorted([datetime.datetime.fromisoformat(d).date() for d in completed_days])
        today = datetime.date.today()
        
        streak = 0
        current_date = today
        
        while current_date in completed_dates:
            streak += 1
            current_date -= datetime.timedelta(days=1)
        
        return streak

    # TASK MANAGEMENT
    def get_tasks(self, task_type: str) -> List[Dict]:
        """Get all tasks for a specific type (weekly/monthly)"""
        tasks_file = self.data_dir / f"{task_type}_tasks.json"
        return self._load_data(tasks_file).get("tasks", [])
    
    def add_task(self, task_type: str, text: str, priority: str = "medium") -> Dict:
        """Add a new task"""
        tasks_file = self.data_dir / f"{task_type}_tasks.json"
        tasks_data = self._load_data(tasks_file)
        
        if "tasks" not in tasks_data:
            tasks_data["tasks"] = []
        
        # Generate unique ID
        task_id = str(len(tasks_data["tasks"]) + 1)
        while any(task["id"] == task_id for task in tasks_data["tasks"]):
            task_id = str(int(task_id) + 1)
        
        new_task = {
            "id": task_id,
            "text": text,
            "completed": False,
            "priority": priority,
            "created_at": datetime.datetime.now().isoformat(),
            "completed_at": None
        }
        
        tasks_data["tasks"].append(new_task)
        self._save_data(tasks_file, tasks_data)
        
        return new_task
    
    def update_task(self, task_type: str, task_id: str, updates: Dict) -> Dict:
        """Update a task (toggle completion, edit text, etc.)"""
        tasks_file = self.data_dir / f"{task_type}_tasks.json"
        tasks_data = self._load_data(tasks_file)
        
        if "tasks" not in tasks_data:
            tasks_data["tasks"] = []
        
        # Find and update task
        for task in tasks_data["tasks"]:
            if task["id"] == task_id:
                if "completed" in updates:
                    task["completed"] = updates["completed"]
                    task["completed_at"] = datetime.datetime.now().isoformat() if updates["completed"] else None
                if "text" in updates:
                    task["text"] = updates["text"]
                if "priority" in updates:
                    task["priority"] = updates["priority"]
                
                self._save_data(tasks_file, tasks_data)
                return task
        
        raise ValueError(f"Task with ID {task_id} not found")
    
    def delete_task(self, task_type: str, task_id: str) -> None:
        """Delete a task"""
        tasks_file = self.data_dir / f"{task_type}_tasks.json"
        tasks_data = self._load_data(tasks_file)
        
        if "tasks" not in tasks_data:
            tasks_data["tasks"] = []
        
        # Remove task
        original_length = len(tasks_data["tasks"])
        tasks_data["tasks"] = [task for task in tasks_data["tasks"] if task["id"] != task_id]
        
        if len(tasks_data["tasks"]) == original_length:
            raise ValueError(f"Task with ID {task_id} not found")
        
        self._save_data(tasks_file, tasks_data)

    # Payment Management Methods
    def get_payments(self) -> List[dict]:
        """Get all monthly payments"""
        payments_file = Path('loop_data/payments.json')
        if not payments_file.exists():
            # Return default payments if file doesn't exist
            default_payments = [
                {'id': '1', 'name': 'Ableton Live Suite', 'amount': 20.00, 'category': 'creative', 'notes': ''},
                {'id': '2', 'name': 'Plugin Subscriptions', 'amount': 30.00, 'category': 'creative', 'notes': ''},
                {'id': '3', 'name': 'Sample Libraries', 'amount': 15.00, 'category': 'creative', 'notes': ''},
                {'id': '4', 'name': 'Cloud Storage', 'amount': 10.00, 'category': 'services', 'notes': ''},
                {'id': '5', 'name': 'Streaming Platforms', 'amount': 25.00, 'category': 'services', 'notes': ''},
                {'id': '6', 'name': 'Domain & Hosting', 'amount': 12.00, 'category': 'services', 'notes': ''},
                {'id': '7', 'name': 'Gym Membership', 'amount': 50.00, 'category': 'lifestyle', 'notes': ''},
                {'id': '8', 'name': 'Supplements', 'amount': 40.00, 'category': 'lifestyle', 'notes': ''}
            ]
            # Save default payments
            self._save_data(payments_file, {'payments': default_payments})
            return default_payments
        
        payments_data = self._load_data(payments_file)
        return payments_data.get('payments', [])

    def add_payment(self, name: str, amount: float, category: str, notes: str = '') -> str:
        """Add a new payment"""
        payments_file = Path('loop_data/payments.json')
        payments_data = self._load_data(payments_file) if payments_file.exists() else {'payments': []}
        
        # Generate new ID
        existing_ids = [int(p['id']) for p in payments_data['payments'] if p['id'].isdigit()]
        new_id = str(max(existing_ids, default=0) + 1)
        
        new_payment = {
            'id': new_id,
            'name': name,
            'amount': float(amount),
            'category': category,
            'notes': notes,
            'created_at': datetime.datetime.now().isoformat()
        }
        
        payments_data['payments'].append(new_payment)
        self._save_data(payments_file, payments_data)
        
        print(f"✅ Payment '{name}' added successfully")
        return new_id

    def update_payment(self, payment_id: str, name: str, amount: float, category: str, notes: str = ''):
        """Update an existing payment"""
        payments_file = Path('loop_data/payments.json')
        if not payments_file.exists():
            raise ValueError("No payments found")
        
        payments_data = self._load_data(payments_file)
        payments = payments_data['payments']
        
        payment = next((p for p in payments if p['id'] == payment_id), None)
        if not payment:
            raise ValueError(f"Payment with ID {payment_id} not found")
        
        # Update payment fields
        payment['name'] = name
        payment['amount'] = float(amount)
        payment['category'] = category
        payment['notes'] = notes
        payment['updated_at'] = datetime.datetime.now().isoformat()
        
        self._save_data(payments_file, payments_data)
        print(f"✅ Payment '{name}' updated successfully")

    def delete_payment(self, payment_id: str):
        """Delete a payment"""
        payments_file = Path('loop_data/payments.json')
        if not payments_file.exists():
            raise ValueError("No payments found")
        
        payments_data = self._load_data(payments_file)
        payments = payments_data['payments']
        
        payment = next((p for p in payments if p['id'] == payment_id), None)
        if not payment:
            raise ValueError(f"Payment with ID {payment_id} not found")
        
        payments_data['payments'] = [p for p in payments if p['id'] != payment_id]
        self._save_data(payments_file, payments_data)
        print(f"✅ Payment '{payment['name']}' deleted successfully")

# CLI Interface
def main():
    agent = CreativeLoopAgent()
    
    print("🔁 DSGNRG Creative Loop Agent")
    print("=" * 40)
    print(agent.generate_creative_report())

if __name__ == "__main__":
    main()