from BaseClasses import Region, Location, ItemClassification, Item
from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule
import logging
from dataclasses import dataclass

from .Items import (
    KeenItem, item_name_to_id, create_item as keen_create_item,
    ck_common_items, ck4_level_items, ck4_unique_items,
    ck4_gem_items, ck4_gemset_items, ck5_level_items, ck5_keycard_items,
    ck5_gem_items, ck5_gemset_items
)
from .Locations import location_table
from .Options import KeenOptions
from .Regions import create_ck4_regions, create_ck5_regions
from .Rules import create_ck_rules

class KeenWorld(World):
    game = "Commander Keen"
    options_dataclass = KeenOptions

    location_name_to_id = location_table
    item_name_to_id = item_name_to_id

    origin_region_name = "Menu"

    def create_item(self, name: str) -> KeenItem:
        return keen_create_item(name, self.player)

    # --------------------------------------------------
    # Create regions + locations
    # --------------------------------------------------

    def create_regions(self):
        ep = self.options.episode_select.value

        menu = Region("Menu", self.player, self.multiworld)

        self.multiworld.regions += [menu]

        if ep == 1:
            create_ck4_regions(self)
        elif ep == 2:
            create_ck5_regions(self)
        else:
            create_ck4_regions(self)
            create_ck5_regions(self)

        if ep in [0, 1]:
            bwbm = self.multiworld.get_location("Bean-With-Bacon Megarocket Complete", self.player)
            bwbm_event = Location(self.player, "Keen 4 Victory", None, bwbm.parent_region)
            bwbm_event.place_locked_item(
                Item("Keen 4 Complete", ItemClassification.progression, None, self.player))
            bwbm.parent_region.locations.append(bwbm_event)
            set_rule(bwbm_event, lambda state:
                     state.can_reach("Bean-With-Bacon Megarocket Complete", "Location", self.player))
        
        if ep in [0, 2]:
            qed = self.multiworld.get_location("Quantum Explosion Dynamo Complete", self.player)
            qed_event = Location(self.player, "Keen 5 Victory", None, qed.parent_region)
            qed_event.place_locked_item(
                Item("Keen 5 Complete", ItemClassification.progression, None, self.player))
            qed.parent_region.locations.append(qed_event)
            set_rule(qed_event, lambda state:
                     state.can_reach("Quantum Explosion Dynamo Complete", "Location", self.player))

    # --------------------------------------------------
    # Determine starting inventory
    # --------------------------------------------------

    def generate_early(self):
        ep = self.options.episode_select.value                
        count = self.options.additional_starting_levels.value
        
        level_selection = []
        self.starting_items = []

        # Starting Level
        ck4_levels = [
            "The Perilous Pit",
            "Cave of the Descendents",
            "Chasm of Chills",
            "Crystalus",
            "Hilville",
            "Sand Yego",
            "Miragia",
            "Lifewater Oasis",
            "Pyramid of the Moons",
            "Pyramid of Shadows",
            "Pyramid of the Gnosticine Ancients",
        ]

        ck5_levels = [
            "Defense Tunnel Vlook",
            "Defense Tunnel Burrh", 
            "Defense Tunnel Sorra",
            "Defense Tunnel Teln",
            "Energy Flow Systems",
            "Regulation Control Center",
            "Neutrino Burst Injector",
            "Brownian Motion Inducer",
        ]

        if ep in [0, 1]:
            level_selection += ck4_levels
            self.starting_items += ["Border Village", "Slug Village"]
        if ep in [0, 2]:
            level_selection += ck5_levels
            self.starting_items += ["Ion Ventilation System", "Security Center"]
            if self.options.enable_gemsets:
                self.starting_items += ["Security Center Gemset", "Security Center - Keycard"]
            else:
                self.starting_items += ["Security Center - Red Gem",
                                        "Security Center - Blue Gem",
                                        "Security Center - Keycard"]

        self.starting_items += self.multiworld.random.sample(level_selection, min(count, len(level_selection)))

        # Starting abilities
        if self.options.randomize_pogo.value == 0:
            self.starting_items.append("Pogo Stick")
        elif self.options.randomize_pogo.value == 1:
            self.multiworld.early_items[self.player]["Pogo Stick"] = 1

        if self.options.randomize_stunner.value == 0:
            self.starting_items.append("Neural Stunner")
        elif self.options.randomize_stunner.value == 1:
            self.multiworld.early_items[self.player]["Neural Stunner"] = 1

        if ep in [0, 1]:
            if self.options.randomize_wetsuit.value == 0:
                self.starting_items.append("Wetsuit")
            elif self.options.randomize_wetsuit.value == 1:
                self.multiworld.early_items[self.player]["Wetsuit"] = 1

        # Push all starting items
        for item in self.starting_items:
            self.multiworld.push_precollected(
                keen_create_item(item, self.player)
            )

    # --------------------------------------------------
    # Create item pool
    # --------------------------------------------------

    def create_items(self):
        ep = self.options.episode_select.value
        gemsets = self.options.enable_gemsets.value

        pool = []

        pool += ck_common_items

        if ep in [0, 1]:
            pool += ck4_level_items
            pool += ck4_unique_items
            pool += ck4_gemset_items if gemsets else ck4_gem_items

        if ep in [0, 2]:
            pool += ck5_level_items
            pool += ck5_keycard_items
            pool += ck5_gemset_items if gemsets else ck5_gem_items

        pool = [i for i in pool if i.name not in self.starting_items]

        for item_def in pool:
            self.multiworld.itempool.append(
                keen_create_item(item_def.name, self.player)
            )

        # Calculate filler needed
        location_count = len(self.multiworld.get_unfilled_locations(self.player))
        item_count = len([i for i in self.multiworld.itempool if i.player == self.player])
        filler_count = max(0, location_count - item_count)

        # Add weighted filler
        for _ in range(filler_count):
            roll = self.multiworld.random.random()
            if roll < 0.67:
                self.multiworld.itempool.append(self.create_item("Stunner Ammo"))
            else:
                self.multiworld.itempool.append(self.create_item("Extra Keen"))

    # --------------------------------------------------
    # Set access rules
    # --------------------------------------------------

    def set_rules(self):
        create_ck_rules(self)

    def fill_slot_data(self) -> dict:
        return {
            "episode_select": self.options.episode_select.value,
            "enable_gemsets": self.options.enable_gemsets.value,
            "death_link": self.options.death_link.value,
        }