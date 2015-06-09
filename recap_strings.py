# NBA NLP - Senior Project - Spring 2015
# Recap Generator - Template Strings
# Jacob Bustamante

"""
Headline
"""
headline_strings = [
    ("%s defeat the %s with a %s to %s victory in %s.", ['winner_team_name', 'loser_team_name', 'winner_score', 'loser_score', 'home_city']),
    ("The %s edge the %s %s to %s.", ['winner_team_name', 'loser_team_name', 'winner_score', 'loser_score']),
    ("%s win in %s over the %s %s-%s.", ['winner_team_name', 'home_city', 'loser_team_name', 'winner_score', 'loser_score']),
    ("%s win by %s over the %s %s-%s.", ['winner_team_name', 'lead', 'loser_team_name', 'winner_score', 'loser_score']),
    ("%s defeats the %s by %s, %s-%s.", ['winner_city', 'loser_team_name', 'lead', 'winner_score', 'loser_score']),
]

headline_partial_strings = [
    ("The %s hold a %s-%s lead over the %s in the %s.", ['winner_team_name', 'winner_score', 'loser_score', 'loser_team_name', 'quarter_str']),
    ("The %s hold a %s-%s lead over %s in the %s.", ['winner_team_name', 'winner_score', 'loser_score', 'loser_city', 'quarter_str']),
    ("The %s lead the %s in the %s, %s-%s.", ['winner_team_name', 'loser_team_name', 'quarter_str', 'winner_score', 'loser_score']),
    ("The %s lead %s by %s in the %s, %s-%s.", ['winner_team_name', 'loser_city', 'lead', 'quarter_str', 'winner_score', 'loser_score']),
    ("%s leads by %s over the %s in the %s, %s-%s.", ['winner_city', 'lead', 'loser_team_name', 'quarter_str', 'winner_score', 'loser_score']),
    ("%s up %s againts %s, the score is %s-%s in the %s.", ['winner_team_name', 'lead', 'loser_city', 'winner_score', 'loser_score', 'quarter_str']),
]

headline_tied_partial_strings = [
    ("The %s and the %s are tied %s-%s in the %s.", ['winner_team_name', 'loser_team_name', 'winner_score', 'loser_score', 'quarter_str']),
    ("The %s are tied with the %s %s-%s in the %s.", ['winner_team_name', 'loser_team_name', 'winner_score', 'loser_score', 'quarter_str']),
    ("The %s are tied with the %s in the %s at %s a piece.", ['winner_team_name', 'loser_team_name', 'quarter_str', 'winner_score']),
    ("%s and %s are tied %s-%s in the %s.", ['winner_city', 'loser_city', 'winner_score', 'loser_score', 'quarter_str']),
    ("%s is tied with %s %s-%s in the %s.", ['winner_city', 'loser_city', 'winner_score', 'loser_score', 'quarter_str']),
    ("%s is tied with %s in the %s at %s a piece.", ['winner_city', 'loser_city', 'quarter_str', 'winner_score']),
]

"""
Record and standings
"""
record_strings = [
    ("The %s now hold a %s-%s record after that result, while the %s hold a %s-%s record.", ('home_team', 'home_wins', 'home_losses', 'away_team', 'away_wins', 'away_losses')),
    ("The %s are now %s-%s. The %s are at %s-%s after that result.", ('home_team', 'home_wins', 'home_losses', 'away_team', 'away_wins', 'away_losses')),
    ("The result puts %s at %s-%s for the season. The %s are now %s-%s.", ('home_city', 'home_wins', 'home_losses', 'away_team', 'away_wins', 'away_losses')),
]

record_partial_strings = [
    ("The %s currently have a %s-%s record, while the %s hold a %s-%s record.", ('home_team', 'home_wins', 'home_losses', 'away_team', 'away_wins', 'away_losses')),
    ("The %s are %s-%s so far this season. The %s are %s-%s.", ('home_team', 'home_wins', 'home_losses', 'away_team', 'away_wins', 'away_losses')),
]

team_losing_streak_strings = [
    ("It's been a rough last few games for the %s. They've lost their last %s games.", ['team_name', 'num_past_games']),
    ("The %s haven't won in the last %s games.", ['team_name', 'num_past_games']),
    ("The %s have lost their last %s games.", ['team_name', 'num_past_games']),
]

team_winning_streak_strings = [
    ("The %s continue their great streak, winning %s of %s.", ['team_name', 'num_won', 'num_past_games']),
    ("The %s have been playing great these last few games. They've won their last %s.", ['team_name', 'num_past_games']),
    ("The %s have been playing great these last few games, winning their last %s.", ['team_name', 'num_past_games'])
]

team_losing_streak_partial_strings = [
    ("It's been a rough last few games for the %s. They've lost their last %s games.", ['team_name', 'num_past_games']),
    ("The %s haven't won in the last %s games.", ['team_name', 'num_past_games']),
    ("The %s have lost their last %s games.", ['team_name', 'num_past_games']),
]

team_winning_streak_partial_strings = [
    ("The %s are aiming to continue their great streak, winning %s of %s.", ['team_name', 'num_won', 'num_past_games']),
    ("The %s have been playing great these last few games. They've won their last %s games.", ['team_name', 'num_past_games']),
    ("A win here would add to the %s current %s-game winning streak.", ['team_name', 'num_won']),
]

"""
statistics
"""
stat_strings = [
    ("%s scored %s points and got %s assists and %s rebounds for the %s.", ('name', 'points', 'assists', 'rebounds', 'team')),
    ("%s recorded %s points, %s assists, and %s rebounds.", ('name', 'points', 'assists', 'rebounds'))
]


"""
Events
"""

"""
stat event
"""

headline_stat_strings = [
    ("%s scores %s, %s defeat the %s %s to %s", ['last_name', 'stat', 'winner_team_name', 'loser_team_name', 'winner_score', 'loser_score']),
    ("%s puts in %s, %s defeat the %s %s to %s", ['last_name', 'stat', 'winner_team_name', 'loser_team_name', 'winner_score', 'loser_score']),
    ("%s takes down %s, %s win %s to %s", ['last_name', 'loser_team_name', 'winner_team_name', 'winner_score', 'loser_score']),
    ("%s and the %s win over %s, %s-%s", ['last_name', 'winner_team_name', 'loser_city', 'winner_score', 'loser_score']),
    ("%s scores %s, %s defeat the %s by %s, %s to %s", ['last_name', 'stat', 'winner_team_name', 'loser_team_name', 'lead', 'winner_score', 'loser_score']),
    ("%s fall to the %s %s to %s, %s scores %s", ['loser_team_name', 'winner_team_name', 'loser_score', 'winner_score', 'name', 'stat']),
    ("%s lose by %s against %s and the %s, %s-%s", ['loser_team_name', 'lead', 'name', 'winner_team_name', 'loser_score', 'winner_score'])
]

intro_stat_strings = [
    ("%s recorded %s %s for the %s.", ['name', 'stat', 'stat_name', 'team']),
    ("%s scored %s %s for the %s.", ['name', 'stat', 'stat_name', 'team']),
    ("%s put in %s %s for the %s.", ['name', 'stat', 'stat_name', 'team']),
    ("%s %s scored %s %s.", ['team', 'name', 'stat', 'stat_name'])
]

stat_strings = [
    ("%s put in %s points.", ('name', 'points')),
    ("%s scored %s points.", ('name', 'points')),
    ("%s recorded %s points.", ('name', 'points')),
    ("%s scored %s.", ('name', 'points'))
]

stat_details_strings = [
    ("%s recorded %s.", ['last_name', 'assists_and_rebounds']),
    ("%s contributed %s.", ['last_name', 'assists_and_rebounds']),
    ("%s got %s.", ['last_name', 'assists_and_rebounds']),
    ("%s recorded %s for the %s.", ['last_name', 'assists_and_rebounds', 'team']),
    ("%s contributed %s for the %s.", ['last_name', 'assists_and_rebounds', 'team']),
    ("%s got %s for the %s.", ['last_name', 'assists_and_rebounds', 'team']),
]

stat_quarter_strings = [
    ("%s of his points were scored in the %s quarter.", ['high_quarter_points', 'high_quarter']),
    ("%s scored %s of his points in the %s.", ['first_name', 'high_quarter_points', 'high_quarter']),
    ("He recorded %s of his points in the %s.", ['first_name', 'high_quarter_points', 'high_quarter']),
    ("He recorded %s points in the %s.", ['first_name', 'high_quarter_points', 'high_quarter']),
    ("He got %s points in the %s.", ['first_name', 'high_quarter_points', 'high_quarter']),
]

"""
high rating event
"""

headline_high_rating_strings = [
    ("%s scores %s, %s defeat the %s %s to %s", ['last_name', 'stat', 'winner_team_name', 'loser_team_name', 'winner_score', 'loser_score']),
    ("%s puts in %s, %s defeat the %s %s to %s", ['last_name', 'stat', 'winner_team_name', 'loser_team_name', 'winner_score', 'loser_score']),
    ("%s takes down %s, %s win %s to %s", ['last_name', 'loser_team_name', 'winner_team_name', 'winner_score', 'loser_score']),
    ("%s and the %s win over %s, %s-%s", ['last_name', 'winner_team_name', 'loser_city', 'winner_score', 'loser_score']),
    ("%s scores %s, %s defeat the %s by %s, %s to %s", ['last_name', 'stat', 'winner_team_name', 'loser_team_name', 'lead', 'winner_score', 'loser_score']),
    ("%s fall to the %s %s to %s, %s scores %s", ['loser_team_name', 'winner_team_name', 'loser_score', 'winner_score', 'name', 'stat']),
    ("%s lose by %s against %s and the %s, %s-%s", ['loser_team_name', 'lead', 'name', 'winner_team_name', 'loser_score', 'winner_score'])
]

intro_high_rating_strings = [
    ("%s proved key, as he put up %s %s for the %s.", ['name', 'stat', 'stat_name', 'team']),
    ("%s recorded %s %s for the %s.", ['name', 'stat', 'stat_name', 'team']),
    ("%s had a great game, scoring %s %s for the %s.", ['name', 'stat', 'stat_name', 'team'])
]


high_rating_strings = [
    ("%s led the %s in %s with %s %s.", ('first_name', 'team', 'stat_noun', 'stat', 'stat_name'))
]

high_rating_quarter_strings = [
    ("%s of his points were scored in the %s quarter.", ['high_quarter_points', 'high_quarter'])
]

high_rating_details_strings = [
    ("%s also recorded %s.", ['last_name', 'assists_and_rebounds'])
]

"""
high rating leader event
"""

headline_high_rating_leader_strings = [
    ("%s scores %s, %s defeat the %s %s to %s", ['last_name', 'stat', 'winner_team_name', 'loser_team_name', 'winner_score', 'loser_score']),
    ("%s fall to the %s %s to %s, %s scores %s", ['loser_team_name', 'winner_team_name', 'loser_score', 'winner_score', 'name', 'stat'])
]

intro_high_rating_leader_strings = [
    ("%s proved key, as he put up %s %s for the %s.", ['name', 'stat', 'stat_name', 'team']),
    ("%s recorded %s %s for the %s.", ['name', 'stat', 'stat_name', 'team']),
    ("%s had a great game, scoring %s %s for the %s.", ['name', 'stat', 'stat_name', 'team'])
]

high_rating_leader_strings = [
    ("%s led the %s in %s with %s %s.", ('first_name', 'team', 'stat_noun', 'stat', 'stat_name'))
]


"""
high overall stats event
"""

headline_overall_stats_strings = [
    ("%s records %s points, %s assists, %s defeat the %s %s to %s", ['last_name', 'points', 'assists', 'winner_team_name', 'loser_team_name', 'winner_score', 'loser_score'])
]

intro_overall_stats_strings = [
    ("%s performed well for the %s, putting up %s points and %s assists.", ['name', 'team', 'points', 'assists'])
]

overall_stats_strings = [
    ("%s led the %s with %s points, %s assists, and %s rebounds.", ('first_name', 'team', 'points', 'assists', 'rebounds'))
]


"""
high team rating event
"""

headline_high_team_rating_strings = [
    ("%s prove too much for the %s, %s win %s to %s", ['name', 'loser_team_name', 'winner_team_name', 'winner_score', 'loser_score'])
]

intro_high_team_rating_strings = [
    ("%s performed great with %s.", ['name', 'points'])
]

high_team_rating_strings = [
    ("The %s %s made great contributions with %s.", ('team', 'name', 'points'))
]

"""
team rating event
"""

headline_team_rating_strings = [
    ("%s prove too much for the %s, %s win %s to %s", ['name', 'loser_team_name', 'winner_team_name', 'winner_score', 'loser_score'])
]

intro_team_rating_strings = [
    ("%s contributed with %s.", ['name', 'points'])
]

team_rating_strings = [
    ("The %s %s put in %s.", ('team', 'name', 'points'))
]



"""
scoring run event
"""

intro_run_strings = [
    ("A %s and %s %s run in the %s proved crucial in the %s defeat.", ['winning_points', 'losing_points', 'winning_team', 's_quarter', 'losing_team']),
    ("The %s come out on top over the %s, putting up a key %s and %s run in the %s.", ['winning_team', 'losing_team', 'winning_points', 'losing_points', 's_quarter'])
]

scoring_run_strings = [
    ("The %s went on a %s and 0 run in the %s quarter with the %s giving up %s turnovers and %s missed attempts during that time.", ('winning_team', 'winning_points', 's_quarter', 'losing_team', 'turnovers', 'missed_attempts'))
]

run_details_strings = [
    
]


"""
last second shot event
"""

headline_last_second_shot_strings = [
    ("%s's buzzer beater lifts the %s over the %s %s-%s.", ("primary_player", "winning_team", "losing_team", "winner_score", "loser_score"))
]

intro_last_second_shot_strings = [
    ("%s made the winning shot with %s seconds remaining to take a %s-%s lead.", ("primary_player", "seconds", "winner_score", "loser_score"))
]

last_second_shot_strings = [
    ("With %s seconds remaining in the %s, %s put up a late %s to win the game.", ("seconds", "quarter_str", "primary_player", "shot_type"))
]

last_second_shot_details_strings = [
    
]

"""
big lead event
"""

intro_big_lead_strings = [
    ("The %s's biggest lead of the night was by %s with %s minutes remaining in the %s.", ("lead_team", "points_up", "minutes", "quarter_str"))
]

big_lead_strings = [
    ("The %s were up by as much as %s points in the %s with a %s-%s lead.", ("lead_team", "points_up", "quarter_str", "lead_points", "down_points"))
]

big_lead_details_strings = [
    
]


"""
foul out event
"""

headline_foul_out_strings = [
    ("%s fouls out, %s defeat the %s %s to %s", ['last_name', 'winner_team_name', 'loser_team_name', 'winner_score', 'loser_score'])
]

intro_foul_out_strings = [
    ("%s fouled out in %s after recording his sixth foul of the night.", ['last_name', 'quarter_str']),
]

foul_out_strings = [
    ("%s fouled out with %s:%s remaining in %s.", ('last_name', 'quarter', 'minutes', 'quarter_str'))
]


"""
comeback success event
"""

headline_comeback_success_strings = [
    ("The %s comeback from %s down to take a %s-%s win over the %s.", ['comeback_team', 'points_down', 'winner_score', 'loser_score', 'other_team'])
]

intro_comeback_success_strings = [
    ("The %s came back from %s down to win the game.", ['comeback_team', 'points_down'])
]

comeback_success_strings = [
    ("The %s were down by as much as %s points in the %s before they cameback to take the lead.", ('comeback_team', 'points_down', 'quarter_str'))
]

"""
comeback fail event
"""

headline_comeback_fail_strings = [
    ("%s come short, %s hold on to %s-%s lead.", ['comeback_team', 'other_team', 'winner_score', 'loser_score'])
]

intro_comeback_fail_strings = [
    ("The %s win by just %s, after %s cut %s point lead.", ['other_team', 'lead', 'comeback_team', 'points_down'])
]

comeback_fail_strings = [
    ("The %s were down by as much as %s points in the %s before they closed the gap to just %s.", ('comeback_team', 'points_down', 'quarter_str', 'lead'))
]







"""
Game commentary strings from NBANLP Commentary Generator
"""
"""
Start of game commentary
"""
game_start_lineup_comments = [
    ("The starting lineup for the %s %s is %s.", ('city', 'name', 'starters')),
    ("%s are starting tonight for the %s %s.", ('starters', 'city', 'name')),
    ("The %s %s are starting %s.", ('city', 'name', 'starters'))
]


assist_pair_avg_comments = [
    ("These two have been playing great together for %s games this season. They've linked up for an assist an average %0.1f times per game.", ['num_games', 'assist_avg']),
    ("These guys consistently make a good pair. %s games this season they've averaged %0.1f assists with each other per game.", ['num_games', 'assist_avg'])
]

"""
Shot commentary
"""

shot_first_comments = [
    ("That was %s with the first shot attempt of the game.", ['primary_player']),
    ("And there's the first shot attempt of the game.", []),
    ("That was the first shot of the game.", [])
]

shot_first_made_comments = [
    ("That %s shot marks the first basket of the game.", ['shot_type']),
    ("And there's the first basket of the game.", []),
    ("So the %s get the first points on the board.", ['name']),
    ("And the %s start the game up %s.", ['name', 'points_worth_str'])
]

make_comments = [
    ("%s's %s shot is good.", ['primary_player', 'shot_type']),
    ("%s makes the basket.", ['primary_player']),
    ("%s puts %s points on the board for the %s with a %s shot.", ['primary_player', 'points_worth_str', 'name', 'shot_type']),
    ("%s makes the %s shot for %s.", ['primary_player', 'shot_type', 'points_worth_str']),
    ("The %s-foot %s shot from %s is good.", ['shot_distance', 'shot_type', 'primary_player']),
    ("%s puts it in for %s.", ['primary_player', 'points_worth_str']),
    ("%s with the %s-foot %s pointer.", ['primary_player', 'shot_distance', 'points_worth_str']),
    ("%s gives the %s %s with that made %s shot.", ['primary_player', 'name', 'points_worth_str', 'shot_type'])
]

make_assist_comments = [
    ("After the assist from %s, %s's %s is good.", ['secondary_player', 'primary_player', 'shot_type']),
    ("%s makes the basket. %s with the assist.", ['primary_player', 'secondary_player']),
    ("%s passes it off to %s, who finishes it with a %s.", ['secondary_player', 'primary_player', 'shot_type']),
    ("%s puts %s points on the board for the %s with a %s. %s with the assist.", ['primary_player', 'points_worth_str', 'name', 'shot_type', 'secondary_player']),
    ("%s passes the ball to %s, who puts %s points on the board for the %s with a %s.", ['secondary_player', 'primary_player', 'points_worth_str', 'name', 'shot_type']),
    ("After the pass from %s, the %s-foot %s from %s is good.", ['secondary_player', 'shot_distance', 'shot_type', 'primary_player']),
    ("%s puts it up for %s. %s with the assist.", ['primary_player', 'points_worth_str', 'secondary_player'])
]

make_long_comments = [
    ("The long shot by %s is good!", ['primary_player']),
    ("%s with the %s-footer!", ['primary_player', 'shot_distance']),
    ("%s hits a long %s-footer.", ['primary_player', 'shot_distance']),
    ("The long %s-foot shot by %s is in!", ['shot_distance', 'primary_player']),
    ("%s hits the 3 from way outside!", ['primary_player']),
]

make_very_long_comments = [
    ("Are you kidding me?? %s's %s-footer hits for the very long 3-pointer.", ['primary_player', 'shot_distance']),
    ("%s makes the %s-foot shot! What!", ['primary_player', 'shot_distance']),
    ("%s drains the %s-footer!!! That was a very long distance shot.", ['primary_player', 'shot_distance'])
]

miss_comments = [
    ("%s misses the shot attempt.", ['primary_player']),
    ("%s misses a shot.", ['primary_player']),
    ("%s with the missed shot.", ['primary_player']),
    ("A missed attempt from %s.", ['primary_player']),
    ("A missed shot from %s.", ['primary_player'])
]

miss_nameless_comments = [
    ("The %s misses the shot attempt.", ['name']),
    ("The %s miss a shot.", ['name']),
    ("The %s with the missed shot.", ['name']),
    ("A missed attempt from the %s.", ['name']),
    ("A missed shot from the %s.", ['name'])
]

block_comments = [
    ("The shot is blocked.", []),
    ("%s swats it away!", ['secondary_player']),
    ("%s's shot is blocked by %s.", ['primary_player', 'secondary_player'])
]

assist_comments = [
    ("Shot is made. Nice assist from %s.", ['secondary_player']),
    ("%s hooks up with %s for the basket.", ['secondary_player', 'primary_player'])
]

fastbreak_12_comments = [
    ("%s with the quick fastbreak.", ['primary_player']),
    ("After the %s by %s, %s scores a fastbreak basket.", ['fastbreak_play', 'fastbreak_creator', 'primary_player'])
]
fastbreak_11_comments = [
    ("%s with the quick fastbreak.", ['primary_player']),
    ("Great play! %s with the %s and then finishes off the play with a %s.", ['primary_player', 'fastbreak_play', 'shot_type'])
]
fastbreak_123_comments = [
    ("%s with the quick fastbreak.", ['primary_player']),
    ("After the %s by %s, %s passes to %s who makes a %s for %s points.", ['fastbreak_play', 'fastbreak_creator', 'secondary_player', 'primary_player', 'shot_type', 'points_worth'])
]
fastbreak_121_comments = [
    ("%s with the quick fastbreak.", ['primary_player']),
    ("After the %s by %s, %s scores a fastbreak basket.", ['fastbreak_play', 'fastbreak_creator', 'primary_player'])
]
fastbreak_112_comments = [
    ("%s with the quick fastbreak.", ['primary_player']),
    ("After the %s by %s, %s scores a fastbreak basket.", ['fastbreak_play', 'fastbreak_creator', 'primary_player'])
]

shot_longest_comments = [
    ("Amazing! That %s-foot shot by %s was the longest shot made all season!", ['shot_distance', 'primary_player'])
]

shot_longest_player_comments = [
    ("Wow! At %s feet, that's %s's longest shot of this season.", ['shot_distance', 'primary_player'])
]


"""
Substitution commentary
"""
substitution_default_comments = [
    ("%s goes in for %s.", ['primary_player', 'secondary_player']),
    ("%s is coming out for %s.", ['secondary_player', 'primary_player']),
    ("%s for the %s is coming out for %s.", ['secondary_player', 'name', 'primary_player']),
    ("The %s sub in %s for %s.", ['name', 'primary_player', 'secondary_player'])
]

substitution_off_bench_comments = [
    ("%s comes off the bench for for %s.", ['primary_player', 'secondary_player']),
]

substitution_on_bench_comments = [
    ("%s returns to the bench. The starter, %s, comes back on the floor.", ['secondary_player', 'primary_player']),
]

substitution_bench_points_comments = [
    ("The %s bench has been doing great tonight, scoring %s of the team's %s points", ['name', 'bench_points', 'team_points']),
    ("The bench for the %s have been making a big impact this game. They've put in a total of %s points out of the team's %s.", ['name', 'bench_points', 'team_points']),
    ("Scoring %s of the team's %s, the %s bench are having a great showing tonight.", ['bench_points', 'team_points', 'name'])
]

"""
Steal commentary
"""
steal_default_comments = [
    ("%s with the steal.", ['primary_player']),
    ("%s steals the ball from %s.", ['primary_player', 'secondary_player']),
    ("%s with the pick.", ['primary_player'])
]


"""
Frethrow commentary
"""

free_throw_start_default_comments = [
    ("%s is %s of %s from the line tonight. He's shooting free throws now.", ['primary_player', 'free_throws_made', 'tot_free_throws']),
    ("%s is %s for %s in free throws tonight. He's shooting at the line now.", ['primary_player', 'free_throws_made', 'tot_free_throws'])
]

free_throw_default_comments = [
    ("%s", ['description'])
]

"""
Foul commentary
"""
foul_default_comments = [
    ("%s with the foul.", ['primary_player']),
    ("Foul called on %s.", ['primary_player']),
    ("There's a foul called on %s.", ['primary_player'])
]

foul_default_non_comments = [
    ("%s with the foul.", ['primary_player']),
    ("Foul called on %s.", ['primary_player']),
    ("There's a foul called on %s.", ['primary_player'])
]

foul_q1_comments = [
    ("He's got two fouls in the first quarter, probably should bench him soon.", []),
    ("Those two fouls in the first quarter could put him in early foul trouble.", []),
    ("He's got to watch his fouls now, with two fouls already in the first quarter.", [])
]

foul_q3_comments = [
    ("%s's fourth foul puts him in foul trouble with still over a quarter remaining.", ['primary_player'])
]

foul_q4_comments = [
    ("%s's has to watch out, one more slip up and he fouls out.", ['primary_player'])
]

foul_out_comments = [
    ("And he's gone. That's %s's last foul to give.", ['primary_player'])
]

"""
Rebound commentary
"""
rebound_default_comments = [
    ("%s with the rebound.", ['primary_player']),
    ("%s with the %s rebound.", ['primary_player', 'rebound_type']),
    ("%s rebounds the ball.", ['primary_player'])
]

"""
Jumpball commentary
"""
jumpball_default_comments = [
    ("A jumpball is called.", []),
    ("A jumpball is called in the %s's favor.", ['name'])
]

jumpball_first_comments = [
    ("And here's the tipoff to start the game. %s on the %s gains possesion.", ['primary_player', 'name'])
]

"""
Timeout commentary
"""
timeout_default_comments = [
    ("A timeout is called by the %s.", ['name']),
    ("The %s call a timeout.", ['name'])
]

timeout_team_losing_streak_comments = [
    ("It's been a sad last few games for the %s. They've lost %s of their last %s games.", ['team_name', 'num_lost', 'num_past_games'])
]

timeout_team_winning_streak_comments = [
    ("The %s have been on a great streak lately, winning %s of %s!", ['team_name', 'num_won', 'num_past_games']),
    ("The %s have been playing great these last few games. They've won %s of their last %s games.", ['team_name', 'num_won', 'num_past_games'])
]


"""
Start of game commentary
"""
game_start_first_default_comments = [
    ("The %s will be playing the %s here in %s.", ['away_team', 'home_team', 'home_city']),
    ("The matchup tonight is the %s %s playing at home against the %s %s.", ['home_city', 'home_team', 'away_city', 'away_team']),
    ("Tonights matchup we have the home team, the %s %s, playing the %s %s.", ['home_city', 'home_team', 'away_city', 'away_team']),
]

game_start_lineup_home_comments = [
    ("The starting lineup for the %s %s is %s.", ('home_city', 'home_team', 'home_starters')),
    ("%s are starting tonight for the %s %s.", ('home_starters', 'home_city', 'home_team')),
    ("The %s %s are starting %s.", ('home_city', 'home_team', 'home_starters')),
    ("The %s %s starting lineup for tonights game is %s.", ('home_city', 'home_team', 'home_starters')),
    ("The starters for the %s %s are %s.", ('home_city', 'home_team', 'home_starters'))
]

game_start_lineup_away_comments = [
    ("The starting lineup for the %s %s is %s.", ('away_city', 'away_team', 'away_starters')),
    ("%s are starting tonight for the %s %s.", ('away_starters', 'away_city', 'away_team')),
    ("The %s %s are starting %s.", ('away_city', 'away_team', 'away_starters')),
    ("The %s %s starting lineup for tonights game is %s.", ('away_city', 'away_team', 'away_starters')),
    ("The starters for the %s %s are %s.", ('away_city', 'away_team', 'away_starters'))
]
    
game_start_record_comments = [
    ("The %s are currently with a %s-%s record, while the %s stand with a %s-%s record", ('home_team', 'home_wins', 'home_losses', 'away_team', 'away_wins', 'away_losses')),
]


"""
End of game commentary
"""

game_end_first_default_comments = [
    ("Game over. The %s end the game with a %s to %s victory over the %s. That ends the night here in %s.", ['winner_team_name', 'winner_score', 'loser_score', 'loser_team_name', 'home_city'])
]
