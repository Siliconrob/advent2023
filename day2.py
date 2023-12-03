import itertools
from dataclasses import dataclass
from parse import parse
from aocd import get_data
from icecream import ic


@dataclass
class GameTurn:
    blue: int
    red: int
    green: int


@dataclass
class GameResult:
    id: int
    turns: list[GameTurn]

    def red_cubes(self):
        return ic(max(turn.red for turn in self.turns))

    def green_cubes(self):
        return ic(max(turn.green for turn in self.turns))

    def blue_cubes(self):
        return ic(max(turn.blue for turn in self.turns))

    def min_cubes_to_play_game(self) -> int:
        return ic(self.red_cubes() * self.green_cubes() * self.blue_cubes())

@dataclass
class GameBag:
    red: int
    green: int
    blue: int

    def is_game_valid(self, game: GameResult) -> bool:
        for game_turn in game.turns:
            if game_turn.red > self.red or game_turn.blue > self.blue or game_turn.green > self.green:
                return False
        return True


def get_game_result(game_result_text: str) -> GameResult:
    id, turns = parse('Game {:d}: {}', game_result_text)
    parsed_turns = [get_game_turn(turn_result) for turn_result in turns.split(";")]
    game = GameResult(id, parsed_turns)
    return ic(game)


def get_game_turn(game_line: str) -> list[GameTurn]:
    new_turn = GameTurn(0, 0, 0)
    for current_turn in game_line.split(","):
        count, color = parse('{:d} {}', current_turn)
        match color:
            case 'red':
                new_turn.red = count
            case 'blue':
                new_turn.blue = count
            case 'green':
                new_turn.green = count
    return new_turn


if __name__ == '__main__':
    data = get_data(day=2, year=2023).splitlines()
    # data = ['Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
    #         'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
    #         'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
    #         'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
    #         'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green']

    valid_games = []
    game_bounds = GameBag(12, 13, 14)
    part2 = 0
    for current_line in data:
        current_game_results = get_game_result(current_line)
        if game_bounds.is_game_valid(current_game_results):
            valid_games.append(ic(current_game_results))
        part2 += ic(current_game_results.min_cubes_to_play_game())

    part1 = sum(valid_game.id for valid_game in valid_games)
    ic(f'Part 1: {part1}')
    ic(f'Part 2: {part2}')
