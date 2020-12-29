import time
from Client import Client
from _thread import start_new_thread


run_threads = True
thread_number = 10

team_name = "ElitAndShira"
team_name_space = team_name + (" " * (32 - len(team_name)))

client = Client(team_name_space)

if not run_threads:
    # run on main thread
    client.run()

else:
    # run thread
    for i in range(thread_number):
        start_new_thread(client.solve_hash, ())

    try:
        time.sleep(120)
    except Exception as e:
        pass
