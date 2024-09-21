import subprocess

# Running first script
process1 = subprocess.Popen(['python', 'main_ui.py'])

# Running second script
process2 = subprocess.Popen(['python', 'look_ahead.py'])

# Wait for both processes to complete
process1.wait()
process2.wait()

print("Both scripts completed! The CSV files have been generated.")