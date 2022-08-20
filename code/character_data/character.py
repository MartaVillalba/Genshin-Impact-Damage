import pandas as pd
import numpy as np

class Character:
    def __init__(self, data):
        self.name = data["Character"]
        self.description = data["Description"]
        self.constellation = data["Constellation"]
        self.level = data["Level"]
        self.atk = data["ATK"]
        self.base_crit_rate = data["CRIT rate"]
        self.total_crit_rate = data["CRIT rate"]
        self.crit_dmg = data["CRIT DMG"]
        self.energy_recharge = data["ER"]
        self.attack_level = data["Normal Attack level"]
        self.skill_level = data["Skill level"]
        self.burst_level = data["Burst level"]
        self.weapon = data["Weapon"]
        self.weapon_ref = data["Weapon refinement"]
        self.artifacts = data["Artifacts"]
        self.electro_dmg = data.get("Electro DMG", 0)
        self.anemo_dmg = data.get("Anemo DMG", 0)
        self.geo_dmg = data.get("Geo DMG", 0)
        self.pyro_dmg = data.get("Pyro DMG", 0)
        self.cryo_dmg = data.get("Cryo DMG", 0)
        self.hydro_dmg = data.get("Hydro DMG", 0)
        self.dendro_dmg = data.get("Dendro DMG", 0)
        self.base_dmg = 0
        self.special_multiplier = 1
        self.flat_bonus = 0
        self.percentage_bonus = 0
        self.out_dmg = 0
        self.crit_out_dmg = 0
        self.real_dmg = 0
        self.crit_real_dmg = 0
        self.mean_dmg = 0
        self.def_multiplier = 0
        self.res_multiplier = 0.9

    def calculate_weapon_bonus(self):
        if self.weapon == "The Catch":
            dmg_bonus = [16, 20, 24, 28, 32]
            crit_rate_bonus = [6, 7.5, 9, 10.5, 12]
            # Assume burst bonus as global bonus because only burst dmg is going to be calculated
            self.percentage_bonus += dmg_bonus[self.weapon_ref - 1]
            self.total_crit_rate += crit_rate_bonus[self.weapon_ref - 1]
        elif self.weapon == "Luxurious Sea-Lord":
            dmg_bonus = [12, 15, 18, 21, 24]
            self.percentage_bonus += dmg_bonus[self.weapon_ref - 1]

    def calculate_artifacts_bonus(self):
        if self.artifacts.get("Emblem of Severed Fate") == "4P":
            self.percentage_bonus += min(0.25 * self.energy_recharge, 75)
        if self.artifacts.get("Noblesse Oblige"):
            self.percentage_bonus += 20
        if self.artifacts.get("Thundering Fury"):
            self.percentage_bonus += 15

    def calculate_out_dmg(self):
        self.out_dmg = (
            self.base_dmg * self.special_multiplier + self.flat_bonus
        ) * (1 + self.percentage_bonus / 100)

    def calculate_crit_dmg(self):
        self.crit_out_dmg = self.out_dmg * (1 + self.crit_dmg / 100)

    def calculate_real_dmg(self):
        self.crit_real_dmg = (
            self.crit_out_dmg * self.def_multiplier * self.res_multiplier
        )
        self.real_dmg = (
            self.out_dmg * self.def_multiplier * self.res_multiplier
        )

    def calculate_mean_dmg(self):
        self.mean_dmg = (
            self.total_crit_rate * self.crit_real_dmg
            + (100 - self.total_crit_rate) * self.real_dmg
        ) / 100

    def reset_stats(self):
        self.percentage_bonus = 0
        self.total_crit_rate = self.base_crit_rate

    def print_results(self):
        results_df = pd.DataFrame(
            {
                "Character": [self.name],
                "Description": [self.description],
                "DMG (non crit)": [int(self.real_dmg)],
                "DMG (crit)": [int(self.crit_real_dmg)],
                "Mean DMG": [int(self.mean_dmg)],
            }
        )
        results_df.index = np.arange(1, len(results_df) + 1)
        return results_df

    def compare_builds(self, other):
        first_build = self.print_results()
        second_build = other.print_results()
        results_df = pd.concat([first_build, second_build])
        results_df.index = np.arange(1, len(results_df) + 1)
        return results_df


other_beidou_data = {
    'Character': 'Beidou',
    'Description': 'Thundering Fury x2',
    'Constellation': 'C6',
    'Level': 80,
    'ATK': 1757,
    'CRIT rate': 24.5,
    'CRIT DMG': 116.8,
    'ER': 154.7,
    'Electro DMG': 70.6,
    'Normal Attack level': 1, 
    'Skill level': 10,
    'Burst level': 10,
    'Weapon': 'Luxurious Sea-Lord',
    'Weapon refinement': 5,
    'Artifacts': {
        'Thundering Fury': '2P',
        'Echoes of an Offering': '2P'
    }
}
beidou = Character(other_beidou_data)
beidou.calculate_artifacts_bonus()