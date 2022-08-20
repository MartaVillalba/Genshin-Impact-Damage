from character_data.character import Character

class Beidou(Character):
    def __init__(self, data):
        Character.__init__(self, data)
        self.abilities = {
            "Normal Attack": {},
            "Skill": {
                "Base DMG": [
                    122,
                    131,
                    140,
                    152,
                    161,
                    170,
                    182,
                    195,
                    207,
                    219,
                    231,
                    243,
                    258
                ],
                "DMG Bonus on Hit Taken": [
                    160,
                    172,
                    184,
                    200,
                    212,
                    224,
                    240,
                    256,
                    272,
                    288,
                    304,
                    320,
                    340
                ]
            },
            "Burst": {
                "Energy Cost": 80,
                "Skill DMG": [
                    122,
                    131,
                    140,
                    152,
                    161,
                    170,
                    182,
                    195,
                    207,
                    219,
                    231,
                    243,
                    258,
                    274
                ],
                "Lightning DMG": [
                    96,
                    103,
                    110,
                    120,
                    127,
                    134,
                    144,
                    154,
                    163,
                    173,
                    182,
                    192,
                    204,
                    216
                ]
            }
        }
        self.calculate_burst_damage()

    def calculate_burst_base_dmg(self):
        percentage = self.abilities["Burst"]["Skill DMG"][self.burst_level - 1]
        self.base_dmg = percentage / 100 * self.atk

    def calculate_def_multiplier(self, enemy_level=85):
        self.def_multiplier = (self.level + 100) / (
            (enemy_level + 100) + self.level + 100
        )

    def calculate_electro_dmg(self):
        self.percentage_bonus += self.electro_dmg

    def calculate_burst_damage(self):
        self.reset_stats()
        self.calculate_burst_base_dmg()
        self.calculate_electro_dmg()
        self.calculate_weapon_bonus()
        self.calculate_artifacts_bonus()
        self.calculate_out_dmg()
        self.calculate_crit_dmg()
        self.calculate_def_multiplier()
        self.calculate_real_dmg()
        self.calculate_mean_dmg()