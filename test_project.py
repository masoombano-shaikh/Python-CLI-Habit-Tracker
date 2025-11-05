import pytest
from freezegun import freeze_time
from main import *
from storage_handler import HabitTracker

@pytest.fixture
def database():
    '''Creates a database instance'''
    database = HabitTracker('test.db')
    return database


def test_add(database: HabitTracker):
    '''Tests if it adds a new habit to the database.'''
    database.create_table()
    today = datetime.now().strftime('%Y-%m-%d, %H:%M')
    assert database.add_habit('read', 'everyday for 15 mins', today, 'daily', 0) == print("Habit 'read' successfully added!")
    assert database.add_habit('journal', 'gratitude journal', today, 'weekly', 0) == print("Habit 'journal' successfully added!")
    assert database.add_habit('piano', 'practice piano everyday', '2025-08-25, 12:30', 'daily', 0) == print("Habit 'piano' successfully added!")
    assert database.add_habit('surf', 'weekly surfing session', '2025-08-11, 15:29', 'weekly', 0) == print("Habit 'surf' successfully added!")
    assert database.add_habit('exercise', '20 mins', today, 'daily', 0) == print("Habit 'exercise' successfully added!")
    assert database.add_habit('grocery shopping', 'meal prep', today, 'weekly', 0) == print("Habit 'grocery shopping' successfully added!")
    


def test_create_habit(database: HabitTracker):
    '''Tests if it creates a new habit.'''
    ht = Habit(name = 'dance', description = 'activity', duration = 'daily', creation_date = datetime.now().strftime('%Y-%m-%d, %H:%M'), streak = 0)
    assert database.add_habit(ht.name, ht.description, ht.duration, ht.creation_date, ht.streak) == print("Habit 'dance' successfully added!")
    ht = Habit(name = 'paint', description = 'take paint classes', duration = 'weekly', creation_date = datetime.now().strftime('%Y-%m-%d, %H:%M'), streak = 0)
    assert database.add_habit(ht.name, ht.description, ht.duration, ht.creation_date, ht.streak) == print("Habit 'paint' successfully added!")


def test_duplicate_add(database: HabitTracker):
    '''Tests if it flags the user if enters a habit name that already exists.'''
    assert database.add_habit('piano', 'practice piano everyday', '2025-08-25, 13:00', 'daily', 0) == print("Habit 'piano' already exists!")
    assert database.add_habit('surf', 'weekly surfing session', '2025-07-25, 21:45', 'weekly', 0) == print("Habit 'surf' already exists!")


def test_verification_fail(database: HabitTracker):
    '''Tests if it verifies if the habit exists in the database'''
    assert database.verification('run') == print("Habit 'run' not found!")
    assert database.verification('swim') == print("Habit 'swim' not found!")


def test_mark_weekly_habit_complete(database: HabitTracker):
    '''Tests if it completes the habit.'''
    today = datetime.now().strftime('%Y-%m-%d, %H:%M')
    ht = Habit('paint', "NULL", "NULL")
    #verifies if the habit name exists in the database.
    assert database.verification(ht.name)
    #collects the duration of the habit name.
    assert database.get_duration(ht.name)
    #collects the last completed date of the habit.
    assert database.get_last_completed_date(ht.name)
    #collects the most current number of streak of the habit
    assert database.get_streak(ht.name)
    #inserts the name and current date with timestamp in the progress table.
    assert database.mark_habit(ht.name, today) == None
    #returns a calculated streak value for the habit
    assert database.calculate_weekly_habit(ht.name) == None
    #updates habit table for the last checked date.
    assert database.update_habit_for_last_checked(today, ht.name) == None
    #updates habit table for the calculated streak value.
    assert database.update_habit_for_streak(1, ht.name) == None


def test_mark_daily_habit_complete(database: HabitTracker):
    '''Tests if it completes the habit.'''
    today = datetime.now().strftime('%Y-%m-%d, %H:%M')
    ht = Habit('dance', "NULL", "NULL")
    #verifies if the habit name exists in the database.
    assert database.verification(ht.name)
    #collects the duration of the habit name.
    assert database.get_duration(ht.name)
    #collects the last completed date of the habit.
    assert database.get_last_completed_date(ht.name)
    #collects the most current number of streak of the habit
    assert database.get_streak(ht.name)
    #inserts the name and current date with timestamp in the progress table.
    assert database.mark_habit(ht.name, today) == None
    #returns a calculated streak value for the habit
    assert database.calculate_daily_habit(ht.name) == None
    #updates habit table for the last checked date.
    assert database.update_habit_for_last_checked(today, ht.name) == None
    #updates habit table for the calculated streak value.
    assert database.update_habit_for_streak(1, ht.name) == None


def test_mark_complete(database: HabitTracker):
    '''Tests if it marks a habit complete.'''
    assert database.mark_habit('piano', '2025-08-25, 10:30') == None
    assert database.mark_habit('piano', '2025-08-26, 15:40') == None
    assert database.mark_habit('surf', '2025-08-10, 17:49') == None
    assert database.mark_habit('surf', '2025-08-17, 22:00') == None
    assert database.mark_habit('surf', '2025-08-24, 19:08') == None


def test_calculate_streak(database):
    '''Tests if it calculates the streak count.'''
    assert database.calculate_daily_habit('piano') == None
    assert database.calculate_weekly_habit('surf') == None


def test_complete_daily_habit(database: HabitTracker):
    '''Tests if it completes the daily habit.'''
    ht = Habit("read", "NULL", "NULL")
    assert  database.check_daily_habit(ht.name) == print(f"Habit '{ht.name}' marked complete for today!")
    ht = Habit("dance", "NULL", "NULL")
    assert  database.check_daily_habit(ht.name) == print(f"Habit '{ht.name}' marked complete for today!")


def test_complete_daily_habit_for_already_completed_habit(database: HabitTracker):
    '''Tests if it flags, when daily habit is already complete.'''
    ht = Habit("read", "NULL", "NULL")
    assert database.check_daily_habit(ht.name) == print(f"Habit '{ht.name}' already marked complete for today!")
    ht = Habit("dance", "NULL", "NULL")
    assert database.check_daily_habit(ht.name) == print(f"Habit '{ht.name}' already marked complete for today!")


def test_complete_daily_habit_with_streak_reset(database: HabitTracker):
    '''Tests if it resets the  streak and restarts the if for daily habit.'''
    ht = Habit("piano", "NULL", "NULL")
    assert database.check_daily_habit(ht.name) == print(f"Streak started again for habit '{ht.name}' and marked complete for today!")


def test_complete_weekly_habit(database: HabitTracker):
    '''Tests if it completes the weekly habit.'''
    ht = Habit("journal", "NULL", "NULL")
    assert  database.check_weekly_habit(ht.name) == print(f"Habit '{ht.name}' marked complete for this week!")
    ht = Habit("paint", "NULL", "NULL")
    assert  database.check_weekly_habit(ht.name) == print(f"Habit '{ht.name}' marked complete for this week!")


def test_complete_weekly_habit_for_already_completed_habit(database: HabitTracker):
    '''Tests if it flags, when weekly habit is already complete.'''
    ht = Habit("journal", "NULL", "NULL")
    assert database.check_weekly_habit(ht.name) == print(f"Habit '{ht.name}' already marked complete for this week!")


def test_complete_weekly_habit_with_streak_reset(database: HabitTracker):
    '''Tests if it resets the  streak and restarts the if for weekly habit.'''
    ht = Habit("surf", "NULL", "NULL")
    assert  database.check_weekly_habit(ht.name) == print(f"Streak started again for habit '{ht.name}' and marked complete for week!")


def test_get_habits_by_daily_duration(database: HabitTracker):
    '''Tests if it returns all the habits with daily duration.'''
    assert database.get_habits_by_duration('daily')


def test_get_habit_by_weekly_duration(database: HabitTracker):
    '''Tests if it returns all the habits with weekly duration.'''
    assert database.get_habits_by_duration('weekly')


def test_longest_of_all_habits(database: HabitTracker):
    '''Tests if it returns longest streaks of all the habits.'''
    assert database.get_longest_streak_of_all_habits()


def test_longest_streak_from_all(database: HabitTracker):
    '''Tests if it returns longest streaks from all the habits.'''
    assert database.get_longest_streak_from_all() == [('surf', 4)]


def test_view(database: HabitTracker):
    '''Tests if it returns all the habits existing in the habit table.'''
    assert database.get_all_habits()


def test_logs_view(database: HabitTracker):
    '''Tests if it returns all the dates with timestamp when a habit was marked completed.'''
    ht = Habit("dance", "NULL", "NULL")
    assert database.get_logs(ht.name)

def test_streak_respects_periodicity(database: HabitTracker):
    now = datetime(2025, 11, 1)
    daily_name = "exercise"
    weekly_name = "grocery shopping"
    # Mark daily and weekly habit as completed today
    with freeze_time(now):
        database.check_daily_habit(daily_name)
        assert database.get_streak(daily_name)[0] == (1,) # streak should be 1 now
        database.check_weekly_habit(weekly_name)
        assert database.get_streak(weekly_name)[0] == (1,)  # streak should be 1 now

    # Move one day forward - daily streak should increment, weekly should be 1
    next_day = now + timedelta(days=1)
    with freeze_time(next_day):
        database.check_daily_habit(daily_name)
        assert database.get_streak(daily_name)[0] == (2,)  # streak increments daily
        database.check_weekly_habit(weekly_name)
        # weekly streak still 1 because within same week
        assert database.get_streak(weekly_name)[0] == (1,)

    # Move to next week - weekly streak increments, daily streak resets if missed day
    next_week = now + timedelta(weeks=1)
    with freeze_time(next_week):
        database.check_weekly_habit(weekly_name)
        assert database.get_streak(weekly_name)[0] == (2,)  # weekly streak increments
        database.check_daily_habit(daily_name)
        # daily streak resets due to missed days, so should be 1 again
        assert database.get_streak(daily_name)[0] == (1,)



def test_remove(database: HabitTracker):
    '''Tests if it removes all the habits from the database.'''
    assert database.delete_habit('read') == print(f"Habit 'read' successfully deleted.")
    assert database.delete_habit('journal')== print(f"Habit 'journal' successfully deleted.")
    assert database.delete_habit('piano') == print(f"Habit 'piano' successfully deleted.")
    assert database.delete_habit('surf') == print(f"Habit 'surf' successfully deleted.")
    assert database.delete_habit('exercise') == print(f"Habit 'surf' successfully deleted.")
    assert database.delete_habit('grocery shopping') == print(f"Habit 'surf' successfully deleted.")

def test_delete(database: HabitTracker):
    '''Tests if it deletes the habits'''
    ht = Habit("dance", "NULL", "NULL")
    assert database.delete_habit('dance') == print(f"Habit '{ht.name}' successfully deleted.")
    ht = Habit("paint", "NULL", "NULL")
    assert database.delete_habit('paint') == print(f"Habit '{ht.name}' successfully deleted.")

def teardown(database):
    yield database
    database.clear()