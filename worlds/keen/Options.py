from dataclasses import dataclass
from Options import PerGameCommonOptions, Choice, DeathLink, Range, Toggle

class EpisodeSelect(Choice):
    """
    Which episodes should be included in the seed.
    ck4 = Episode 4
    ck5 = Episode 5
    both = Episode 4 & Episode 5
    """
    display_name = "Episode Select"

    option_ck4 = 1
    option_ck5 = 2
    option_both = 0

    default = option_both

class EnableGemsets(Toggle):
    """
    Whether gemsets should be enabled in the seed.
    With this option on, you will receive all level gem items for a specific level at the same time.
    With this option off, you will receive each level gem individually.
    """
    display_name = "Enable Gemsets"

    default = 1

class AdditionalStartingLevels(Range):
    """
    How many additional levels should be randomly unlocked at the start of the game.
    By default, Border Village and Slug Village in Keen 4 and Ion Ventilation System and
    Security Center in Keen 5 are always unlocked. Additionally, the gems and keycards
    needed to complete these levels are also unlocked from the start.
    """
    display_name = "Additional Starting Levels"

    range_start = 3
    range_end = 10
    
    default = 3

# Leaving out for now - will return if/when pointsanity is implemented

#class EnablePointsanity(Toggle):
#    """
#    Whether to enable pointsanity.
#    Adds a number of checks to each level at various point threshholds.
#    *NOT YET IMPLEMENTED*
#    """
#   display_name = "Enable Pointsanity"
#
#    default = 0

class RandomizePogo(Choice):
    """
    Whether the pogo stick should be randomized.
    startwith = Start the game with the ability to use the pogo stick. This is vanilla behavior.
    early = The pogo stick will be placed early in the seed.
    randomize = The pogo stick can appear anywhere in the seed.
    """
    display_name = "Randomize Pogo"

    option_startwith = 0
    option_early = 1
    option_randomize = 2

    default = option_early

class RandomizeStunner(Choice):
    """
    Whether the neural stunner should be randomized.
    startwith = Start the game with the ability to use the stunner. This is vanilla behavior.
    early = The stunner will be placed early in the seed.
    randomize = The stunner can appear anywhere in the seed.
    """
    display_name = "Randomize Stunner"

    option_startwith = 0
    option_early = 1
    option_randomize = 2

    default = option_startwith

class RandomizeWetsuit(Choice):
    """
    Whether the wetsuit should be randomized.
    startwith = Start the game with the ability to use the wetsuit.
    early = The wetsuit will be placed early in the seed.
    randomize = The wetsuit can appear anywhere in the seed.
    """
    display_name = "Randomize Wetsuit"

    option_startwith = 0
    option_early = 1
    option_randomize = 2

    default = option_randomize

@dataclass
class KeenOptions(PerGameCommonOptions):
    episode_select: EpisodeSelect
    enable_gemsets: EnableGemsets
    additional_starting_levels: AdditionalStartingLevels
    # enable_pointsanity: EnablePointsanity
    randomize_pogo: RandomizePogo
    randomize_stunner: RandomizeStunner
    randomize_wetsuit: RandomizeWetsuit
    death_link: DeathLink