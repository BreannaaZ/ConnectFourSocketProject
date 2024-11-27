import subprocess
import time

# Run the server.py script
server_process = subprocess.Popen(['python', 'server.py'])

# Wait a second to make sure the server started up
time.sleep(1)

# Run two instances of client.py
client1_process = subprocess.Popen(['python', 'client.py'])
client2_process = subprocess.Popen(['python', 'client.py'])

# Wait for the clients to terminate
client1_process.wait()
client2_process.wait()

# End the server when both clients end
server_process.terminate()
