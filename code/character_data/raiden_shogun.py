import pandas as pd

class RaidenShogun():

    def __init__(self, data):
        self.name = 'Raiden Shogun'
        self.constellation = data['Constellation']
        self.level = data['Level']
        self.atk = data['ATK']
        self.crit_rate = data['CRIT rate']
        self.crit_dmg = data['CRIT DMG']
        self.energy_recharge = data['ER']
        self.electro_dmg = data['Electro DMG']
        self.attack_level = data['Normal Attack level']
        self.skill_level = data['Skill level']
        self.burst_level = data['Burst level']
        self.weapon = data['Weapon']
        self.weapon_ref = data['Weapon refinement']
        self.artifacts = data['Artifacts']
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
            'Normal Attack': {},
            'Skill': {
                'Skill DMG': [117.2, 126, 134.8, 146.5, 155.3, 164.1, 
                              175.8, 187.5, 199.2, 211, 222.7, 234.4, 249.1],
                'Coordinated ATK DMG': [42, 45.2, 48.3, 52.5, 55.7, 58.8, 
                                        63, 67.2, 71.4, 75.6, 79.8, 84, 89.3],
                'Elemental Burst DMG Bonus': [0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 
                                              0.28, 0.29, 0.3, 0.3, 0.3, 0.3, 0.3]
            },
            'Burst': {
                'Energy Cost': 90,
                'Base DMG': [401, 431, 461, 501, 531, 561, 601, 641, 681, 721, 762, 802, 852, 902]
            }
        }
        self.calculate_burst_damage()

    def calculate_burst_base_dmg(self):
        percentage = self.abilities['Burst']['Base DMG'][self.burst_level-1]
        self.base_dmg = percentage/100*self.atk

    def calculate_electro_dmg(self):
        if self.level > 20:
            self.electro_dmg += 0.4*(self.energy_recharge-100)
        self.percentage_bonus += self.electro_dmg

    def calculate_weapon_bonus(self):
        if self.weapon == 'The Catch':
            dmg_bonus = [16, 20, 24, 28, 32]
            crit_rate_bonus = [6, 7.5, 9, 10.5, 12]
            # Assume burst bonus as global bonus because only burst dmg is going to be calculated
            self.percentage_bonus += dmg_bonus[self.weapon_ref - 1]
            self.crit_rate += crit_rate_bonus[self.weapon_ref - 1]

    def calculate_artifacts_bonus(self):
        if {'Emblem of Severed Fate': '4P'} in self.artifacts:
            self.percentage_bonus += min(0.25 * self.energy_recharge, 75)

    def calculate_skill_bonus(self):
        bonus = self.abilities['Skill']['Elemental Burst DMG Bonus'][self.skill_level - 1]
        self.percentage_bonus += bonus * self.abilities['Burst']['Energy Cost']
        
    def calculate_out_dmg(self):
        self.out_dmg = (self.base_dmg * self.special_multiplier + self.flat_bonus) * (1 + self.percentage_bonus/100)

    def calculate_crit_dmg(self):
        self.crit_out_dmg = self.out_dmg*(1 + self.crit_dmg/100)

    def calculate_def_multiplier(self, enemy_level = 85):
        if self.constellation == 'C2':
            k = 0.4
        else:
            k = 1
        self.def_multiplier = (self.level + 100)/(k*(enemy_level + 100) + self.level + 100)

    def calculate_real_dmg(self):
        self.crit_real_dmg = self.crit_out_dmg * self.def_multiplier * self.res_multiplier
        self.real_dmg = self.out_dmg * self.def_multiplier * self.res_multiplier

    def calculate_mean_dmg(self):
        self.mean_dmg = (self.crit_rate * self.crit_real_dmg + (100 - self.crit_rate) * self.real_dmg)/100

    def calculate_burst_damage(self):
        self.percentage_bonus = 0
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

    def print_results(self):
        results_df = pd.DataFrame({'Character': [self.name],
                                   'DMG (non crit)': [int(self.real_dmg)], 
                                   'DMG (crit)': [int(self.crit_real_dmg)],
                                   'Mean DMG': [int(self.mean_dmg)]})
        return results_df


