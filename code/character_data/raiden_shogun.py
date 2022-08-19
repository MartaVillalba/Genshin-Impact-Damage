import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class RaidenShogun:
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
        self.base_electro_dmg = data["Electro DMG"]
        self.total_electro_dmg = data["Electro DMG"]
        self.attack_level = data["Normal Attack level"]
        self.skill_level = data["Skill level"]
        self.burst_level = data["Burst level"]
        self.weapon = data["Weapon"]
        self.weapon_ref = data["Weapon refinement"]
        self.artifacts = data["Artifacts"]
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
        self.abilities = {
            "Normal Attack": {},
            "Skill": {
                "Skill DMG": [
                    117.2,
                    126,
                    134.8,
                    146.5,
                    155.3,
                    164.1,
                    175.8,
                    187.5,
                    199.2,
                    211,
                    222.7,
                    234.4,
                    249.1,
                ],
                "Coordinated ATK DMG": [
                    42,
                    45.2,
                    48.3,
                    52.5,
                    55.7,
                    58.8,
                    63,
                    67.2,
                    71.4,
                    75.6,
                    79.8,
                    84,
                    89.3,
                ],
                "Elemental Burst DMG Bonus": [
                    0.22,
                    0.23,
                    0.24,
                    0.25,
                    0.26,
                    0.27,
                    0.28,
                    0.29,
                    0.3,
                    0.3,
                    0.3,
                    0.3,
                    0.3,
                ],
            },
            "Burst": {
                "Energy Cost": 90,
                "Base DMG": [
                    401,
                    431,
                    461,
                    501,
                    531,
                    561,
                    601,
                    641,
                    681,
                    721,
                    762,
                    802,
                    852,
                    902,
                ],
            },
        }
        self.calculate_burst_damage()

    def calculate_burst_base_dmg(self):
        percentage = self.abilities["Burst"]["Base DMG"][self.burst_level - 1]
        self.base_dmg = percentage / 100 * self.atk

    def calculate_electro_dmg(self):
        if self.level > 20:
            self.total_electro_dmg += 0.4 * (self.energy_recharge - 100)
        self.percentage_bonus += self.total_electro_dmg

    def calculate_weapon_bonus(self):
        if self.weapon == "The Catch":
            dmg_bonus = [16, 20, 24, 28, 32]
            crit_rate_bonus = [6, 7.5, 9, 10.5, 12]
            # Assume burst bonus as global bonus because only burst dmg is going to be calculated
            self.percentage_bonus += dmg_bonus[self.weapon_ref - 1]
            self.total_crit_rate += crit_rate_bonus[self.weapon_ref - 1]

    def calculate_artifacts_bonus(self):
        if {"Emblem of Severed Fate": "4P"} in self.artifacts:
            self.percentage_bonus += min(0.25 * self.energy_recharge, 75)

    def calculate_skill_bonus(self):
        bonus = self.abilities["Skill"]["Elemental Burst DMG Bonus"][
            self.skill_level - 1
        ]
        self.percentage_bonus += bonus * self.abilities["Burst"]["Energy Cost"]

    def calculate_out_dmg(self):
        self.out_dmg = (
            self.base_dmg * self.special_multiplier + self.flat_bonus
        ) * (1 + self.percentage_bonus / 100)

    def calculate_crit_dmg(self):
        self.crit_out_dmg = self.out_dmg * (1 + self.crit_dmg / 100)

    def calculate_def_multiplier(self, enemy_level=85):
        if self.constellation == "C2":
            k = 0.4
        else:
            k = 1
        self.def_multiplier = (self.level + 100) / (
            k * (enemy_level + 100) + self.level + 100
        )

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

    def calculate_burst_damage(self):
        self.reset_stats()
        self.calculate_burst_base_dmg()
        self.calculate_electro_dmg()
        self.calculate_weapon_bonus()
        self.calculate_artifacts_bonus()
        self.calculate_skill_bonus()
        self.calculate_out_dmg()
        self.calculate_crit_dmg()
        self.calculate_def_multiplier()
        self.calculate_real_dmg()
        self.calculate_mean_dmg()

    def reset_stats(self):
        self.percentage_bonus = 0
        self.total_crit_rate = self.base_crit_rate
        self.total_electro_dmg = self.base_electro_dmg

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

    def calculate_dmg_vs_er(self, er_values, atk_values):
        results = np.zeros(shape=(len(atk_values), len(er_values)))
        for i, atk in enumerate(atk_values):
            dmg_er_values = []
            self.atk = atk
            for er in er_values:
                self.energy_recharge = er
                self.calculate_burst_damage()
                dmg_er_values.append(self.mean_dmg)
            results[i, :] = dmg_er_values
        return results

    def calculate_dmg_vs_atk(self, atk_values, er_values):
        results = np.zeros(shape=(len(er_values), len(atk_values)))
        for i, er in enumerate(er_values):
            dmg_atk_values = []
            self.energy_recharge = er
            for atk in atk_values:
                self.atk = atk
                self.calculate_burst_damage()
                dmg_atk_values.append(self.mean_dmg)
            results[i, :] = dmg_atk_values
        return results

    def plot_dmg(self):
        er_min, er_max = 150, 300
        er_values = np.linspace(er_min, er_max, 1000)
        er_atk_values = np.array([2400, 2000, 1600])
        dmg_er_values = self.calculate_dmg_vs_er(er_values, er_atk_values)

        atk_min, atk_max = 1500, 2500
        atk_values = np.linspace(atk_min, atk_max, 1000)
        atk_er_values = np.array([300, 250, 200, 150])
        dmg_atk_values = self.calculate_dmg_vs_atk(atk_values, atk_er_values)

        fig=make_subplots(specs=[[{"secondary_y": True}]])
        line_style = ['solid', 'dash', 'dashdot', 'dot']
        for i, er in enumerate(atk_er_values):
            fig.add_trace(
                go.Scatter(
                    x=dmg_atk_values[i, :],
                    y=atk_values,
                    name="ATK curve (ER=" + str(er) + ")",
                    line=dict(color="firebrick", width=2, dash=line_style[i])
                ),
                secondary_y=False
            )
        for i, atk in enumerate(er_atk_values):
            fig.add_trace(
                go.Scatter(
                    x=dmg_er_values[i, :],
                    y=er_values,
                    name="ER curve (ATK=" + str(atk) + ")",
                    line=dict(color="royalblue", width=2, dash=line_style[i])
                ),
                secondary_y=True
            )

        fig.update_xaxes(title_text="Mean DMG")
        fig.update_yaxes(title_text="ATK", secondary_y=False)
        fig.update_yaxes(title_text="ER", secondary_y=True)
        fig.update_layout(
            autosize=True,
            margin=dict(l=50, r=50, b=50, t=50)
        )
        fig.show()

    def plot_3d_dmg(self):
        n_points = 50
        er_min, er_max = 150, 300
        er_values = np.arange(er_min, er_max, (er_max - er_min) / n_points)
        atk_min, atk_max = 1500, 2500
        atk_values = np.arange(
            atk_min, atk_max, (atk_max - atk_min) / n_points
        )
        dmg_values = np.zeros(shape=(n_points, n_points))
        for i, er in enumerate(er_values):
            for j, atk in enumerate(atk_values):
                self.energy_recharge = er
                self.atk = atk
                self.calculate_burst_damage()
                dmg_values[i, j] = self.mean_dmg

        fig = go.Figure(
            data=[go.Surface(z=dmg_values, x=er_values, y=atk_values)]
        )
        camera = dict(eye=dict(x=-1.8, y=-1.3, z=0.6))
        fig.update_layout(
            scene=dict(
                xaxis_title="ER", yaxis_title="ATK", zaxis_title="Mean DMG"
            ),
            autosize=True,
            width=700,
            height=500,
            margin=dict(l=50, r=50, b=5, t=5),
            scene_camera=camera,
        )
        fig.show()
