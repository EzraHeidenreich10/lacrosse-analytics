# CONSTANTS
UNSUCCESSFUL_RESULTS = ['no advantage', 'turnover', 'switch']
DODGE_STAT_TYPES = ['dodges', 'wins', 'win percent', 'goals', 'shots', 'assists', 'missed assists', 'turnovers']

# Data organization 
def get_data(file_name: str) -> list:
    """
        Creates a 2d list with all the data in the file, with each row being its own nested list
    """
    # Gathers all data from file and stores it in a 2d list
    file = open(file_name, "r")
    everything = file.readlines()
    
    num_rows = len(everything)
    data = []

   # Clean up data in everything 
    for i in range(num_rows): 
        data.append([])
        row_data = everything[i].split('\t') 

        for j in range(len(row_data)):  
            row_data[j] = row_data[j].strip() 
            data[i].append(row_data[j].lower())
    
    return data

def get_player_list(file_name: str) -> list:
    """
        Creates a list of players that have appeared in the ball carrier column
    """
    data = get_action_dict(file_name)['dodge']
    players = []

    for row in data:
        player = row[1]

        if player not in players:
            players.append(player)
    
    return players

def get_duo_list(file_name: str) -> list:
    """
        Creates a list of duos that have performed a pick (First player is ball carrier, second is picker)
    """
    picks = get_action_dict(file_name)['pick']

    duos = []

    for pick in picks:             
        duo = (pick[1], pick[3])
        rev_duo = (pick[3], pick[1])

        if rev_duo in duos:
            pass
        elif duo not in duos:      
            duos.append(duo)
        
    return duos


#NEW FUNCTION
def get_action_dict(file_name: str) -> dict[str, list[str]]:
    """
        Get a dictionary of all occurences of the given action
    """
    data = get_data(file_name)
    action_d = {}

    for elem in data:
        if elem[0] in action_d:
            action_d[elem[0]].append(elem)
        else:
            action_d[elem[0]] = [elem]
    
    return action_d
    
def create_player_dict(file_name: str) -> dict:
    """
        Creates a dictionary of every stat for every player
    """
    players = get_player_list(file_name)
    stats_d = {}


     # Iterate through each player in player list and find their stats, then add to dictionary
    for player in players:
        stats = create_player_stat_list(file_name, player)

        stats_d[player] = stats
    
    return stats_d

def create_duo_dict(file_name: str) -> dict:
    """
        Creates a dictionary of every stat for every duo
    """
    duos = get_duo_list(file_name)
    stats_d = {}


     # Iterate through each player and find their stats, then add to dictionary
    for duo in duos:
        stats = create_duo_stat_list(file_name, duo)

        stats_d[duo] = stats
    
    return stats_d

def create_player_stat_list(file_name: str, player: str) -> list:
    """
        Creates a list of a player's stats
    """
    all_actions = get_action_dict(file_name)
    
    # Retrieve the value for each stat
    dodges = count_player_actions(all_actions, player)['dodge']
    wins = count_successful_dodges(file_name, player)
    win_percent = round(wins / dodges * 100, 2)
    goals = count_stat(file_name, player, 'dodge', 'goal') 
    shots = count_stat(file_name, player, 'dodge', 'shot') + goals
    asst = count_stat(file_name, player, 'dodge', 'assist')
    miss_asst = count_stat(file_name, player, 'dodge', 'missed assist')
    turnovers = count_stat(file_name, player, 'dodge', 'turnover')

    # Create a list containing each stat
    stats = [dodges, wins, f"{win_percent}%", goals, shots, asst, miss_asst, turnovers]

    return stats

def create_duo_stat_list(file_name: str, duo: tuple) -> list:
    """
        Creates a list of a duo's stats
    """
    # Retrieve the value for each stat
    picks = count_picks(file_name, duo)
    wins = count_successful_picks(file_name, duo)
    win_percent = round(wins / picks, 2) * 100
    goals = count_stat(file_name, duo, 'pick', 'goal') 
    shots = count_stat(file_name, duo, 'pick', 'shot') + goals
    asst = count_stat(file_name, duo, 'pick', 'assist')
    miss_asst = count_stat(file_name, duo, 'pick', 'missed assist')
    turnovers = count_stat(file_name, duo, 'pick', 'turnover')

    # Create a list containing each stat
    stats = [picks, wins, f"{win_percent}%", goals, shots, asst, miss_asst, turnovers]

    return stats


def count_player_actions(all_actions: dict[str, list[str]], player: str) -> dict[str, int]:
    """
        Counts occurences of each action for given player
    """
    action_d = {}

    for action in all_actions:
        count = 0
        for elem in all_actions[action]:
            if player == elem[1]:
                count += 1
        action_d[action] = count
    
    return action_d
                


def count_picks(file_name: str, target_duo: tuple) -> int:
    """
        Counts the number of picks for given target duo
    """
    picks = get_action_dict(file_name)['pick']
    num_picks = 0
    
    for pick in picks:
        # Create a tuple for the current duo of the current pick
        ball_carrier = pick[1]
        picker = pick[3]
        current_duo = (ball_carrier, picker)
        rev_duo = (picker, ball_carrier)

        # Add to pick total if current duo matches target duo
        if current_duo == target_duo or rev_duo == target_duo:
            num_picks += 1
            
        
    return num_picks

def count_successful_dodges(file_name: str, player: str) -> int:
    """
        Counts the number of successful dodges for the given player
    """
    all_actions = get_action_dict(file_name)
    successful = count_player_actions(all_actions, player)['dodge']

    for dodge in all_actions['dodge']:
        current_player = dodge[1]
        result = dodge[5]

        # Check if current player is same as target player and result is unsuccessful
        if  current_player == player and result in UNSUCCESSFUL_RESULTS:
            successful -= 1
        
    
    return successful

def count_successful_picks(file_name: str, target_duo: tuple) -> int:
    """
        Count the number of successful picks for a duo
    """
    all_actions = get_action_dict(file_name)   
    successful = 0
    
    for pick in all_actions['pick']:
        duo = (pick[1], pick[3])            
        result = pick[5]

        # If current duo is the same as target duo and result was successful, add to successful count
        if duo == target_duo and result not in UNSUCCESSFUL_RESULTS:
            successful += 1
    
    return successful  

def count_stat(file_name: str, player: str|tuple, action: str, stat: str) -> int:
    """
        Counts the given stat for the player after performing a dodge or pick
    """
    # Gets a list of every occurence of the correct action
    all_actions = get_action_dict(file_name)[action]
    stat_total = 0
    
    for elem in all_actions:
        # Creates a variable to check if player is correct, if action is pick, correct_player is a duo, else its a singular player
        if action == 'pick':                        
            correct_player = (elem[1], elem[3])    
        else:
            correct_player = elem[1]
            
        # If player is correct and if the stat occurs, adds one to stat total
        if correct_player == player and elem[5] == stat:    

            stat_total += 1
    
    return stat_total


def write_dodge_data_in_file(file_name: str) -> None:
    """
        Writes all player dodge data in a file
    """
    print(f"Updating file 'dodge_stats.txt' using data from '{file_name}'...")
    output = open("dodge_stats.txt", 'w')

    stats_d = create_player_dict(file_name)
    
    for player, stats in stats_d.items():
        output.write(f"{player} {stats[0]} {stats[1]} {stats[2]} {stats[3]} {stats[4]} {stats[5]} {stats[6]} {stats[7]} \n")
    
    output.close()
    print("File updated.\n")

def write_pick_data_in_file(file_name: str) -> None:
    """
        Writes all duo pick data in a file
    """
    print(f"Updating file 'pick_stats.txt' using data from '{file_name}'...")
    output = open("pick_stats.txt", 'w')

    stats_d = create_duo_dict(file_name)
    
    for duo, stats in stats_d.items():
        player1 = duo[0]
        player2 = duo[1]
        output.write(f"{player1} {player2} {stats[0]} {stats[1]} {stats[2]} {stats[3]} {stats[4]} {stats[5]} {stats[6]} {stats[7]} \n")
    
    output.close()

    print("File updated.\n")


def main():
    file = 'raw_data.txt'
    write_dodge_data_in_file(file)
    write_pick_data_in_file(file)
    
    
    
    

if __name__ == "__main__":
    main()



