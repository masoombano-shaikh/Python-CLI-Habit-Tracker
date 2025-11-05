from rich.console import Console
from rich.table import Table
from storage_handler import *

console = Console()

def not_found():
        '''Function when the data is not found.'''
        print("--------")
        print(f"No habits found!")
        print("--------\n")


class AnalyticsHandler:
    '''Contains core display functions for outputs.'''

    def __init__(self, tracker):
        '''Initializes a object of the Habit Tracker class.'''
        self.tracker = tracker




    def load_habits(self, habits):
        '''Prints all habit data in table format.'''
        if not habits:
            not_found()
        else:
            console.print("[bold magenta]\n--- Your Habits ---[/bold magenta]")
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Name", min_width=20)
            table.add_column("Description", min_width=20)
            table.add_column("Created On", min_width=12, justify="right")
            table.add_column("Duration", min_width=12, justify="right")
            table.add_column("Last Completed On", min_width=12, justify='right')
            table.add_column("Current Streak", min_width=12, justify="right")
            def get_duration_color(duration):
                COLORS = {'weekly': 'magenta', 'daily': 'cyan'}
                if duration in COLORS:
                    return COLORS[duration]
                return 'white'
            for habit in habits:
                c = get_duration_color(habit[3])
                table.add_row(f"{habit[0]}", f"{habit[1]}", f"{habit[2]}", f"[{c}]{habit[3]}[/{c}]", f"{habit[4]}", f"{habit[5]}")
            console.print(table)


    def display_habits(self, habits):
        '''Prints habit data in table format.'''
        if not habits:
            not_found()
        else:
            console.print("[bold green]\n--- Your Habits ---[/bold green]")
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Name", min_width=12, justify="right")
            table.add_column("Duration", min_width=12, justify="right")
            table.add_column("Last Completed on", min_width=12, justify="right")
            table.add_column("Current Streak", min_width=12, justify="right")
            def get_duration_color(duration):
                COLORS = {'weekly': 'magenta', 'daily': 'cyan'}
                if duration in COLORS:
                    return COLORS[duration]
                return 'white'
            for habit in habits:
                c = get_duration_color(habit[1])
                table.add_row(f"{habit[0]}", f"[{c}]{habit[1]}[/{c}]", f"{habit[2]}", f"{habit[3]}")
            console.print(table)


    def display_longest_habits(self, habits):
        '''Prints habit data in table format.'''
        if not habits:
            not_found()
        else:
            console.print("[bold green]\n--- Your Habits ---[/bold green]")
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Name", min_width=20)
            table.add_column("Longest Streak", min_width=12, justify="right")
            table.add_column("Current Streak", min_width=12, justify="right")
            for habit in habits:
                table.add_row(f"{habit[0]}", f"{habit[1]}", f"{habit[2]}")
            console.print(table)


    def display_duration_habits(self, habits, duration):
        '''Prints habit data in table format.'''
        if not habits:
            not_found()
        else:
            console.print("[bold green]\n--- Your Habits ---[/bold green]")
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Name", min_width=20)
            table.add_column("Description", min_width=20)
            table.add_column("Created On", min_width=12, justify="right")
            table.add_column("Duration", min_width=12, justify="right")
            table.add_column("Last Completed On", min_width=12, justify='right')
            table.add_column("Streak", min_width=12, justify="right")
            def get_duration_color(duration):
                COLORS = {'weekly': 'magenta', 'daily': 'cyan'}
                if duration in COLORS:
                    return COLORS[duration]
                return 'white'
            for habit in habits:
                c = get_duration_color(habit[3])
                table.add_row(f"{habit[0]}", f"{habit[1]}", f"{habit[2]}", f"[{c}]{habit[3]}[/{c}]", f"{habit[4]}", f"{habit[5]}")
            console.print(table)


    def display_longest_streak_habit(self, habits):
        '''Prints habit data in table format.'''
        if not habits:
            not_found()
        else:
            console.print("[bold green]\n--- Your Habits ---[/bold green]")
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Name", min_width=20)
            table.add_column("Longest Streak from All", min_width=12, justify="right")
            for habit in habits:
                table.add_row(f"{habit[0]}", f"{habit[1]}")
            console.print(table)


    def display_log_dates(self, habits):
        '''Prints progress data in table format.'''
        if not habits:
            not_found()
        else:
            console.print("[bold green]\n--- Your Habits ---[/bold green]")
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Name", min_width=20)
            table.add_column("Log Dates", min_width=12, justify="right")
            for habit in habits:
                table.add_row(f"{habit[0]}", f"{habit[1]}")
            console.print(table)
