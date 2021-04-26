# TennisAPI

## About TennisAPI

This is a simplified version of my tennis project. Include CSV-importer and basic JSON-API. Crawlers, predictions, and UI are for family use only.

## Installation

Start server:
```shell
cd tennis_api
docker-compose up
```

Init data:
```shell
bash init.sh [start_year]
```
Data is from https://github.com/JeffSackmann/tennis_atp and elo is calculated using constant K=32 (better way to calculate elo https://www.betfair.com.au/hub/tennis-elo-modelling/)

## Update data

Weekly updates:
```shell
bash update.sh
```

## API

**Player:**

```http
GET /api/player/:pk/
```

*Example response:*

```javascript
{
    "id": 5515,
    "atp_id": 104925,
    "country": "SRB",
    "name": "Novak Djokovic",
    "hand": "R",
    "ranking": 1,
    "ranking_points": 12030,
    "elo": 1969,
    "elo_grass": 1929,
    "elo_clay": 1932,
    "elo_hard": 1977
}
```

**Players matches:**

```http
GET /api/player/:pk/matches/
```

*Return players won and lost matches:*

```javascript
{
     "won_matches": [{}...],
     "lost_matches": [{}...]
}
```

**Player list:**

```http
GET /api/players/
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `search` | `string` | Partial name search |
| `offset` | `int` | Default 0 |
| `limit` | `int` | Default 20 |
| `order_by` | `string` | Default 'ranking' |


**Tourney:**

```http
GET /api/tourney/:pk/
```

*Example response:*

```javascript
{
    "id": 6,
    "tourney_id": "2018-580",
    "name": "Australian Open",
    "start_date": "2018-01-15",
    "surface": "hard",
    "draw_size": 128,
    "tourney_level": "G"
}
```

**Tourney matches:**

```http
GET /api/tourney/:pk/matches/
```

*Returns all matches in the tournament*


**Tourney list:**

```http
GET /api/tourneys/
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `search` | `string` | Partial name search |
| `offset` | `int` | Default 0 |
| `limit` | `int` | Default 20 |


**Match:**

```http
GET /api/match/:pk/
```

*Example response:*

```javascript
{
    "id": 7324,
    "w_name": "Stefanos Tsitsipas",
    "l_name": "Andrey Rublev",
    "tourney_name": "Monte Carlo Masters",
    "score": "6-3 6-3",
    "best_of": 3,
    "match_num": 300,
    "round": "F",
    "minutes": 71,
    "w_ace": 3,
    "w_df": 1,
    "w_svpt": 47,
    "w_1stIn": 28,
    "w_1stWon": 24,
    "w_2ndWon": 13,
    "w_SvGms": 9,
    "w_bpSaved": 0,
    "w_bpFaced": 0,
    "l_ace": 1,
    "l_df": 0,
    "l_svpt": 54,
    "l_1stIn": 30,
    "l_1stWon": 24,
    "l_2ndWon": 8,
    "l_SvGms": 9,
    "l_bpSaved": 0,
    "l_bpFaced": 3,
    "winner_rank": 5,
    "winner_rank_points": 7040,
    "loser_rank": 8,
    "loser_rank_points": 5400,
    "w_elo": 1808,
    "l_elo": 1861,
    "w_elo_ts": 1746,
    "l_elo_ts": 1700,
    "w_player": 69,
    "l_player": 11,
    "tourney": 185
}
```

**Match list:**

```http
GET /api/matches/
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `search` | `string` | Partial name search (players and tourney)|
| `offset` | `int` | Default 0 |
| `limit` | `int` | Default 20 |
