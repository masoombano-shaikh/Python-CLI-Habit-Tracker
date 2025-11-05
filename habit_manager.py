from storage_handler import *
from analytics_handler import *
import questionary
from datetime import datetime

habit_tracker= HabitTracker()
analytics = AnalyticsHandler(habit_tracker)

class Habit:
    def __init__(self, name, description, duration, creation_date=None, last_checked=0, streak=0):
        '''Initializes new habit by accepting values for the parameters:
        param:
        name = Name of the habit,
        description = Description for the habit,
        creation date = Date and timestamp at which the habit was created,
        last checked = Date and timestamp at which, the habit was completed,
        streak = Number of days of habit completion.'''
        self.name = name
        self.description = description
        self.duration = duration
        self.creation_date = creation_date or datetime.now().strftime('%Y-%m-%d, %H:%M')
        self.last_checked = last_checked
        self.streak = streak


    def __str__(self):
        return f"{self.name}", f"{self.description}", f"{self.duration}", f"{self.creation_date}", f"{self.last_checked}", f"{self.streak}"



class HabitManager:
    '''Contains core functions for user input.'''

    def __init__(self, tracker: HabitTracker):
        '''Initializes a object of the Habit Tracker class.'''
        self.tracker = tracker


    def create_habit(self):
        '''Creates a new habit based on the user input.'''
        HabitManager.load(self)
        name = questionary.text('Enter the habit name ',
        validate=lambda text: True if len(text) > 0 else 'Please enter a value').ask()
        description = questionary.text('Enter the habit description ',
        validate=lambda text: True if len(text) > 0 else 'Please enter a value').ask()
        duration = questionary.select('How often should this habit be completed?',
        choices=['daily', 'weekly']).ask()
        creation_date = datetime.now().strftime('%Y-%m-%d, %H:%M')
        ht = Habit(name, description, duration, creation_date, streak = 0)
        self.tracker.add_habit(ht.name, ht.description, ht.duration, ht.creation_date, ht.streak)


    def load(self):
        '''Loads the habit data in a table format.'''
        habits = self.tracker.get_all_habits()
        analytics.load_habits(habits)


    def mark_streak(self):
        '''Marks a streak complete for the selected habit from the existing habits.'''
        habits = self.tracker.get_habits()
        analytics.display_habits(habits)
        name = questionary.text("Enter habit name to mark complete: ",
        validate=lambda text: True if len(text) > 0 else 'Please enter a value').ask()
        ht = Habit(name, "NULL", "NULL")
        dur = self.tracker.get_duration(ht.name)
        if dur == [('daily',)]:
            self.tracker.check_daily_habit(ht.name)
        else:
            self.tracker.check_weekly_habit(ht.name)


    def analyse(self):
        '''Returns data from habit and progress table for user to analyse.'''
        while True:
            UI_decorator.menu()
            print("1. Analyse all habits")
            print("2. Analyse habits with same duration")
            print("3. Analyse check-off logs for a habit")
            print("4. Analyse longest streaks of all habits")
            print("5. Analyse your longest streak")
            print("6. Exit")
            print("\n(Enter a number from the menu above)")
            choice = input("Enter your choice: ")
            

            if choice == '1':
                HabitManager.load(self)
            elif choice == '2':
                duration = questionary.select('Enter habit duration you want to see',
                    choices=['daily', 'weekly']).ask()
                habits = self.tracker.get_habits_by_duration(duration)
                analytics.display_duration_habits(habits,duration)
            elif choice == '3':
                name = questionary.text('Enter habit name to analyse a list of logs: ',
                validate=lambda text: True if len(text) > 0 else 'Please enter a value').ask()
                habits = self.tracker.get_logs(name)
                analytics.display_log_dates(habits)
            elif choice == '4':
                habits = self.tracker.get_longest_streak_of_all_habits()
                analytics.display_longest_habits(habits)
            elif choice == '5':
                habits = self.tracker.get_longest_streak_from_all()
                analytics.display_longest_streak_habit(habits)
            elif choice == '6':
                UI_decorator.suffix()
                break
            else:
                print("Invalid choice. Please try again.")
                print("--------\n")


    def delete(self):
        '''Deletes a habit from the habit table based on the user input.'''
        habits = self.tracker.get_habits()
        analytics.display_habits(habits)
        name = questionary.text("Enter habit name to delete: ",
        validate=lambda text: True if len(text) > 0 else 'Please enter a value').ask()
        ht = Habit(name, "NULL", "NULL")
        self.tracker.delete_habit(ht.name)


    def exit_tracker(self):
        '''Shows the saved data while exit.'''
        HabitManager.load(self)
        print("All changes are saved!")
        print("--------\n")
        print("\n---x Exiting habit tracker! x---\n")
