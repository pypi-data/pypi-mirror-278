####1
import ama_xiv_combat_sim
import copy
import matplotlib.pyplot as plt
import numpy as np
import os
import time

from ama_xiv_combat_sim.example_rotations.get_example_rotations import (
    get_example_rotations,
)
from ama_xiv_combat_sim.kill_time_estimator.kill_time_estimator import KillTimeEstimator
from ama_xiv_combat_sim.rotation_analysis.rotation_analysis_utils import (
    RotationAnalysisUtils,
)
from ama_xiv_combat_sim.simulator.skills import create_skill_library, SkillModifier
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.damage_simulator import DamageSimulator
from ama_xiv_combat_sim.simulator.rotation_import_utils.csv_utils import CSVUtils
from ama_xiv_combat_sim.simulator.timeline_builders.damage_builder import DamageBuilder
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import (
    RotationBuilder,
)

GAME_VERSION="7.0"
SKILL_LIBRARY = create_skill_library(GAME_VERSION)

ROTATION_LIBRARY = get_example_rotations(SKILL_LIBRARY)
for v in ROTATION_LIBRARY.values():
    v.get_skill_timing()

class DisplayUtils:
    PERCENTILES_TO_USE = [1, 5, 25, 50, 75, 95, 99]
    COLOURS_TO_USE = [
        "black",
        "dimgray",
        "g",
        "b",
        (0.36, 0.28, 0.55),
        (1, 0.5, 0),
        (1, 0.0, 0.5),
    ]

    @staticmethod
    def print_button_press_timings(rb):
        print("---Times (in s) when skills get used:---")
        for tmp in rb.get_button_press_timing():
            print("{:>8}: {:>22}".format(tmp[0] / 1000.0, tmp[1]))
        print("\n")

    @staticmethod
    def print_damage_applications(per_skill_damage):
        print("---Times (in s) when damage lands:---")
        for sk in per_skill_damage:
            print(
                "time: {:>8}, name: {:>22}, expected_damage: {:9.2f}, potency: {:4n}, skill modifier: {:>22}, damage variance: {:6.2f}".format(
                    sk.application_time / 1000.0,
                    sk.skill_name,
                    sk.expected_damage,
                    sk.potency,
                    ", ".join(sk.skill_modifier_condition),
                    sk.standard_deviation,
                )
            )

    @staticmethod
    def print_damage_details(
        per_skill_damage, damage_ranges, status_effect_names_only=True
    ):
        print("---Damage ranges and expectation:---")
        for i in range(0, len(damage_ranges)):
            sk = per_skill_damage[i]
            print(
                '{:5n}: {:<22}, Potency: {:4n}, Modifier: "{}". '.format(
                    sk.application_time / 1000.0,
                    damage_ranges[i][0],
                    sk.potency,
                    ", ".join(sk.skill_modifier_condition),
                )
            )
            buffs, debuffs = sk.status_effects[0], sk.status_effects[1]
            if status_effect_names_only:
                print("  Buffs: ||{}||".format(", ".join(buffs.status_effects)))
                print("  DeBuffs: ||{}||".format(", ".join(debuffs.status_effects)))
            else:
                print(
                    "  Buffs: ||{:>22}||  crit: {:3.2f}, dh: {:3.2f}, damage_mult: {:3.2f}, guaranteed crit/dh: {}/{}:".format(
                        ", ".join(buffs.status_effects),
                        buffs.crit_rate_add,
                        buffs.dh_rate_add,
                        buffs.damage_mult,
                        buffs.guaranteed_crit,
                        buffs.guaranteed_dh,
                    )
                )
                print(
                    "  Debuffs: ||{:>22}||  crit: {:3.2f}, dh: {:3.2f}, damage_mult: {:3.2f}, guaranteed crit/dh: {}/{}:".format(
                        ", ".join(debuffs.status_effects),
                        debuffs.crit_rate_add,
                        debuffs.dh_rate_add,
                        debuffs.damage_mult,
                        debuffs.guaranteed_crit,
                        debuffs.guaranteed_dh,
                    )
                )
            for tmp in damage_ranges[i][1:]:
                print(
                    "   {:>14} ({:5.1f}%). expected_damage: {:9.2f},   [low, high]: [{}, {}]".format(
                        tmp[0], 100 * tmp[3], (tmp[1] + tmp[2]) / 2, tmp[1], tmp[2]
                    )
                )

    @staticmethod
    def print_results(total_damage, title="Average Damage"):
        percs = np.percentile(total_damage, DisplayUtils.PERCENTILES_TO_USE)
        print("{}: {mean:.2f}".format(title, mean=np.mean(total_damage)))
        for i in range(0, len(DisplayUtils.PERCENTILES_TO_USE)):
            print(
                "Percentile {}: {percs:.2f}".format(
                    DisplayUtils.PERCENTILES_TO_USE[i], percs=percs[i]
                )
            )
        print()

    @staticmethod
    def display_results(
        total_damage, xlabel="DPS", title=None, display_cumulative=True
    ):
        percs = np.percentile(total_damage, DisplayUtils.PERCENTILES_TO_USE)

        try:
            count, bins_count = np.histogram(total_damage, bins=500)
        except ValueError:
            return

        plt.figure()
        pdf = count / sum(count)
        plt.plot(bins_count[1:], pdf)
        for i in range(len(percs)):
            plt.plot(
                [percs[i], percs[i]],
                [0, max(pdf)],
                color=DisplayUtils.COLOURS_TO_USE[i],
            )
        plt.ylabel("Probability")
        plt.xlabel(xlabel)
        if title is not None:
            plt.title(title)
        plt.show(block=False)

        if display_cumulative:
            plt.figure()
            plt.plot(bins_count[1:], np.cumsum(pdf))
            plt.ylabel("Cumulative Probability")
            plt.xlabel("{} <= Value".format(xlabel))
            if title is not None:
                plt.title(title)
            plt.show(block=False)

    @staticmethod
    def display_damage_over_time(damage, t, window_length, title_prefix="Damage done"):
        RESOLUTION = 10
        x = np.asarray(range(int(min(t)), int(max(t)), RESOLUTION))
        res = np.zeros((len(x), 1))
        t = np.asarray(t)
        damage = np.asarray(damage)

        for i in range(0, len(x)):
            time_to_use = x[i]
            idx = np.argwhere(
                (t >= time_to_use) & (t <= time_to_use + window_length * 1000)
            )[:, 0]
            res[i] = np.sum(damage[idx])

        plt.figure()
        plt.plot(x / 1000, res)
        plt.title("{} in a time window of {}s".format(title_prefix, window_length))
        plt.xlabel("Starting Time of Window")
        plt.ylabel("Average damage in time window")
        plt.show(block=False)
        return res

    @staticmethod
    def display_damage_snapshots_in_time_window(per_skill_damage, window_length):
        DisplayUtils.display_damage_over_time(
            [float(x.expected_damage) for x in per_skill_damage],
            [float(x.snapshot_time) for x in per_skill_damage],
            window_length,
            title_prefix="Snapshotted Damage Done",
        )

    @staticmethod
    def display_kill_time_estimates(kill_times):
        num_examples = len(kill_times)
        kill_time_success = list(filter(lambda x: x is not None, kill_times))
        num_kill_succeeded = len(kill_time_success)
        print("Num success: {}. Total: {}".format(num_kill_succeeded, num_examples))

        if num_kill_succeeded == 0:
            print("Boss cannot be killed with given rotations")
            return

        count, bins_count = np.histogram(kill_time_success, bins=500)
        plt.figure()
        pdf = (num_kill_succeeded / num_examples) * count / sum(count)
        plt.plot(bins_count[1:], pdf)
        plt.title("Kill time")
        plt.ylabel("Probability")
        plt.xlabel("Time")

        plt.figure()
        plt.plot(bins_count[1:], np.cumsum(pdf))
        plt.title("Probability of killing boss at time <= T")
        plt.xlabel("Time=T")
        plt.ylabel("Probability")


# @title execute_rotation
def execute_rotation(rb, skill_library, num_samples=200000):
    stats = rb.get_stats()
    db = DamageBuilder(stats, skill_library)
    start = time.time()
    sim = DamageSimulator(
        stats, db.get_damage_instances(rb.get_skill_timing()), num_samples
    )
    end = time.time()
    print("Time taken: {}".format(end - start))
    dps = sim.get_dps()
    damage = sim.get_raw_damage()
    per_skill_damage = sim.get_per_skill_damage(rb)
    damage_ranges = sim.get_damage_ranges()
    t = sim.get_damage_time()
    return dps, damage, per_skill_damage, damage_ranges, t


def execute_rotation_and_display_results(
    rotation_name, rotation_library=ROTATION_LIBRARY, skill_library=SKILL_LIBRARY
):
    rotation_to_use = rotation_library[rotation_name]
    dps, damage, per_skill_damage, damage_ranges, t = execute_rotation(
        rotation_to_use, skill_library, num_samples=100000
    )

    print("Results: ")

    DisplayUtils.print_button_press_timings(rotation_to_use)
    DisplayUtils.print_damage_applications(per_skill_damage)
    DisplayUtils.print_damage_details(
        per_skill_damage, damage_ranges, status_effect_names_only=True
    )

    if len(per_skill_damage) > 0:
        DisplayUtils.display_damage_snapshots_in_time_window(
            per_skill_damage, window_length=15
        )
        DisplayUtils.display_results(
            dps,
            title="DPS over {} s".format(per_skill_damage[-1].application_time / 1000),
            display_cumulative=False,
        )

    DisplayUtils.print_results(dps, title="Average DPS")
    DisplayUtils.print_results(damage, title="Average Damage")

    print("---Expected max damage over N runs---")
    for num_runs in [1, 5, 10, 20, 50, 100]:
        print(
            "{} Runs: {:.2f}".format(
                num_runs,
                RotationAnalysisUtils.get_expected_max_in_k_runs(
                    dps, num_runs, num_trials=10000
                ),
            )
        )


def add_to_rotation_library(rotation_name, rb, rotation_library):
    if rotation_name in rotation_library:
        print('Updating rotation "{}" in the rotation library.'.format(rotation_name))
    rotation_library[rotation_name] = rb


####1

####2
# @title Example of adding a rotation directly in the sim


def add_my_rotation(rotation_library=ROTATION_LIBRARY, skill_library=SKILL_LIBRARY):
    # input your stats here (TODO: etro and xivgear links).
    # these stats include food only; 5% party buffs are added automatically during the sim.
    stats = Stats(
        wd=132,
        weapon_delay=3.36,
        main_stat=3330,
        det_stat=2182,
        crit_stat=2596,
        dh_stat=940,
        speed_stat=400,
        tenacity=601,
        job_class="WAR",
        version=GAME_VERSION
    )

    rb = RotationBuilder(
        stats,
        skill_library,
        ignore_trailing_dots=True,
        enable_autos=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rotation_name = "My Rotation"

    # Example of party buffs/debuffs.
    # This sim supports all buffs/debuffs up to Endwalker (Dawntrail coming soon).
    # Generally, just type in 1) the time the buff/debuff is used, 2) the name of
    # the name of the skill that triggers the buff/debuff as it appears on the
    # FF14 job site, and 3) the job class it belongs to. For skills that apply a
    # buff/debuff that also have damage, you may need to specify that you only
    # want to add the buff/debuff portion. Eg:
    #    rb.add(6.3, 'Mug', job_class='NIN', skill_modifier=SkillModifier(with_condition='Debuff Only'))
    rb.add(6.3, "Chain Stratagem", job_class="SCH")
    rb.add(7.1, "Battle Litany", job_class="DRG")
    rb.add(0.8, "Arcane Circle", job_class="RPR")
    rb.add(6.28, "Embolden", job_class="RDM")
    rb.add(
        6.3,
        "Dokumori",
        job_class="NIN",
        skill_modifier=SkillModifier(with_condition="Debuff Only"),
    )

    # Example of rotation of interest.
    # Generally, you just type in the name of the skill you want to use as it appears
    # on the FF14 job site. For certain special conditions (eg, no positional), you may have to use
    # the skill_modifier field to indicate the condition under which you're using the skill.
    # Example of SkillModifier:
    # For SAM:
    #    rb.add_next('Gekko', skill_modifier=SkillModifier(with_condition='No Positional'))
    # Will indicate that Gekko was used, but the positional was not hit. Note that
    # the sim will automatically track combos and conditions that can be inferred
    # from skill usage (eg, using Inner Release on WAR, Meikyo Shisui on SAM) that
    # result in changes to skills (guaranteed crit/dh for Inner Release,
    # automatically meeting combo requirements for Meikyo Shisui). Please see the
    # class SkillModifier and the corresponding class's skill library for
    # information on the conditionals.
    rb.add_next("Tomahawk")
    rb.add_next("Infuriate")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Storm's Eye")
    rb.add_next("Inner Release")
    rb.add_next("Inner Chaos")
    rb.add_next("Upheaval")
    rb.add_next("Onslaught")
    rb.add_next("Primal Rend")
    rb.add_next("Inner Chaos")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Fell Cleave")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Storm's Path")
    rb.add_next("Fell Cleave")
    rb.add_next("Inner Chaos") 
    # New 7.0 skills; I have no idea where they go
    # in the rotation, so here they are.   
    rb.add_next("Primal Ruination")
    rb.add_next("Primal Wrath")

    add_to_rotation_library(rotation_name, rb, rotation_library)


add_my_rotation(ROTATION_LIBRARY, SKILL_LIBRARY)

####2
####3
#@title Example of adding a rotation from a CSV

# This is the same as add_my_rotation(...), but where the rotation is specified
# in a CSV file. For the example CSV file, please refer to:
# https://github.com/Amarantine-xiv/Amas-FF14-Combat-Sim/blob/main/my_rotation.csv
# If you'd like to create your own CSV files, feel free to! Follow the example
# in my_rotation.csv (see the link above). Note the names of the columns!!! To upload
# your CSV rotation file to this workspace, click the folder icon on the left <----
# then the upload icon (file with an up arrow). Navigate to your file, and select it.
# It should then be accessible in this workbook. You may overwrite the file at any time.
# If you prefer a Google Drive sheets example, you can use this one as template:
# https://docs.google.com/spreadsheets/d/1wvq7QDVic3SLZ5may3_1fNfOYF9vCufF04E4yDfSoI4.
# If using the Drive sheet, you will have to:
#   1) download it (File->Download->Comma-separated values (.csv)), and
#   2) upload the file to this workspace
#      i) Click the Folder icon on the left <--- in the sidebar.
#     ii) Click the file with the up arrow on it.
#    iii) Navigate to the file you downloaded, and click on that to upload to this workspace.
#   3) (Optional) Set the csv_filename and rotation_name entries to your uploaded file name, and name the rotation whatever you like.
#
# If you find this a hassle, let Amarantine know (on Discord or Github).
# Amarantine can enable reading directly from your Drive, though you would have
# to grant this notebook/app some permissions which can be scary, to be honest.
def add_my_rotation_from_CSV(rotation_library=ROTATION_LIBRARY, skill_library=SKILL_LIBRARY, csv_filename='', rotation_name= ''):
  stats = Stats(wd=132, weapon_delay=3.36, main_stat=3330, det_stat=2182, crit_stat=2596, dh_stat=940, speed_stat=400, tenacity=601, job_class = 'WAR', version='7.0')
  rb = RotationBuilder(stats, SKILL_LIBRARY, ignore_trailing_dots=True, enable_autos=True, snap_dots_to_server_tick_starting_at=0)

  if not os.path.exists(csv_filename):
    print('File does not exist: {}. Make sure you are in the right directory and have the right file name (see the folder icon on the left <----).'.format(csv_filename))
  else:
    rb, _ = CSVUtils.populate_rotation_from_csv(rb, csv_filename)
  add_to_rotation_library(rotation_name, rb, rotation_library)

add_my_rotation_from_CSV(ROTATION_LIBRARY, SKILL_LIBRARY, csv_filename='my_rotation.csv', rotation_name='My CSV Rotation')

####3


####5
#@title Example of executing a rotation (pre-set, CSV uploaded, or entered into the sim directly)

# You just need to specify the name of the rotation you want to use.

# This is a pre-set rotation. Uncomment to use.
rotation_to_use= 'VPR 7.0'

# This is the rotation we filled in directly in 'Example of adding a rotation directly in the sim'. Uncomment to use.
# rotation_to_use= 'My Rotation'

# This is the rotation we provided from a CSV in 'Example of adding a rotation from a CSV'. Uncomment to use.
# rotation_to_use= 'My CSV Rotation'

execute_rotation_and_display_results(rotation_to_use)
####5