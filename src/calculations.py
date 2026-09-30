import math
from enum import StrEnum
from dataclasses import dataclass


class Character(StrEnum):
    Fox = "Fox"
    Falco = "Falco"
    Marth = "Marth"
    Bowser = "Bowser"
    DonkeyKong = "Donkey Kong"
    Samus = "Samus"
    Ganondorf = "Ganondorf"
    Yoshi = "Yoshi"
    CaptainFalcon = "Captain Falcon"
    Link = "Link"
    DrMario = "Dr. Mario"
    Luigi = "Luigi"
    Mario = "Mario"
    Ness = "Ness"
    Peach = "Peach"
    Sheik = "Sheik"
    Zelda = "Zelda"
    IceClimbers = "Ice Climbers"
    Mewtwo = "Mewtwo"
    Roy = "Roy"
    YoungLink = "Young Link"
    Pikachu = "Pikachu"
    Kirby = "Kirby"
    Jigglypuff = "Jigglypuff"
    MrGameAndWatch = "Mr. Game & Watch"
    Pichu = "Pichu"


# at low-kb sakurai angle moves cannot be asdi-down'ed.
# this means low-kb moves *beat crouch*; crouching may also make a mid-kb
# move weak enough to break crouch.
# so, for a Sakurai angle move, as percent increases:
# breaks crouch unconditionally --> asdi down works, crouch DOESNT --> crouch works normally -->

# for a normal move, as percent increases:
# crouch and


@dataclass
class Move:
    percent: int
    scaling: float
    base_knockback: float
    sakurai: bool = False
    downwards: bool = False


def kb(
    move_dmg_percent,
    victim_pre_percent,
    victim_weight,
    move_scaling,
    move_bkb,
    crouch,
):
    "TODO: staling is not properly incorporated."

    p = math.floor(move_dmg_percent + victim_pre_percent)
    d = move_dmg_percent
    w = victim_weight
    s = move_scaling
    b = move_bkb
    r = 1 / 3 if crouch else 1.0
    inner = (p * d / 20) + (p / 10)
    return r * (b + (s * (18.0 + inner * 280 / (w + 100))))
