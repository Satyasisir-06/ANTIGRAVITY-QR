import sqlite3
import json
from datetime import datetime, timedelta

def get_db_connection():
    conn = sqlite3.connect('attendance.db')
    conn.row_factory = sqlite3.Row
    return conn

def debug_analytics():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 1. Attendance Trends (Last 7 Days)
    dates = []
    present_counts = []
    absent_counts = []
    
    for i in range(6, -1, -1):
        d = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        p = cur.execute("SELECT COUNT(*) FROM attendance WHERE date = ? AND status = 'PRESENT'", (d,)).fetchone()[0]
        a = cur.execute("SELECT COUNT(*) FROM attendance WHERE date = ? AND status = 'ABSENT'", (d,)).fetchone()[0]
        dates.append(d)
        present_counts.append(p)
        absent_counts.append(a)
        
    # 2. Branch Performance (Dynamic)
    branch_rows = cur.execute("SELECT DISTINCT branch FROM students WHERE branch IS NOT NULL AND branch != ''").fetchall()
    branches = sorted([r[0] for r in branch_rows])
    if not branches:
        branches = ['CSM', 'CSD', 'CSE-A', 'CSE-B', 'CSE-C', 'CSE-D', 'CIVIL', 'MECH', 'ECE', 'EEE']
        
    branch_data = []
    for b in branches:
        total = cur.execute("SELECT COUNT(*) FROM attendance WHERE LOWER(branch) = LOWER(?)", (b,)).fetchone()[0]
        if total == 0:
            branch_data.append(0)
        else:
            present = cur.execute("SELECT COUNT(*) FROM attendance WHERE LOWER(branch) = LOWER(?) AND status = 'PRESENT'", (b,)).fetchone()[0]
            pct = round((present / total) * 100, 1)
            branch_data.append(pct)
            
    conn.close()
    
    result = {
        'trends': {
            'labels': dates,
            'present': present_counts,
            'absent': absent_counts
        },
        'branches': {
            'labels': branches,
            'data': branch_data
        }
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    debug_analytics()
