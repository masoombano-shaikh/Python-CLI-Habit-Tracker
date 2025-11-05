from storage_handler import *
from habit_manager import *
from analytics_handler import *
from pre_load_data import *

def main():
    tracker = HabitTracker()
    manager = HabitManager(tracker)
    preload_habits()
    marking_habits()

    while True:
        UI_decorator.enter()
        print("1. Create new habit")
        print("2. Mark habit complete")
        print("3. Analyse habits")
        print("4. Delete habit")
        print("5. Exit")


        print("\n(Enter a number from the menu above)")
        choice = input("Enter your choice: ")
        


        if choice == '1':
            manager.create_habit()
        elif choice == '2':
            manager.mark_streak()
        elif choice == '3':
            manager.analyse()
        elif choice == '4':
            manager.delete()
        elif choice == '5':
            value = questionary.select('Do you want exit the habit tracker?',
            choices=['Yes', 'No']).ask()
            if value == 'Yes':
                manager.exit_tracker()
                delete_data()
                break


        else:
            print("Invalid choice. Please try again.")
            print("--------\n")


if __name__ == "__main__":
    main()