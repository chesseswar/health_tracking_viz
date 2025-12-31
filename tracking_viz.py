import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import datetime as dt
import calendar

WEEKS = 52
DAYS = 7


def get_dates(filename, year):
    with open(filename, 'r') as f:
        return [
            dt.date(
                year,
                *map(int, line.split(maxsplit=1)[0].split('/'))
            )
            for line in f.readlines()
            if len(line.strip()) > 0
        ]


def plot_tracking(filename, year):
    start_of_year = dt.date(year, 1, 1)
    end_of_year = dt.date(year, 12, 31)
    start_sunday = start_of_year - dt.timedelta(days=(start_of_year.weekday() + 1) % 7)

    dates = get_dates(filename, year)
    grid = np.zeros((DAYS, WEEKS))
    for d in dates:
        delta_days = (d - start_sunday).days
        week_idx = delta_days // 7
        if 0 <= week_idx < WEEKS:
            weekday_idx = (d.weekday() + 1) % 7
            grid[weekday_idx, week_idx] = 0.5

    _, ax = plt.subplots(figsize=(12, 2.5))
    cmap = mcolors.ListedColormap([
        "#ebedf0",
        "#28b555",
    ])

    _ = ax.imshow(
        grid,
        cmap=cmap,
        vmin=0,
        vmax=1,
        interpolation="nearest",
        aspect="auto"
    )

    month_positions_centered = []
    for month in range(1, 13):
        first_day = dt.date(year, month, 1)
        last_day = dt.date(year, month, calendar.monthrange(year, month)[1])

        start_week = (first_day - start_sunday).days // DAYS
        end_week = (last_day - start_sunday).days // DAYS

        if 0 <= start_week < WEEKS:
            month_positions_centered.append((start_week + end_week) / 2)

    ax.set_xticks(month_positions_centered)
    ax.set_xticklabels(calendar.month_abbr[1:13])


    ax.set_yticks(range(7))
    ax.set_yticklabels(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
    ax.set_aspect("equal")
    ax.set_xticks(np.arange(-0.5, WEEKS, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, DAYS, 1), minor=True)
    ax.grid(which="minor", color="lightgray", linewidth=0.5)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.set_title(f"{year} Gym Tracking")
    plt.tight_layout()
    plt.show()
