def calculate_elos(winner_elo, loser_elo):
    elo_ev = calculate_elo_ev(winner_elo, loser_elo)
    winner_elo = winner_elo + 32*(1 - elo_ev)
    loser_elo = loser_elo - 32*(1 - elo_ev)
    return int(winner_elo), int(loser_elo)


def calculate_elo_ev(p1_elo, p2_elo):
    r_1 = 10**(p1_elo/400)
    r_2 = 10**(p2_elo/400)
    return r_1/(r_1 + r_2)
