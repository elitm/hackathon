from Client import Client
import threading



run_threads = True
thread_number = 2

team_name = "ElitAndShira"
team_name1 = "Apolo"

client = Client(team_name)
client1 = Client(team_name1)
# client.run()

threading.Thread(target=client.run()).start()
threading.Thread(target=client1.run()).start()


# if not run_threads:
#     # run on main thread
#     client.run()
#     client1.run()
#
#
# else:
#     # run thread
#     for i in range(thread_number):
#         start_new_thread(client.run())
#         start_new_thread(client1.run())
#
#     try:
#         time.sleep(120)
#     except Exception as e:
#         pass
