from simulator.calcs.damage_class import DamageClass
from simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from simulator.game_data.patch_655.convenience_timings import (
    get_auto_timing,
    get_instant_timing_spec,
)
from simulator.sim_consts import SimConsts
from simulator.skills.skill import Skill
from simulator.specs.combo_spec import ComboSpec
from simulator.specs.damage_spec import DamageSpec
from simulator.specs.follow_up import FollowUp
from simulator.specs.status_effect_spec import StatusEffectSpec
from simulator.specs.timing_spec import TimingSpec


def add_sam_skills(skill_library):
    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("SAM")
    _fugetsu_follow_up = FollowUp(
        skill=Skill(
            name="_Fugetsu buff",
            is_GCD=False,
            buff_spec=StatusEffectSpec(damage_mult=1.13, duration=40000),
        ),
        delay_after_parent_application=650,
    )
    _fuka_follow_up = FollowUp(
        skill=Skill(
            name="_Fuka buff",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.13,
                auto_attack_delay_reduction=0.13,
                duration=40000,
            ),
        ),
        delay_after_parent_application=0,
    )
    skill_library.add_skill(
        Skill(
            name="Auto",
            is_GCD=False,
            timing_spec=auto_timing,
            damage_spec=DamageSpec(
                potency=90, damage_class=DamageClass.AUTO, trait_damage_mult_override=1
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hakaze",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=200),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )

    jinpu_follow_up = FollowUp(
        skill=Skill(name="Jinpu", damage_spec=DamageSpec(potency=280)),
        delay_after_parent_application=620,
    )
    jinpu_no_combo_follow_up = FollowUp(
        skill=Skill(name="Jinpu", damage_spec=DamageSpec(potency=120)),
        delay_after_parent_application=620,
    )
    skill_library.add_skill(
        Skill(
            name="Jinpu",
            is_GCD=True,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Hakaze",)),),
                "No Combo": (ComboSpec(combo_actions=("Hakaze",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Hakaze",)),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    jinpu_follow_up,
                    _fugetsu_follow_up,
                ),
                "No Combo": (jinpu_no_combo_follow_up,),
            },
        )
    )

    enhanced_enpi_buff = Skill(
        name="Enhanced_Enpi",
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=1,
            duration=15 * 1000,
            skill_allowlist=("Enpi",),
        ),
    )
    enhanced_enpi_follow_up = FollowUp(
        skill=enhanced_enpi_buff, delay_after_parent_application=0
    )

    skill_library.add_skill(
        Skill(
            name="Enpi",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=100),
                "Enhanced_Enpi": DamageSpec(potency=260),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=710
            ),
        )
    )

    shifu_follow_up = FollowUp(
        skill=Skill(name="Shifu", damage_spec=DamageSpec(potency=280)),
        delay_after_parent_application=800,
    )
    shifu_no_combo_follow_up = FollowUp(
        skill=Skill(name="Shifu", damage_spec=DamageSpec(potency=120)),
        delay_after_parent_application=800,
    )
    skill_library.add_skill(
        Skill(
            name="Shifu",
            is_GCD=True,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Hakaze",)),),
                "No Combo": (ComboSpec(combo_actions=("Hakaze",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Hakaze",)),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    shifu_follow_up,
                    _fuka_follow_up,
                ),
                "No Combo": (shifu_no_combo_follow_up,),
            },
        )
    )

    gekko_follow_up = FollowUp(
        skill=Skill(name="Gekko", damage_spec=DamageSpec(potency=380)),
        delay_after_parent_application=760,
    )
    gekko_no_combo_follow_up = FollowUp(
        skill=Skill(name="Gekko", damage_spec=DamageSpec(potency=170)),
        delay_after_parent_application=760,
    )
    gekko_no_pos_follow_up = FollowUp(
        skill=Skill(name="Gekko", damage_spec=DamageSpec(potency=330)),
        delay_after_parent_application=760,
    )
    gekko_no_pos_no_combo_follow_up = FollowUp(
        skill=Skill(name="Gekko", damage_spec=DamageSpec(potency=120)),
        delay_after_parent_application=760,
    )
    skill_library.add_skill(
        Skill(
            name="Gekko",
            is_GCD=True,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Jinpu",)),),
                "No Combo": (ComboSpec(combo_actions=("Jinpu",)),),
                "No Positional": (ComboSpec(combo_actions=("Jinpu",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Jinpu",)),
                ),
                "No Positional, Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Jinpu",)),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (gekko_follow_up,),
                "No Combo, No Positional": (gekko_no_pos_no_combo_follow_up,),
                "No Combo": (gekko_no_combo_follow_up,),
                "No Positional": (gekko_no_pos_follow_up,),
                "Meikyo Shisui": (gekko_follow_up, _fugetsu_follow_up),
                "Meikyo Shisui, No Combo, No Positional": (
                    gekko_no_pos_follow_up,
                    _fugetsu_follow_up,
                ),
                "Meikyo Shisui, No Combo": (gekko_follow_up, _fugetsu_follow_up),
                "Meikyo Shisui, No Positional": (
                    gekko_no_pos_follow_up,
                    _fugetsu_follow_up,
                ),
            },
        )
    )
    higanbana_dot = Skill(
        name="_Higanbana dot",
        is_GCD=False,
        damage_spec=DamageSpec(potency=45, damage_class=DamageClass.PHYSICAL_DOT),
    )
    higanbana_follow_up = FollowUp(
        skill=higanbana_dot,
        delay_after_parent_application=0,
        dot_duration=60 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
    )
    iaijutsu_timing = TimingSpec(
        base_cast_time=1300,
        affected_by_speed_stat=False,
        affected_by_haste_buffs=False,
        animation_lock=0,
        application_delay=620,
    )

    skill_library.add_skill(
        Skill(
            name="Higanbana",
            is_GCD=True,
            damage_spec=DamageSpec(potency=200),
            timing_spec=iaijutsu_timing,
            follow_up_skills=(higanbana_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Tenka Goken",
            is_GCD=True,
            damage_spec=DamageSpec(potency=300),
            timing_spec=iaijutsu_timing,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Midare Setsugekka",
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=640, guaranteed_crit=ForcedCritOrDH.FORCE_YES
            ),
            timing_spec=iaijutsu_timing,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Kaeshi: Higanbana",
            is_GCD=True,
            damage_spec=DamageSpec(potency=200),
            timing_spec=instant_timing_spec,
            follow_up_skills=(higanbana_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Kaeshi: Goken",
            is_GCD=True,
            damage_spec=DamageSpec(potency=300),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Kaeshi: Setsugekka",
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=640, guaranteed_crit=ForcedCritOrDH.FORCE_YES
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )

    magnetsu_follow_up = FollowUp(
        skill=Skill(name="Magnetsu", damage_spec=DamageSpec(potency=120)),
        delay_after_parent_application=620,
    )
    magnetsu_no_combo_follow_up = FollowUp(
        skill=Skill(name="Magnetsu", damage_spec=DamageSpec(potency=100)),
        delay_after_parent_application=620,
    )
    skill_library.add_skill(
        Skill(
            name="Mangetsu",
            is_GCD=True,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Fuko",)),),
                "No Combo": (ComboSpec(combo_actions=("Fuko",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Fuko",)),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (magnetsu_follow_up, _fugetsu_follow_up),
                "No Combo": (magnetsu_no_combo_follow_up,),
            },
        )
    )

    kasha_follow_up = FollowUp(
        skill=Skill(name="Kasha", damage_spec=DamageSpec(potency=380)),
        delay_after_parent_application=620,
    )
    kasha_no_combo_follow_up = FollowUp(
        skill=Skill(name="Kasha", damage_spec=DamageSpec(potency=170)),
        delay_after_parent_application=620,
    )
    kasha_no_pos_follow_up = FollowUp(
        skill=Skill(name="Kasha", damage_spec=DamageSpec(potency=330)),
        delay_after_parent_application=620,
    )
    kasha_no_pos_no_combo_follow_up = FollowUp(
        skill=Skill(name="Kasha", damage_spec=DamageSpec(potency=120)),
        delay_after_parent_application=620,
    )
    skill_library.add_skill(
        Skill(
            name="Kasha",
            is_GCD=True,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Shifu",)),),
                "No Combo": (ComboSpec(combo_actions=("Shifu",)),),
                "No Positional": (ComboSpec(combo_actions=("Shifu",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Shifu",)),
                ),
                "No Positional, Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Shifu",)),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (kasha_follow_up,),
                "No Combo, No Positional": (kasha_no_pos_no_combo_follow_up,),
                "No Combo": (kasha_no_combo_follow_up,),
                "No Positional": (kasha_no_pos_follow_up,),
                "Meikyo Shisui": (kasha_follow_up, _fuka_follow_up),
                "Meikyo Shisui, No Combo, No Positional": (
                    kasha_no_pos_follow_up,
                    _fuka_follow_up,
                ),
                "Meikyo Shisui, No Combo": (kasha_follow_up, _fuka_follow_up),
                "Meikyo Shisui, No Positional": (
                    kasha_no_pos_follow_up,
                    _fuka_follow_up,
                ),
            },
        )
    )
    oka_follow_up = FollowUp(
        skill=Skill(name="Oka", damage_spec=DamageSpec(potency=120)),
        delay_after_parent_application=620,
    )
    oka_no_combo_follow_up = FollowUp(
        skill=Skill(name="Oka", damage_spec=DamageSpec(potency=100)),
        delay_after_parent_application=620,
    )
    skill_library.add_skill(
        Skill(
            name="Oka",
            is_GCD=True,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Fuko",)),),
                "No Combo": (ComboSpec(combo_actions=("Fuko",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Fuko",)),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (oka_follow_up, _fuka_follow_up),
                "No Combo": (oka_no_combo_follow_up,),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Yukikaze",
            is_GCD=True,
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Hakaze",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Hakaze",)),
                ),
                "No Combo": (ComboSpec(combo_actions=("Hakaze",)),),
            },
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=300),
                "No Combo": DamageSpec(potency=120),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hissatsu: Shinten",
            is_GCD=False,
            damage_spec=DamageSpec(potency=250),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hissatsu: Gyoten",
            is_GCD=False,
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hissatsu: Yaten",
            is_GCD=False,
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=450
            ),
            follow_up_skills=(enhanced_enpi_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hissatsu: Kyuten",
            is_GCD=False,
            damage_spec=DamageSpec(potency=120),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hissatsu: Guren",
            is_GCD=False,
            damage_spec=DamageSpec(potency=500),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hissatsu: Senei",
            is_GCD=False,
            damage_spec=DamageSpec(potency=860),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Shoha",
            is_GCD=False,
            damage_spec=DamageSpec(potency=560),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Shoha II",
            is_GCD=False,
            damage_spec=DamageSpec(potency=200),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fuko",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Ogi Namikiri",
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=860, guaranteed_crit=ForcedCritOrDH.FORCE_YES
            ),
            timing_spec=TimingSpec(
                base_cast_time=1300,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
                application_delay=490,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Kaeshi: Namikiri",
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=860, guaranteed_crit=ForcedCritOrDH.FORCE_YES
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Meikyo Shisui",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=3,
                duration=int(15.1 * 1000),
                skill_allowlist=(
                    "Hakaze",
                    "Jinpu",
                    "Shifu",
                    "Gekko",
                    "Mangetsu",
                    "Kasha",
                    "Oka",
                    "Yukikaze",
                    "Fuko",
                ),
            ),
        )
    )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(
        Skill(name="True North", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Ikishoten", is_GCD=False, timing_spec=instant_timing_spec)
    )

    return skill_library
