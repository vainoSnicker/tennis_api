from datetime import date
import pandas as pd
from tqdm import tqdm

from tennis.models import Player
from tennis.models import Match
from tennis.models import Tourney

from .mappings import MATCH_FIELDS
from .utils import calculate_elos


class CSVImporter:
    players = {}
    tourneys = {}
    csv_path = 'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/'
    match_prefix = 'atp_matches'
    rank_csv = 'atp_rankings_current.csv'
    player_csv = 'atp_players.csv'
    this_year = date.today().year

    def data_from_csv(self, start_year, init=True):
        for year in range(start_year, self.this_year + 1):
            print('Importing data from year {}:'.format(year))
            df = pd.read_csv('{}{}_{}.csv'.format(self.csv_path, self.match_prefix, year), encoding="ISO-8859-1")
            df = self.clean_csv(df)
            for index, row in tqdm(df.iterrows(), total=df.shape[0]):
                if not init:
                    if Match.objects.filter(tourney__tourney_id=row.tourney_id, match_num=row.match_num).exists():
                        continue
                if row.surface.lower() not in ['clay', 'grass', 'hard']:
                    row.surface = 'hard'
                row.surface = row.surface.lower()
                tourney = self.get_or_create_tourney(row)
                winner = self.get_or_create_player(row, 'winner_')
                loser = self.get_or_create_player(row, 'loser_')
                self.create_match(row, winner, loser, tourney)
                self.update_elos(winner, loser, row.surface)
        self.update_rankings()
        self.save_players()
        
    def clean_csv(self, df):
        df = df[df.tourney_name.str.contains('Davis Cup') == False]
        df = df[df.tourney_name.str.contains('Atp Cup') == False]
        try:
            df['tourney_date'] = pd.to_datetime(df['tourney_date'], format='%Y%m%d')
        except:
            df['tourney_date'] = pd.to_datetime(df['tourney_date'], format='%Y.%m.%d')
        df['winner_id'] = df['winner_id'].astype(int)
        df['loser_id'] = df['loser_id'].astype(int)
        df = df.sort_values(['tourney_date', 'match_num'])
        return df.fillna('')

    def get_or_create_tourney(self, row):
        if row.tourney_id not in self.tourneys:
            tourney, created = Tourney.objects.get_or_create(
                tourney_id=row.tourney_id,
                defaults={
                    'name': row.tourney_name,
                    'start_date': row.tourney_date,
                    'surface': row.surface,
                    'draw_size': row.draw_size,
                    'tourney_level': row.tourney_level
                }
                
            )
            self.tourneys[row.tourney_id] = tourney
        return self.tourneys[row.tourney_id]

    def get_or_create_player(self, data, prefix=''):
        player_id = data['{}id'.format(prefix)]
        if player_id not in self.players:
            player, created = Player.objects.get_or_create(
                atp_id=player_id,
                defaults={
                    'country': data['{}ioc'.format(prefix)],
                    'name': data['{}name'.format(prefix)],
                    'hand': data['{}hand'.format(prefix)],
                    'elo': 1500,
                    'elo_grass': 1500,
                    'elo_clay': 1500,
                    'elo_hard': 1500
                }
            )
            self.players[player_id] = player
        return self.players[player_id]

    def create_match(self, row, winner, loser, tourney):
        match_data = {k: v for k, v in dict(**row).items() if k in MATCH_FIELDS and v != ''}
        match_data['w_player'] = winner
        match_data['l_player'] = loser
        match_data['tourney'] = tourney
        match_data['w_elo'] = winner.elo
        match_data['l_elo'] = loser.elo
        match_data['w_elo_ts'] = getattr(winner, 'elo_{}'.format(row.surface))
        match_data['l_elo_ts'] = getattr(loser, 'elo_{}'.format(row.surface))
        Match.objects.create(**match_data)
    
    def update_rankings(self, save=False):
        print('Updating ranks:')
        self.clean_ranks()
        player_df = pd.read_csv('{}{}'.format(self.csv_path, self.player_csv), names=['id', 'first_name', 'last_name', 'hand', 'birth', 'ioc'])
        rank_df = pd.read_csv('{}{}'.format(self.csv_path, self.rank_csv), names=['date', 'rank', 'id', 'rank_points'])
        df = pd.merge(rank_df, player_df, on='id')
        df = df.query('date == {}'.format(df.iloc[0].date))
        df['name'] = df[['first_name', 'last_name']].apply(lambda x: ' '.join(x), axis=1)
        df = df.fillna('')
        for index, row in tqdm(df.iterrows(), total=df.shape[0]):
            player = self.get_or_create_player(row)
            player.ranking = row['rank']
            player.ranking_points = row['rank_points']
            if save:
                player.save()
    
    def save_players(self):
        print('Saving players.:')
        for k, v in tqdm(self.players.items()):
            v.save()

    def clean_ranks(self):
        players = Player.objects.filter(ranking__isnull=False)
        players.update(ranking=None, ranking_points=None)
    
    def update_elos(self, winner, loser, surface):
        elo_ts_name = 'elo_{}'.format(surface)
        w_new_tot, l_new_tot = calculate_elos(winner.elo, loser.elo)
        w_new_ts, l_new_ts = calculate_elos(getattr(winner, elo_ts_name), getattr(loser, elo_ts_name))
        winner.elo = w_new_tot
        loser.elo = l_new_tot
        setattr(winner, elo_ts_name, w_new_ts)
        setattr(loser, elo_ts_name, l_new_ts)
