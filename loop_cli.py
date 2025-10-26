#!/usr/bin/env python3
"""
DSGNRG Creative Loop CLI
Easy command-line interface for tracking your creative loop
"""

import argparse
import sys
from pathlib import Path
from creative_loop_agent import CreativeLoopAgent

def main():
    parser = argparse.ArgumentParser(description="DSGNRG Creative Loop Tracker")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Input commands
    input_parser = subparsers.add_parser('input', help='Log daily creative inputs')
    input_subparsers = input_parser.add_subparsers(dest='input_type')
    
    # Sonic sketch
    sketch_parser = input_subparsers.add_parser('sketch', help='Log sonic sketch')
    sketch_parser.add_argument('duration', type=int, help='Duration in minutes')
    sketch_parser.add_argument('description', help='Description of the sketch')
    sketch_parser.add_argument('--audio', help='Path to audio file')
    sketch_parser.add_argument('--tags', nargs='+', help='Tags for the sketch')
    
    # Visual moodboard
    visual_parser = input_subparsers.add_parser('visual', help='Log visual moodboard')
    visual_parser.add_argument('theme', help='Theme of the moodboard')
    visual_parser.add_argument('--images', nargs='+', required=True, help='Image file paths')
    visual_parser.add_argument('--colors', nargs='+', help='Color palette')
    
    # Lore fragment
    lore_parser = input_subparsers.add_parser('lore', help='Log lore fragment')
    lore_parser.add_argument('character', help='Character name')
    lore_parser.add_argument('fragment', help='Lore fragment text')
    lore_parser.add_argument('arc', help='Narrative arc')
    lore_parser.add_argument('--elements', nargs='+', help='World building elements')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Log creative process')
    process_parser.add_argument('sample', help='Sample source')
    process_parser.add_argument('remix', help='Remix approach')
    process_parser.add_argument('render', help='Render format')
    process_parser.add_argument('emotion', help='Emotion tag')
    process_parser.add_argument('--tempo', type=int, help='Tempo (BPM)')
    process_parser.add_argument('--lore-connection', help='Lore arc connection')
    
    # Output commands
    output_parser = subparsers.add_parser('output', help='Log creative outputs')
    output_subparsers = output_parser.add_subparsers(dest='output_type')
    
    # Micro release
    micro_parser = output_subparsers.add_parser('micro', help='Log micro release')
    micro_parser.add_argument('title', help='Release title')
    micro_parser.add_argument('category', choices=['beat', 'visual', 'lore'], help='Release category')
    micro_parser.add_argument('--file', help='File path')
    micro_parser.add_argument('--description', help='Description')
    micro_parser.add_argument('--tags', nargs='+', help='Tags')
    
    # Major release
    major_parser = output_subparsers.add_parser('major', help='Log major release')
    major_parser.add_argument('title', help='Release title')
    major_parser.add_argument('category', choices=['track', 'video', 'plugin'], help='Release category')
    major_parser.add_argument('--file', help='File path')
    major_parser.add_argument('--description', help='Description')
    major_parser.add_argument('--tags', nargs='+', help='Tags')
    
    # VST3 plugin
    vst3_parser = output_subparsers.add_parser('vst3', help='Log VST3 plugin')
    vst3_parser.add_argument('title', help='Plugin title')
    vst3_parser.add_argument('--file', help='File path')
    vst3_parser.add_argument('--description', help='Description')
    vst3_parser.add_argument('--tags', nargs='+', help='Tags')
    
    # Status commands
    status_parser = subparsers.add_parser('status', help='Check status and progress')
    status_subparsers = status_parser.add_subparsers(dest='status_type')
    status_subparsers.add_parser('daily', help='Check daily completion status')
    status_subparsers.add_parser('weekly', help='Check weekly progress')
    status_subparsers.add_parser('monthly', help='Check monthly progress')
    status_subparsers.add_parser('report', help='Generate full creative report')
    status_subparsers.add_parser('stats', help='Show creative statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize agent
    agent = CreativeLoopAgent()
    
    try:
        if args.command == 'input':
            handle_input_command(agent, args)
        elif args.command == 'process':
            handle_process_command(agent, args)
        elif args.command == 'output':
            handle_output_command(agent, args)
        elif args.command == 'status':
            handle_status_command(agent, args)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def handle_input_command(agent, args):
    if args.input_type == 'sketch':
        agent.log_sonic_sketch(args.duration, args.description, args.audio, args.tags)
    elif args.input_type == 'visual':
        agent.log_visual_moodboard(args.images, args.theme, args.colors)
    elif args.input_type == 'lore':
        agent.log_lore_fragment(args.character, args.fragment, args.arc, args.elements)
    else:
        print("Please specify input type: sketch, visual, or lore")

def handle_process_command(agent, args):
    agent.log_creative_process(
        args.sample, args.remix, args.render, args.emotion,
        args.tempo, args.lore_connection or ""
    )

def handle_output_command(agent, args):
    if args.output_type == 'micro':
        agent.log_micro_release(
            args.title, args.category, args.file, 
            args.description or "", args.tags
        )
    elif args.output_type == 'major':
        agent.log_major_release(
            args.title, args.category, args.file,
            args.description or "", args.tags
        )
    elif args.output_type == 'vst3':
        agent.log_vst3_plugin(
            args.title, args.file,
            args.description or "", args.tags
        )
    else:
        print("Please specify output type: micro, major, or vst3")

def handle_status_command(agent, args):
    if args.status_type == 'daily':
        status = agent.get_daily_completion_status()
        print_daily_status(status)
    elif args.status_type == 'weekly':
        progress = agent.get_weekly_progress()
        print_weekly_progress(progress)
    elif args.status_type == 'monthly':
        progress = agent.get_monthly_progress()
        print_monthly_progress(progress)
    elif args.status_type == 'report':
        print(agent.generate_creative_report())
    elif args.status_type == 'stats':
        stats = agent.get_creative_stats()
        print_stats(stats)
    else:
        print("Please specify status type: daily, weekly, monthly, report, or stats")

def print_daily_status(status):
    print(f"\n📅 Daily Status for {status['date']}")
    print("=" * 30)
    print(f"{'✅' if status['sonic_sketch_complete'] else '❌'} Sonic Sketch")
    print(f"{'✅' if status['visual_moodboard_complete'] else '❌'} Visual Moodboard")
    print(f"{'✅' if status['lore_fragment_complete'] else '❌'} Lore Fragment")
    print(f"\n🎯 {'COMPLETE' if status['daily_loop_complete'] else 'INCOMPLETE'}")

def print_weekly_progress(progress):
    print(f"\n📊 Weekly Progress")
    print("=" * 20)
    print(f"Week starting: {progress['week_start']}")
    print(f"Micro-releases: {progress['micro_releases_this_week']}/{progress['target_micro_releases']}")
    print(f"Status: {'✅ ON TRACK' if progress['weekly_goal_met'] else '⚠️  BEHIND'}")

def print_monthly_progress(progress):
    print(f"\n📈 Monthly Progress")
    print("=" * 20)
    print(f"Month starting: {progress['month_start']}")
    print(f"Major releases: {progress['major_releases_this_month']}/{progress['target_major_releases']}")
    print(f"Status: {'✅ ON TRACK' if progress['monthly_goal_met'] else '⚠️  BEHIND'}")

def print_stats(stats):
    print(f"\n📊 Creative Statistics")
    print("=" * 25)
    print(f"Total input days: {stats['total_input_days']}")
    print(f"Completed days: {stats['completed_input_days']}")
    print(f"Completion rate: {stats['completion_rate']:.1f}%")
    print(f"Current streak: {stats['current_streak']} days")
    print(f"Total processes: {stats['total_processes']}")
    print(f"Micro releases: {stats['total_micro_releases']}")
    print(f"Major releases: {stats['total_major_releases']}")
    print(f"VST3 plugins: {stats['total_vst3_plugins']}")

if __name__ == "__main__":
    main()