from storage_handler import *

tracker = HabitTracker('habit.db')
tracker.create_table()

def preload_habits():
    '''Insert default habits if none exist already.'''
    tracker.cursor.execute("SELECT COUNT(*) FROM habit")
    count = tracker.cursor.fetchone()[0]
    if count == 0:
        default_habits = [
        ('Read', 'Read 15 mins', 'daily', '2025-10-25, 15:12', '2025-10-27, 02:56', 3),
        ('Grocery Shopping', '1 hour', 'weekly', '2025-09-05, 01:01', '2025-10-24, 12:00', 1), # 8 Weeks of Weekly Habit tracking with 1 week break
        ('Meal Prep', 'Meal prep weekly', 'weekly', '2025-09-05, 01:02', '2025-10-24, 13:00', 8), # 8 Weeks of Weekly Habit tracking.
        ('Walk', 'To improve mindset', 'daily', '2025-10-13, 20:21', '2025-11-11, 17:49', 30), # 4 Weeks of Daily Habit tracking.
        ]
        for habit in default_habits:
            tracker.cursor.execute('INSERT INTO habit(name, description, duration, creation_date, last_completed_date, streak) VALUES (?, ?, ?, ?, ?, ?)', habit)
        tracker.db.commit()


def marking_habits():
    '''Marks habit complete for the default habits.'''
    tracker.cursor.execute("SELECT COUNT(*) FROM progress")
    count = tracker.cursor.fetchone()[0]
    if count == 0:
        default_habits = [

        # 3-day daily streak:
        ('Read', '2025-10-26, 00:45'),
        ('Read', '2025-10-27, 02:56'),
        ('Read', '2025-10-25, 16:12'),

        # 8-week weekly streak:
        ('Meal Prep', '2025-09-05, 12:30'),
        ('Meal Prep', '2025-09-12, 15:48'),
        ('Meal Prep', '2025-09-19, 17:20'),
        ('Meal Prep', '2025-09-26, 19:30'),
        ('Meal Prep', '2025-10-03, 14:00'),
        ('Meal Prep', '2025-10-10, 10:10'),
        ('Meal Prep', '2025-10-17, 18:40'),
        ('Meal Prep', '2025-10-24, 13:00'),
        

        #8-week weekly streak with 1 week streak break:
        ('Grocery Shopping', '2025-09-05, 11:00'),
        ('Grocery Shopping', '2025-09-12, 14:10'),
        ('Grocery Shopping', '2025-09-26, 18:00'),
        ('Grocery Shopping', '2025-10-03, 13:50'),
        ('Grocery Shopping', '2025-10-10, 09:13'),
        ('Grocery Shopping', '2025-10-17, 17:27'),
        ('Grocery Shopping', '2025-10-24, 12:00'),
        

        #for 4 Weeks of daily Habit tracking.
        ('Walk', '2025-10-13, 22:17'),
        ('Walk', '2025-10-14, 19:08'),
        ('Walk', '2025-10-15, 23:00'),
        ('Walk', '2025-10-16, 17:23'),
        ('Walk', '2025-10-17, 12:47'),
        ('Walk', '2025-10-18, 08:59'),
        ('Walk', '2025-10-19, 07:57'),
        ('Walk', '2025-10-20, 16:11'),
        ('Walk', '2025-10-21, 21:09'),
        ('Walk', '2025-10-22, 09:15'),
        ('Walk', '2025-10-23, 09:24'),
        ('Walk', '2025-10-24, 15:12'),
        ('Walk', '2025-10-25, 24:01'),
        ('Walk', '2025-10-26, 12:28'),
        ('Walk', '2025-10-27, 10:10'),
        ('Walk', '2025-10-28, 13:43'),
        ('Walk', '2025-10-29, 16:17'),
        ('Walk', '2025-10-30, 22:18'),
        ('Walk', '2025-10-31, 18:45'),
        ('Walk', '2025-11-01, 17:17'),
        ('Walk', '2025-11-02, 19:39'),
        ('Walk', '2025-11-03, 21:04'),
        ('Walk', '2025-11-04, 12:00'),
        ('Walk', '2025-11-05, 14:13'),
        ('Walk', '2025-11-06, 13:40'),
        ('Walk', '2025-11-07, 23:08'),
        ('Walk', '2025-11-08, 11:15'),
        ('Walk', '2025-11-09, 12:38'),
        ('Walk', '2025-11-10, 10:20'),
        ('Walk', '2025-11-11, 17:49'),
        ]
        for habit in default_habits:
            tracker.cursor.execute('INSERT INTO progress(name, last_checked) VALUES (?, ?)', habit)
    tracker.db.commit()


def delete_data():
    '''Deletes pre-load habits.'''
    tracker.cursor.execute("SELECT COUNT(*) FROM habit")
    count = tracker.cursor.fetchone()[0]
    if count != 0:
        default_habits = [
        ('Read'),
        ('Grocery Shopping'),
        ('Meal Prep'),
        ('Walk'),
        ]
        for habit in default_habits:
            tracker.cursor.execute('DELETE FROM habit WHERE name = ?', (habit,))
    tracker.db.commit()
