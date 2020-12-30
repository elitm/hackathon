from Server import Server

team_name = "ElitAndShira" #todo change
team_name_space = team_name + (" " * (32 - len(team_name))) #todo check if 32?

server = Server(team_name_space)
server.run()
