import os
from collections import defaultdict
from datetime import timedelta
import argparse
from stats import cache_handler

def generate_stats(root_dir):
    if not cache_handler.is_cache_valid(root_dir):
        exposure_cache = cache_handler.update_cache(root_dir)
    else:
        exposure_cache = cache_handler.get_cached_data(root_dir)

    total_exposure = timedelta()
    total_exposure_per_year = defaultdict(timedelta)
    total_exposure_per_panel = defaultdict(lambda: {"exposure": timedelta(), "subs": 0})
    total_number_of_subs = 0
    number_of_subs_per_panel = defaultdict(int)
    total_exposure_per_yyyymm = defaultdict(lambda: {"exposure": timedelta(), "subs": 0})

    for file_info in exposure_cache:
        exposure_time = timedelta(seconds=file_info['exposure'])
        total_number_of_subs += 1

        dirpath = file_info['dirpath']
        parts = dirpath.split(os.sep)
        panel_id = None
        year = None
        yyyymm = None
        for part in parts:
            if "PANEL" in part:
                panel_id = part.split("_")[1]
            elif "SESSION" in part:
                date_part = part.split("_")[1]
                year = date_part[:4]
                yyyymm = date_part[:6]

        total_exposure += exposure_time
        total_exposure_per_year[year] += exposure_time
        total_exposure_per_panel[panel_id]["exposure"] += exposure_time
        total_exposure_per_panel[panel_id]["subs"] += 1
        total_exposure_per_yyyymm[yyyymm]["exposure"] += exposure_time
        total_exposure_per_yyyymm[yyyymm]["subs"] += 1

        number_of_subs_per_panel[panel_id] += 1

    return (total_exposure, total_number_of_subs, total_exposure_per_year, total_exposure_per_panel, total_exposure_per_yyyymm)

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours:02}h{minutes:02}m"

def main(root_dir='Lights'):
    stats = generate_stats(root_dir)
    total_exposure, total_number_of_subs, total_exposure_per_year, total_exposure_per_panel, total_exposure_per_yyyymm = stats

    os.system('clear')
    print(f"\n\n\033[4mTotal Exposure:\033[0m\n")
    print(f"  \033[2mTotal\033[0m          {format_timedelta(total_exposure)} = {total_number_of_subs:3} x {format_timedelta(timedelta(seconds=300))}")
    for year, exposure in sorted(total_exposure_per_year.items()):
        subs_count = sum(data['subs'] for k, data in total_exposure_per_yyyymm.items() if k.startswith(year))
        print(f"  \033[2m{year:14}\033[0m {format_timedelta(exposure)} = {subs_count:3} x {format_timedelta(timedelta(seconds=300))}")

    print("\n\n\033[4mTotal Exposure per Panel:\033[0m\n")
    for panel, data in sorted(total_exposure_per_panel.items()):
        print(f"  \033[2m{panel:14}\033[0m {format_timedelta(data['exposure'])} = {data['subs']:3} x {format_timedelta(timedelta(seconds=300))}")

    print("\n\033[4mExposure per YYYY/MM:\033[0m\n")
    for yyyymm, data in sorted(total_exposure_per_yyyymm.items()):
        year, month = yyyymm[:4], int(yyyymm[4:])
        formatted_date = f"{year}/{month:02}"
        print(f"  \033[2m{formatted_date:14}\033[0m {format_timedelta(data['exposure'])} = {data['subs']:3} x {format_timedelta(timedelta(seconds=300))}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate overall statistics.')
    parser.add_argument('root_dir', nargs='?', default='Lights', help='Root directory for your Lights')
    args = parser.parse_args()
    main(root_dir=args.root_dir)
