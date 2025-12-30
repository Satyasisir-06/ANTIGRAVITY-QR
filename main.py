import os
import sys

# Add the subfolder to the path so imports work
sys.path.append(os.path.join(os.path.dirname(__file__), 'QR_Attendance'))

from QR_Attendance.app import app, socketio

# Vercel looks for 'app' or 'application'
application = app

if __name__ == "__main__":
    socketio.run(app, debug=True)
