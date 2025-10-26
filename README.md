# DSGNRG Creative Loop Agent

A modular system to track and maintain creative consistency as an artist/producer/DJ.

## Features

🔁 **Creative Loop Tracking**
- Daily input logging (sonic sketches, visual moodboards, lore fragments)
- Creative process documentation (Sample → Remix → Render)
- Output tracking (micro-releases weekly, major releases monthly)

📊 **Progress Analytics**
- Daily completion status
- Weekly and monthly progress tracking
- Creative statistics and streaks
- Comprehensive reporting

🖥️ **Multiple Interfaces**
- Command-line interface (CLI)
- Web dashboard with real-time updates
- Python API for custom integrations

## Quick Start

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

**Note**: If you see a PATH warning during installation, this is normal and won't affect functionality. The system will work perfectly with the standard Python installation.

### 2. Easy Launcher (Windows)
```powershell
# Double-click launcher.bat for a user-friendly menu interface
launcher.bat
```

### 3. CLI Usage
```powershell
# Log daily inputs
python loop_cli.py input sketch 30 "Ambient drone with field recordings"
python loop_cli.py input visual "Cyberpunk neon" --images img1.jpg img2.jpg img3.jpg img4.jpg img5.jpg
python loop_cli.py input lore "Zara" "Discovered encrypted data fragments" "Digital archaeology arc"

# Log creative process
python loop_cli.py process "field_recording.wav" "granular synthesis" "24bit/48kHz WAV" "melancholic" --tempo 85

# Log outputs
python loop_cli.py output micro "Neon Dreams Beat" beat --file "beats/neon_dreams.wav"
python loop_cli.py output major "Digital Archaeology EP" track --file "releases/digital_arch_ep.wav"

# Check status
python loop_cli.py status daily
python loop_cli.py status report
```

### 3. Web Dashboard
```powershell
python loop_server.py
```
Then open http://localhost:5000 in your browser.

### 4. Python Integration
```python
from creative_loop_agent import CreativeLoopAgent

agent = CreativeLoopAgent()

# Log daily inputs
agent.log_sonic_sketch(30, "Ambient textures", tags=["ambient", "experimental"])
agent.log_visual_moodboard(["img1.jpg", "img2.jpg"], "Dark synthwave")
agent.log_lore_fragment("Nova", "The signal was getting stronger", "Signal hunt arc")

# Check progress
status = agent.get_daily_completion_status()
report = agent.generate_creative_report()
```

## Creative Loop Structure

### Input Phase (Daily)
- **Sonic Sketch**: 30-minute audio exploration
- **Visual Moodboard**: 5 images that capture your vibe
- **Lore Fragment**: Character or world-building element

### Process Phase
- **Sample**: Source material identification
- **Remix**: Creative transformation approach
- **Render**: Final output format and processing

### Output Phase
- **Micro-Releases** (Weekly): Beats, visuals, lore drops
- **Major Releases** (Monthly): Tracks, videos, plugins

## File Structure
```
DSGNRG_CREATIVE_LOOP/
├── creative_loop_agent.py    # Core tracking logic
├── loop_cli.py              # Command-line interface
├── loop_server.py           # Web server
├── dashboard.html           # Web dashboard
├── launcher.bat             # Windows GUI launcher
├── setup.bat               # Windows setup script
├── setup.ps1               # PowerShell setup script
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── loop_data/              # Generated data directory
│   ├── inputs.json         # Daily input logs
│   ├── processes.json      # Creative process logs
│   ├── outputs.json        # Release logs
│   └── stats.json          # Statistics cache
└── INSTRUCTIONS/
    └── INSTRUCTIONS.txt    # Original creative guidance
```

## Dashboard Features

- **Real-time Progress Tracking**: Visual progress bars for daily, weekly, and monthly goals
- **Creative Statistics**: Streak counters, completion rates, and output metrics
- **Quick Actions**: Fast logging buttons for common inputs
- **Activity Timeline**: Recent creative activities and milestones

## API Endpoints

- `GET /api/status/daily` - Daily completion status
- `GET /api/status/weekly` - Weekly progress
- `GET /api/status/monthly` - Monthly progress
- `GET /api/stats` - Creative statistics
- `POST /api/input/sketch` - Log sonic sketch
- `POST /api/input/visual` - Log visual moodboard
- `POST /api/input/lore` - Log lore fragment
- `POST /api/process` - Log creative process
- `POST /api/output/micro` - Log micro release
- `POST /api/output/major` - Log major release

## Customization

The system is designed to be modular and extensible. You can:

- Modify the `CreativeLoopAgent` class to add new tracking categories
- Customize the dashboard styling in `dashboard.html`
- Add new CLI commands in `loop_cli.py`
- Integrate with external tools via the Python API

## Philosophy

Consistency as a creative is not about rigid schedules—it's about **ritualized momentum**. This system helps you:

1. **Build Daily Habits**: Small, manageable creative inputs every day
2. **Track Progress**: Visual feedback on your creative consistency  
3. **Maintain Flow**: Modular system that adapts to your creative process
4. **Document Journey**: Complete history of your creative evolution

Remember: The goal is not perfection, but **persistent creative momentum**. 🔁

---

*Created for the DSGNRG Creative Loop project - scaffold your creativity, track your momentum.*