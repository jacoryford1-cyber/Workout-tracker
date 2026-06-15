import sqlite3
from datetime import datetime
import json

# Database setup
def setup_database():
    """Create the database and tables if they don't exist"""
    conn = sqlite3.connect('workouts.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise TEXT NOT NULL,
            weight INTEGER,
            reps INTEGER,
            date TEXT NOT NULL,
            notes TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

# Log a workout
def log_workout(conn, cursor, exercise, weight, reps, notes=""):
    """Add a new workout to the database"""
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO workouts (exercise, weight, reps, date, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (exercise, weight, reps, date, notes))
    conn.commit()
    print(f"✅ Logged: {exercise} - {weight}lbs x {reps} reps")

# View all workouts
def view_workouts(cursor):
    """Display all logged workouts"""
    cursor.execute('SELECT id, exercise, weight, reps, date FROM workouts ORDER BY date DESC')
    workouts = cursor.fetchall()
    
    if not workouts:
        print("No workouts logged yet!")
        return
    
    print("\n" + "="*70)
    print(f"{'ID':<5} {'Exercise':<15} {'Weight':<10} {'Reps':<8} {'Date':<25}")
    print("="*70)
    
    for workout in workouts:
        print(f"{workout[0]:<5} {workout[1]:<15} {workout[2]:<10} {workout[3]:<8} {workout[4]:<25}")
    print("="*70 + "\n")

# Get stats for a specific exercise
def get_exercise_stats(cursor, exercise):
    """Get statistics for a specific exercise"""
    cursor.execute('''
        SELECT weight, reps, date FROM workouts 
        WHERE exercise = ? 
        ORDER BY date DESC
    ''', (exercise,))
    
    stats = cursor.fetchall()
    if not stats:
        print(f"No workouts found for {exercise}")
        return
    
    print(f"\n📊 Stats for {exercise}:")
    print(f"Total workouts: {len(stats)}")
    
    weights = [s[0] for s in stats if s[0] is not None]
    if weights:
        print(f"Max weight: {max(weights)}lbs")
        print(f"Latest weight: {weights[0]}lbs")
    
    for i, (weight, reps, date) in enumerate(stats[:5]):
        print(f"  {i+1}. {weight}lbs x {reps} reps on {date}")

# Delete a workout
def delete_workout(conn, cursor, workout_id):
    """Delete a workout by ID"""
    cursor.execute('DELETE FROM workouts WHERE id = ?', (workout_id,))
    conn.commit()
    print(f"✅ Deleted workout #{workout_id}")

# Main menu
def main():
    """Main application loop"""
    conn, cursor = setup_database()
    
    print("\n🏋️  WORKOUT TRACKER 💪")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Log a workout")
        print("2. View all workouts")
        print("3. Get stats for an exercise")
        print("4. Delete a workout")
        print("5. Exit")
        
        choice = input("\nChoose an option (1-5): ").strip()
        
        if choice == "1":
            exercise = input("Exercise name: ").strip()
            try:
                weight = int(input("Weight (lbs): "))
                reps = int(input("Reps: "))
                notes = input("Notes (optional): ").strip()
                log_workout(conn, cursor, exercise, weight, reps, notes)
            except ValueError:
                print("❌ Please enter valid numbers for weight and reps")
        
        elif choice == "2":
            view_workouts(cursor)
        
        elif choice == "3":
            exercise = input("Exercise name: ").strip()
            get_exercise_stats(cursor, exercise)
        
        elif choice == "4":
            try:
                workout_id = int(input("Workout ID to delete: "))
                delete_workout(conn, cursor, workout_id)
            except ValueError:
                print("❌ Please enter a valid ID")
        
        elif choice == "5":
            print("\n👋 Thanks for working out! See you next time!")
            conn.close()
            break
        
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()
