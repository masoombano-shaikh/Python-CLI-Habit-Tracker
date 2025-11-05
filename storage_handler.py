import sqlite3
from datetime import *

class UI_decorator:
    '''Functions:
    suffix and prefix: used for adding a separator between 2 statements.
    enter: Header for the Main Menu of the Habit Tracker.
    menu: Header for the Analyse Menu for the Habit Tracker.
    '''
    def suffix():
        print("--------\n")

    def prefix():
        print("--------")

    def enter():
        print("\n----| Habit Tracker |----\n")

    def menu():
        print("\n---- Analyse Habits ----")




class HabitTracker:
    '''Contains core database-related functions.'''

    def __init__(self, db_name='habit.db'):
        '''Method to create and maintain the database connection;
        also contains the function call for creation of the tables in the database.'''
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()
        self.create_table()


    def create_table(self):
        '''Creates the habit and progress table for the habit tracker, if it doesn't exist.'''
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS habit (
                name TEXT PRIMARY KEY,
                description TEXT,
                duration TEXT NOT NULL,
                creation_date TEXT NOT NULL,
                last_completed_date TEXT DEFAULT 0,
                streak INTEGER DEFAULT 0
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS progress(
                name TEXT,
                last_checked TEXT,
                FOREIGN KEY (name) REFERENCES habit(name) ON DELETE CASCADE
            )
        ''')
        self.db.commit()


    def verification(self, name):
        '''This function verifies whether the entered habit name exists in the database.'''
        try:
            self.cursor.execute("SELECT name FROM habit WHERE name = ?", (name,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def add_habit(self, name, description, duration, creation_date, streak):
        '''Adds a new habit to the database.
        Param:
        name = Name of the habit,
        description = Description or detail for the habit,
        duration = Periodicity of the habit, can be selected from: daily or weekly,
        creation Date = Date and Timestamp(24-Hour Clock) of the created habit,
        streak = Current streak(Number of days for which the habit has been constant), which in beginning is 0.
        '''
        try:
            name_check = self.verification(name)
            if name_check:
                UI_decorator.prefix()
                print(f"Habit '{name}' already exists!")
                UI_decorator.suffix()
            else:
                self.cursor.execute('INSERT INTO habit(name, description, duration, creation_date, streak) VALUES (?, ?, ?, ?, ?)', (name, description, duration, creation_date, streak))
                self.db.commit()
                UI_decorator.prefix()
                print(f"Habit '{name}' successfully added!")
                UI_decorator.suffix()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def mark_habit(self, name, today):
            '''Adds a record for marking the habit complete.
            Param:
            name = Name of the existing habit in the database,
            today(date) = Current date which will be added for the mark of habit completion.
            '''
            self.cursor.execute("INSERT INTO progress (name, last_checked) VALUES (?, ?)", (name, today))
            self.update_habit_for_last_checked(today, name)
            self.db.commit()

    def delete_habit(self, name):
        '''Deletes a habit from the database.
        Param:
        name = Name of the existing habit in the database.
        '''
        try:
            name_check = self.verification(name)
            if name_check:
                self.cursor.execute('DELETE FROM habit WHERE name = ?', (name,))
                self.db.commit()
                self.cursor.execute('DELETE FROM progress WHERE name = ?', (name,))
                self.db.commit()
                UI_decorator.prefix()
                print(f"Habit '{name}' successfully deleted.")
                UI_decorator.suffix()
            else:
                    UI_decorator.prefix()
                    print(f"Habit '{name}' not found!")
                    UI_decorator.suffix()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def save_all(self):
        '''Retrieves the saved habit data.'''
        self.cursor.execute("SELECT * FROM habit")
        return self.cursor.fetchall()


    def check_daily_habit(self, name):
        '''Checks current streak, marks if its a new record; or alerts
        if the habit is completed for the day and calculates the current streak'''
        try:
            name_check = self.verification(name)
            if name_check:
                today = date.today()
                last = self.get_last_checked(name)
                last1 = [i[0] for i in last]
                current_date = datetime.now().strftime('%Y-%m-%d, %H:%M')
                if last1 == []:
                    self.mark_habit(name, current_date)
                    self.calculate_daily_habit(name)
                    UI_decorator.prefix()
                    print(f"Habit '{name}' marked complete for today!")
                    UI_decorator.suffix()
                else:
                    last_check = datetime.strptime(last1[-1], '%Y-%m-%d, %H:%M').date()
                    if today - last_check < timedelta(days=1):
                        UI_decorator.prefix()
                        print(f"Habit '{name}' already marked complete for today!")
                        UI_decorator.suffix()
                    elif today - last_check < timedelta(days=2):
                        self.mark_habit(name, current_date)
                        self.calculate_daily_habit(name)
                        UI_decorator.prefix()
                        print(f"Habit '{name}' marked complete for today!")
                        UI_decorator.suffix()
                    else:
                        self.mark_habit(name, current_date)
                        self.calculate_daily_habit(name)
                        UI_decorator.prefix()
                        print(f"Streak started again for habit '{name}' and marked complete for today!")
                        UI_decorator.suffix()
            else:
                UI_decorator.prefix()
                print(f"Habit '{name}' not found!")
                UI_decorator.suffix()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def update_habit_for_streak(self, streak, name):
        '''Updates the value of streak in the habit table.'''
        self.cursor.execute("UPDATE habit SET streak = ? WHERE name = ?", (streak, name))
        self.db.commit()

    def get_last_completed_date(self, name):
        '''Returns the last completed date for a habit from the habit table.'''
        self.cursor.execute("SELECT last_completed_date FROM habit WHERE name=?", (name,))
        return self.cursor.fetchall()

    def get_duration(self, name):
        '''Returns duration of a specified habit from the habit table.'''
        self.cursor.execute("SELECT duration FROM habit WHERE name=?", (name,))
        return self.cursor.fetchall()

    def get_streak(self, name):
        '''Returns streak value from habit table.'''
        self.cursor.execute("SELECT streak FROM habit WHERE name=?", (name,))
        return self.cursor.fetchall()

    def update_habit_for_last_checked(self, today, name):
        '''Updates the last completed date of existing habit in the habit table.'''
        self.cursor.execute("UPDATE habit SET last_completed_date = ? WHERE name = ?", (today, name))
        self.db.commit()

    def get_last_checked(self, name):
        '''Returns last completed date from progress table.'''
        self.cursor.execute("SELECT DISTINCT last_checked FROM progress WHERE name = ? ORDER BY last_checked DESC",(name,))
        return self.cursor.fetchall()

    def check_weekly_habit(self, name):
        '''Checks current streak, marks if its a new record; or alerts
        if the habit is completed for the week and calculates the current
        streak for the weekly habit'''
        
        try:
            name_check = self.verification(name)
            if name_check:
                today = date.today()
                last = self.get_last_checked(name)
                last1 = [i[0] for i in last]
                current_date = datetime.now().strftime('%Y-%m-%d, %H:%M')
                if last1 == []:
                    self.mark_habit(name, current_date)
                    self.calculate_weekly_habit(name)
                    UI_decorator.prefix()
                    print(f"Habit '{name}' marked complete for this week!")
                    UI_decorator.suffix()
                else:
                    last_check = datetime.strptime(last1[-1], '%Y-%m-%d, %H:%M').date()
                    if today - last_check < timedelta(days=7):
                        UI_decorator.prefix()
                        print(f"Habit '{name}' already marked complete for this week!")
                        UI_decorator.suffix()
                        self.calculate_weekly_habit(name)
                    elif today - last_check < timedelta(days=8):
                        self.mark_habit(name, current_date)
                        self.calculate_weekly_habit(name)
                        UI_decorator.prefix()
                        print(f"Habit '{name}' marked complete for this week!")
                        UI_decorator.suffix()
                    else:
                        self.mark_habit(name, current_date)
                        self.calculate_weekly_habit(name)
                        UI_decorator.prefix()
                        print(f"Streak started again for habit '{name}' and marked complete for week!")
                        UI_decorator.suffix()
            else:
                UI_decorator.prefix()
                print(f"Habit '{name}' not found!")
                UI_decorator.suffix()
        except sqlite3.Error as e:
            print(f"Database error: {e}")


    def calculate_weekly_habit(self, name):
        '''Calculates the current streak value for weekly habit using
        the last streak value existing in the habit table, then updates
        the habit table with the updated streak value.'''
        try:
            name_check = self.verification(name)
            if name_check:
                logs = self.get_last_checked(name)
                completions = [datetime.strptime(row[0], '%Y-%m-%d, %H:%M') for row in logs]
                if not completions:
                    self.update_habit_for_streak(0, name)
                current_streak = 0
                completions.sort()
                for i in range(len(completions)):
                    if i == 0:
                        current_streak = 1
                    else:
                        prev_week_start = completions[i-1] - timedelta(days=completions[i-1].weekday())
                        current_week_start = completions[i] - timedelta(days=completions[i].weekday())
                        if current_week_start == prev_week_start + timedelta(weeks=1):
                            current_streak += 1
                        elif current_week_start != prev_week_start:
                            current_streak = 1
                self.update_habit_for_streak(current_streak, name)
            else:
                UI_decorator.prefix()
                print(f"Habit '{name}' not found!")
                UI_decorator.suffix()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def calculate_daily_habit(self, name):
        '''Calculates the current streak value for daily habit using
        the last streak value existing in the habit table, then updates
        the habit table with the updated streak value.'''
        try:
            name_check = self.verification(name)
            if name_check:
                logs = self.get_last_checked(name)
                today = datetime.now().strftime('%Y-%m-%d, %H:%M')
                expected_date = datetime.strptime(today, '%Y-%m-%d, %H:%M')
                completion_dates = [row[0] for row in logs]
                if not completion_dates:
                    self.update_habit_for_streak(0, name)
                current_streak = 0
                for date_str in completion_dates:
                    completed_date = datetime.strptime(date_str, '%Y-%m-%d, %H:%M')
                    if completed_date == expected_date:
                        current_streak += 1
                        expected_date -= timedelta(days=1)
                    else:
                        current_streak = 1
                        break
                self.update_habit_for_streak(current_streak, name)
            else:
                UI_decorator.prefix()
                print(f"Habit '{name}' not found!")
                UI_decorator.suffix()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def get_habits_by_duration(self, duration):
        '''Returns existing habits from the habit table
        as per their duration[daily or weekly]'''
        self.cursor.execute("SELECT * FROM habit WHERE duration = ?", (duration,))
        return self.cursor.fetchall()

    def get_longest_streak_of_all_habits(self):
        '''Returns the longest streak of all the habits.'''
        self.cursor.execute("SELECT progress.name, COUNT(progress.last_checked), habit.streak FROM progress JOIN habit ON habit.name = progress.name GROUP BY progress.name")
        return self.cursor.fetchall()

    def get_longest_streak_from_all(self):
        '''Returns the longest streak from all the habits in the habit table.'''
        self.cursor.execute("WITH T AS (SELECT name, COUNT(last_checked) AS streak_temp FROM progress GROUP BY name) SELECT name, MAX(streak_temp) FROM T")
        return self.cursor.fetchall()



    def get_all_habits(self):
        '''Retrieves all habits from the database.'''
        self.cursor.execute('SELECT * FROM habit')
        return self.cursor.fetchall()

    def get_habits(self):
        '''Retrieves selected parameters: name, duration, last completed date, streak) 
        from the habit table.'''
        self.cursor.execute("SELECT name, duration, last_completed_date, streak FROM habit")
        return self.cursor.fetchall()

    def get_logs(self, name):
        '''Returns all the data from progress table.'''
        self.cursor.execute("SELECT * FROM progress WHERE name = ?", (name,))
        return self.cursor.fetchall()
