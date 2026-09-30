from .calculations import Character, Move

weights = {
    Character.Fox: 75,
    Character.Falco: 80,
    Character.Marth: 87,
    Character.Bowser: 117,
    Character.DonkeyKong: 114,
    Character.Samus: 110,
    Character.Ganondorf: 109,
    Character.Yoshi: 108,
    Character.CaptainFalcon: 104,
    Character.Link: 104,
    Character.DrMario: 100,
    Character.Luigi: 100,
    Character.Mario: 100,
    Character.Ness: 94,
    Character.Peach: 90,
    Character.Sheik: 90,
    Character.Zelda: 90,
    Character.IceClimbers: 88,
    Character.Marth: 87,
    Character.Mewtwo: 85,
    Character.Roy: 85,
    Character.YoungLink: 85,
    Character.Pikachu: 80,
    Character.Kirby: 70,
    Character.Jigglypuff: 60,
    Character.MrGameAndWatch: 60,
    Character.Pichu: 55,
}

pal_weights = weights.copy()
pal_weights[Character.Kirby] = 74
pal_weights[Character.Fox] = 73
pal_weights[Character.Marth] = 85
pal_weights[Character.Mario] = 98
pal_weights[Character.Yoshi] = 111
pal_weights[Character.Bowser] = 118


moves = {}
moves[Character.Fox] = {
    "nair_early": [
        Move(12, 1.0, 1.0),
    ],
    "nair_late": [
        Move(9, 1.0, 1.0),
    ],
    "dair": [
        Move(3, 1.0, 1.0, downwards=True),
    ],
}
