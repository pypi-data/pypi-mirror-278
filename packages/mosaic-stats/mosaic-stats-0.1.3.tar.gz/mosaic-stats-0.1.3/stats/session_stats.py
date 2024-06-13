import os
from collections import defaultdict
from datetime import timedelta
import argparse
from stats import cache_handler

def generate_session_stats(root_dir, panels=None):
    if not cache_handler.is_cache_valid(root_dir):
        exposure_cache = cache_handler.update_cache(root_dir)
    else:
        exposure_cache = cache_handler.get_cached_data(root_dir)

    total_exposure_per_session = defaultdict(lambda: {"exposure": timedelta(), "subs": 0})

    for file_info in exposure_cache:
        exposure_time = timedelta(seconds=file_info['exposure'])

        dirpath = file_info['dirpath']
        parts = dirpath.split(os.sep)
        panel_id = None
        session_date = None
        for part in parts:
            if "PANEL" in part:
                panel_id = part.split("_")[1]
            elif "SESSION" in part:
                session_date = part.split("_")[1]

        if panel_id and session_date:
            if panels is None or panel_id in panels:
                total_exposure_per_session[session_date]["exposure"] += exposure_time
                total_exposure_per_session[session_date]["subs"] += 1

    return total_exposure_per_session

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours:02}h{minutes:02}m"

def main(root_dir='Lights', panels=None):
    total_exposure_per_session = generate_session_stats(root_dir, panels)

    os.system('clear')

    print(f"\n\033[4mStatistics Per Session:\033[0m\n")

    for session, data in sorted(total_exposure_per_session.items()):
        print(f"Session {session}: {format_timedelta(data['exposure'])} = {data['subs']:3} x {format_timedelta(timedelta(seconds=300))}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate session statistics.')
    parser.add_argument('root_dir', nargs='?', default='Lights', help='Root directory for your Lights')
    parser.add_argument('--panels', nargs='*', help='List of panels to include in the calculations')
    args = parser.parse_args()
    main(root_dir=args.root_dir, panels=args.panels)
