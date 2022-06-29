
class Player:
    def __init__(self, name):
        self.name = name
        # Extra details can be added such as address, mobile, email etc


class Team:     # Playing Team
    def __init__(self, name):
        self.name = name
        self.players = []

    def add_player(self, player):
        self.players.append(player)


class BallType:
    NORMAL, WIDE, WICKET = 1, 2, 3


class Ball:
    def __init__(self, played_by, balled_by=None, ball_type=BallType.NORMAL, runs=0):
        self.played_by = played_by
        self.balled_by = balled_by      # Currently balled by is None as in example there is no way to enter baller
        self.type = ball_type
        self.runs = runs

    def throw(self):
        result = input()
        try:
            self.runs = int(result)
        except ValueError:
            if result == 'W':
                self.type = BallType.WICKET
            elif result == 'Wd':
                self.type = BallType.WIDE
                self.runs = 1


class Over:
    def __init__(self, number):
        self.number = number
        self.balls = []
        # Extra details can be added such as score, wickets, dot ball etc in a over

    def add_ball(self, ball):
        self.balls.append(ball)

    def begin(self, first_batsman, second_batsman, runs_needed, inning):
        balls = 0
        while balls < 6:
            balls += 1
            ball = Ball(inning.team.players[first_batsman])
            ball.throw()
            self.add_ball(ball)

            runs = ball.runs
            inning.total_runs += runs
            current_player_board = inning.stats[inning.team.players[first_batsman]]

            if ball.type == BallType.NORMAL:
                current_player_board['score'] += runs
                current_player_board['balls'] += 1
                if runs % 2 == 1:
                    first_batsman, second_batsman = second_batsman, first_batsman
                elif runs == 4:
                    current_player_board['4s'] += 1
                elif runs == 6:
                    current_player_board['6s'] += 1

            elif ball.type == BallType.WICKET:
                current_player_board['balls'] += 1
                first_batsman = max(first_batsman, second_batsman) + 1
                inning.wickets += 1

            elif ball.type == BallType.WIDE:
                balls -= 1

            if inning.wickets == match.no_of_players - 1 or inning.total_runs >= runs_needed:
                break

        return second_batsman, first_batsman


class Match:
    INNING_COUNT = 2

    def __init__(self):
        self.teams = []
        self.innings = []
        self.no_of_players = 0
        self.no_of_overs = 0
        # Extra details can be added such as empires, commentary, inning stats etc

    def add_team(self, team):
        self.teams.append(team)

    def add_inning(self, inning):
        self.innings.append(inning)

    def validate(self):
        if self.no_of_players < 2:
            raise Exception("Minimum 2 players are required.")
        if self.no_of_overs < 1:
            raise Exception("Minimum 1 over is required.")

    def start(self):
        print("No of players for each team")
        self.no_of_players = int(input())

        print("No of overs")
        self.no_of_overs = int(input())

        self.validate()

        for i in range(self.INNING_COUNT):
            print("\n Batting order for team {0}".format(i + 1))
            team = Team('team_{0}'.format(str(i + 1)))
            self.add_team(team)

            for j in range(match.no_of_players):
                name = str(input())
                team.add_player(Player(name))

            inning = Inning(i + 1, team)
            if i > 0:
                inning.play(runs_needed=self.innings[-1].total_runs + 1)
            else:
                inning.play()
            self.add_inning(inning)

        if self.innings[0].total_runs > self.innings[1].total_runs:
            print('Result: Team 1 won the match by {0} runs'.format(self.innings[0].total_runs - self.innings[1].total_runs))
        elif self.innings[0].total_runs == self.innings[1].total_runs:
            print('Result: Its a tie')
        else:
            print('Result: Team 2 won the match by {0} wickets'.format(self.no_of_players - self.innings[1].wickets))


class Inning:
    def __init__(self, number, team):
        self.number = number
        self.team = team        # batting team
        self.total_runs = 0
        self.wickets = 0
        self.overs = []
        self.stats = {}         # Batsmen stats
        # Extra details can be added such as baller stats

    def initialize_player_stats(self):
        self.stats = {i: {'score': 0, '4s': 0, '6s': 0, 'balls': 0} for i in self.team.players}

    def add_over(self, over):
        self.overs.append(over)

    def get_no_of_balls_played(self):
        cnt = 0
        for i in self.overs[-1].balls:
            if i.type in (BallType.NORMAL, BallType.WICKET):
                cnt += 1
        return (6 * (len(self.overs) - 1)) + cnt

    def print_scorecard(self, first, second):
        balls = self.get_no_of_balls_played()
        print('Scorecard for team {0}'.format(self.team.name))
        print('Player Name      Score       4s      6s      balls')
        for player, values in self.stats.items():
            print('{0}{5}                  {1}         {2}         {3}         {4}'.
                  format(player.name, values['score'], values['4s'], values['6s'], values['balls'],
                         '*' if (first < len(self.team.players) and player == self.team.players[first]) or (
                                     second < len(self.team.players) and player == self.team.players[second]) else ''
                         )
                  )
        print('Total: {0}/{1}'.format(self.total_runs, self.wickets))
        print('Overs: {0}.{1}'.format(int(balls / 6), balls % 6))

    def play(self, runs_needed=1000000):
        self.initialize_player_stats()
        first_batsman = 0
        second_batsman = 1

        for over_number in range(match.no_of_overs):
            print('\n Over {0}:'.format(over_number + 1))
            over = Over(over_number + 1)
            first_batsman, second_batsman = over.begin(first_batsman, second_batsman, runs_needed, self)
            self.add_over(over)
            self.print_scorecard(first_batsman, second_batsman)
            if self.wickets == match.no_of_players - 1:
                break


if __name__ == '__main__':
    try:
        match = Match()
        match.start()
    except Exception as e:
        print(str(e))
