from simulator.calcs.damage_class import DamageClass
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


def add_nin_skills(skill_library):
    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()
    mudra_timing_spec = TimingSpec(
        base_cast_time=0,
        gcd_base_recast_time=500,
        affected_by_speed_stat=False,
        affected_by_haste_buffs=False,
        animation_lock=0,
    )

    skill_library.set_current_job_class("NIN")

    # TODO: this is bugged. We are setting delay_after_parent_application=88 and
    # not snapshotting with parent to mimic the 0.088s snapshot delay on anything
    # bunshin. This in return ignores when the damage actually comes out.
    bunshin_melee_follow_up_ = FollowUp(
        skill=Skill(
            name="_Bunshin_melee",
            is_GCD=False,
            damage_spec=DamageSpec(
                potency=160, damage_class=DamageClass.PET, pet_job_mod_override=100
            ),
            status_effect_denylist=("Dragon Sight",),
        ),
        delay_after_parent_application=88,
        snapshot_buffs_with_parent=False,
        snapshot_debuffs_with_parent=False,
    )
    bunshin_ranged_follow_up_ = FollowUp(
        skill=Skill(
            name="_Bunshin_ranged",
            is_GCD=False,
            damage_spec=DamageSpec(
                potency=160, damage_class=DamageClass.PET, pet_job_mod_override=100
            ),
            status_effect_denylist=("Dragon Sight",),
        ),
        delay_after_parent_application=88,
        snapshot_buffs_with_parent=False,
        snapshot_debuffs_with_parent=False,
    )
    bunshin_area_follow_up_ = FollowUp(
        skill=Skill(
            name="_Bunshin_area",
            is_GCD=False,
            damage_spec=DamageSpec(
                potency=80, damage_class=DamageClass.PET, pet_job_mod_override=100
            ),
            status_effect_denylist=("Dragon Sight",),
        ),
        delay_after_parent_application=88,
        snapshot_buffs_with_parent=False,
        snapshot_debuffs_with_parent=False,
    )

    _huton_follow_up_huton = FollowUp(
        skill=Skill(
            name="_Huton buff",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.15,
                auto_attack_delay_reduction=0.15,
                duration=60 * 1000,
                max_duration=60 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )

    _huton_follow_up_hakke = FollowUp(
        skill=Skill(
            name="_Huton buff",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.15,
                auto_attack_delay_reduction=0.15,
                duration=10 * 1000,
                max_duration=60 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )
    _huton_follow_up_armor_crush = FollowUp(
        skill=Skill(
            name="_Huton buff",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.15,
                auto_attack_delay_reduction=0.15,
                duration=30 * 1000,
                max_duration=60 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )
    _dream_follow_ups = (
        FollowUp(
            skill=Skill(
                name="_dream_within_a_dream1",
                is_GCD=False,
                damage_spec=DamageSpec(150),
            ),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=False,
            delay_after_parent_application=700,
        ),
        FollowUp(
            skill=Skill(
                name="_dream_within_a_dream2",
                is_GCD=False,
                damage_spec=DamageSpec(150),
            ),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=False,
            delay_after_parent_application=850,
        ),
        FollowUp(
            skill=Skill(
                name="_dream_within_a_dream3",
                is_GCD=False,
                damage_spec=DamageSpec(150),
            ),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=False,
            delay_after_parent_application=1000,
        ),
    )

    doton_dot = Skill(
        name="_Doton dot",
        is_GCD=False,
        damage_spec=DamageSpec(potency=80, damage_class=DamageClass.PHYSICAL_DOT),
    )
    doton_follow_up = FollowUp(
        skill=doton_dot,
        delay_after_parent_application=0,
        dot_duration=18 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=False,
    )
    doton_dot_hollow_nozuchi = Skill(
        name="_Doton dot (hollow nozuchi)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=50, damage_class=DamageClass.PHYSICAL_DOT),
    )
    doton_hollow_nozuchi_follow_up = FollowUp(
        skill=doton_dot_hollow_nozuchi,
        delay_after_parent_application=0,
        dot_duration=18 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=False,
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

    spinning_edge_damage = Skill(
        name="Spinning Edge", damage_spec=DamageSpec(potency=220)
    )
    spinning_edge_follow_up = FollowUp(
        skill=spinning_edge_damage, delay_after_parent_application=400
    )
    skill_library.add_skill(
        Skill(
            name="Spinning Edge",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (spinning_edge_follow_up,),
                "Bunshin": (bunshin_melee_follow_up_, spinning_edge_follow_up),
            },
        )
    )

    gust_slash_damage_follow_up = FollowUp(
        Skill(name="Gust Slash", damage_spec=DamageSpec(potency=320)),
        delay_after_parent_application=400,
    )
    gust_slash_damage_no_combo_follow_up = FollowUp(
        Skill(name="Gust Slash", damage_spec=DamageSpec(potency=160)),
        delay_after_parent_application=400,
    )
    skill_library.add_skill(
        Skill(
            name="Gust Slash",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Spinning Edge",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (gust_slash_damage_follow_up,),
                "No Combo": (gust_slash_damage_no_combo_follow_up,),
                "Bunshin": (bunshin_melee_follow_up_, gust_slash_damage_follow_up),
                "Bunshin, No Combo": (
                    bunshin_melee_follow_up_,
                    gust_slash_damage_no_combo_follow_up,
                ),
            },
        )
    )

    throwing_dagger_follow_up = FollowUp(
        skill=Skill(name="Throwing Dagger", damage_spec=DamageSpec(potency=120)),
        delay_after_parent_application=620,
    )
    skill_library.add_skill(
        Skill(
            name="Throwing Dagger",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (throwing_dagger_follow_up,),
                "Bunshin": (throwing_dagger_follow_up, bunshin_ranged_follow_up_),
            },
        )
    )

    mug_damage_follow_up = FollowUp(
        skill=Skill(name="Mug", damage_spec=DamageSpec(potency=150)),
        delay_after_parent_application=620,
    )
    mug_debuff_follow_up = FollowUp(
        skill=Skill(
            name="Mug",
            debuff_spec=StatusEffectSpec(
                damage_mult=1.05, duration=int(20.5 * 1000), is_party_effect=True
            ),
        ),
        delay_after_parent_application=0,
    )
    skill_library.add_skill(
        Skill(
            name="Mug",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    mug_damage_follow_up,
                    mug_debuff_follow_up,
                ),
                "Debuff Only": (mug_debuff_follow_up,),
            },
        )
    )

    trick_damage_follow_up = FollowUp(
        skill=Skill(name="Trick Attack", damage_spec=DamageSpec(potency=400)),
        delay_after_parent_application=800,
    )
    trick_damage_no_pos_follow_up = FollowUp(
        skill=Skill(name="Trick Attack", damage_spec=DamageSpec(potency=300)),
        delay_after_parent_application=800,
    )

    trick_debuff_follow_up = FollowUp(
        skill=Skill(
            name="Trick Attack (Debuff)",
            debuff_spec=StatusEffectSpec(damage_mult=1.10, duration=int(15.77 * 1000)),
        ),
        delay_after_parent_application=0,
    )
    skill_library.add_skill(
        Skill(
            name="Trick Attack",
            is_GCD=False,
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    trick_damage_follow_up,
                    trick_debuff_follow_up,
                ),
                "No Positional": (
                    trick_damage_no_pos_follow_up,
                    trick_debuff_follow_up,
                ),
            },
            timing_spec=instant_timing_spec,
        )
    )

    aeolian_edge_follow_up = FollowUp(
        skill=Skill(name="Aeolian Edge", damage_spec=DamageSpec(440)),
        delay_after_parent_application=540,
    )
    aeolian_edge_no_combo_follow_up = FollowUp(
        skill=Skill(name="Aeolian Edge", damage_spec=DamageSpec(200)),
        delay_after_parent_application=540,
    )
    aeolian_edge_no_pos_follow_up = FollowUp(
        skill=Skill(name="Aeolian Edge", damage_spec=DamageSpec(380)),
        delay_after_parent_application=540,
    )
    aeolian_edge_no_pos_no_combo_follow_up = FollowUp(
        skill=Skill(name="Aeolian Edge", damage_spec=DamageSpec(140)),
        delay_after_parent_application=540,
    )
    skill_library.add_skill(
        Skill(
            name="Aeolian Edge",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Gust Slash",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (aeolian_edge_follow_up,),
                "No Combo": (aeolian_edge_no_combo_follow_up,),
                "No Positional": (aeolian_edge_no_pos_follow_up,),
                "No Combo, No Positional": (aeolian_edge_no_pos_no_combo_follow_up,),
                "Bunshin": (aeolian_edge_follow_up, bunshin_melee_follow_up_),
                "Bunshin, No Combo": (
                    aeolian_edge_no_combo_follow_up,
                    bunshin_melee_follow_up_,
                ),
                "Bunshin, No Positional": (
                    aeolian_edge_no_pos_follow_up,
                    bunshin_melee_follow_up_,
                ),
                "Bunshin, No Combo, No Positional": (
                    aeolian_edge_no_pos_no_combo_follow_up,
                    bunshin_melee_follow_up_,
                ),
            },
        )
    )

    skill_library.add_skill(
        Skill(name="Ten", is_GCD=True, timing_spec=mudra_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Chi", is_GCD=True, timing_spec=mudra_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Jin", is_GCD=True, timing_spec=mudra_timing_spec)
    )
    death_blossom_follow_up = FollowUp(
        skill=Skill(name="_Death Blossom", damage_spec=DamageSpec(100)),
        delay_after_parent_application=710,
    )
    skill_library.add_skill(
        Skill(
            name="Death Blossom",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (death_blossom_follow_up,),
                "Bunshin": (bunshin_area_follow_up_, death_blossom_follow_up),
            },
        )
    )

    hakke_follow_up = FollowUp(
        skill=Skill(name="Hakke Mujinsatsu", damage_spec=DamageSpec(130)),
        delay_after_parent_application=620,
    )
    hakke_no_combo_follow_up = FollowUp(
        skill=Skill(name="Hakke Mujinsatsu", damage_spec=DamageSpec(100)),
        delay_after_parent_application=620,
    )

    skill_library.add_skill(
        Skill(
            name="Hakke Mujinsatsu",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Death Blossom",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (_huton_follow_up_hakke, hakke_follow_up),
                "No Combo": (hakke_no_combo_follow_up,),
                "Bunshin": (
                    _huton_follow_up_hakke,
                    bunshin_area_follow_up_,
                    hakke_follow_up,
                ),
                "Bunshin, No Combo": (
                    bunshin_area_follow_up_,
                    hakke_no_combo_follow_up,
                ),
            },
        )
    ),

    armor_crush_follow_up = FollowUp(
        skill=Skill(name="Armor Crush", damage_spec=DamageSpec(420)),
        delay_after_parent_application=620,
    )
    armor_crush_no_combo_follow_up = FollowUp(
        skill=Skill(name="Armor Crush", damage_spec=DamageSpec(200)),
        delay_after_parent_application=620,
    )
    armor_crush_no_pos_follow_up = FollowUp(
        skill=Skill(name="Armor Crush", damage_spec=DamageSpec(360)),
        delay_after_parent_application=620,
    )
    armor_crush_no_pos_no_combo_follow_up = FollowUp(
        skill=Skill(name="Armor Crush", damage_spec=DamageSpec(140)),
        delay_after_parent_application=620,
    )
    skill_library.add_skill(
        Skill(
            name="Armor Crush",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Gust Slash",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    armor_crush_follow_up,
                    _huton_follow_up_armor_crush,
                ),
                "No Combo": (armor_crush_no_combo_follow_up,),
                "No Positional": (
                    armor_crush_no_pos_follow_up,
                    _huton_follow_up_armor_crush,
                ),
                "No Combo, No Positional": (armor_crush_no_pos_no_combo_follow_up,),
                "Bunshin": (
                    armor_crush_follow_up,
                    _huton_follow_up_armor_crush,
                    bunshin_melee_follow_up_,
                ),
                "Bunshin, No Combo": (
                    armor_crush_no_combo_follow_up,
                    bunshin_melee_follow_up_,
                ),
                "Bunshin, No Positional": (
                    armor_crush_no_pos_follow_up,
                    _huton_follow_up_armor_crush,
                    bunshin_melee_follow_up_,
                ),
                "Bunshin, No Combo, No Positional": (
                    armor_crush_no_pos_no_combo_follow_up,
                    bunshin_melee_follow_up_,
                ),
            },
        )
    )

    skill_library.add_skill(
        Skill(
            name="Dream Within a Dream",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=_dream_follow_ups,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Huraijin ",
            is_GCD=True,
            damage_spec=DamageSpec(potency=200),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (_huton_follow_up_huton,),
                "Bunshin": (_huton_follow_up_huton, bunshin_melee_follow_up_),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hellfrog Medium",
            is_GCD=False,
            damage_spec=DamageSpec(potency=160),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Bhavacakra",
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=350),
                "Meisui": DamageSpec(potency=500),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Phantom Kamaitachi",
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=600, damage_class=DamageClass.PET, pet_job_mod_override=100
            ),
            timing_spec=TimingSpec(base_cast_time=0, application_delay=1560),
            status_effect_denylist=("Dragon Sight",),
            follow_up_skills=tuple(),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hollow Nozuchi",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=270
            ),
            follow_up_skills=(doton_hollow_nozuchi_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Forked Raiju",
            is_GCD=True,
            damage_spec=DamageSpec(potency=560),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Bunshin": (bunshin_melee_follow_up_,),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fleeting Raiju",
            is_GCD=True,
            damage_spec=DamageSpec(potency=560),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Bunshin": (bunshin_melee_follow_up_,),
            },
        )
    )

    # ninjitsus
    skill_library.add_skill(
        Skill(
            name="Fuma Shuriken",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=450),
                "Ten Chi Jin": DamageSpec(potency=450),
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=890,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=890,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Katon",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=350),
                "Ten Chi Jin": DamageSpec(potency=350),
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=940,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=940,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Raiton",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=650),
                "Ten Chi Jin": DamageSpec(potency=650),
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=710,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=710,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hyoton",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=350),
                "Ten Chi Jin": DamageSpec(potency=350),
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=1160,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=1160,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Huton",
            is_GCD=True,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=0,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=0,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
            follow_up_skills=(_huton_follow_up_huton,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Doton",
            is_GCD=True,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=1300,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=1300,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
            follow_up_skills=(doton_follow_up,),
        )
    ),
    skill_library.add_skill(
        Skill(
            name="Suiton",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=500),
                "Ten Chi Jin": DamageSpec(potency=500),
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    #  application_delay=0,
                    application_delay=980,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=980,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Goka Mekkyaku",
            is_GCD=True,
            damage_spec=DamageSpec(potency=600),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                application_delay=760,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hyosho Ranryu",
            is_GCD=True,
            damage_spec=DamageSpec(potency=1300),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                application_delay=620,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Bunshin",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=5,
                duration=45 * 1000,
                skill_allowlist=(
                    "Spinning Edge",
                    "Gust Slash",
                    "Throwing Dagger",
                    "Aeolian Edge",
                    "Death Blossom",
                    "Hakke Mujinsatsu",
                    "Armor Crush",
                    "Huraijin",
                    "Forked Raiju",
                    "Fleeting Raiju",
                ),
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Ten Chi Jin",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=3,
                duration=6 * 1000,
                skill_allowlist=(
                    "Fuma Shuriken",
                    "Katon",
                    "Raiton",
                    "Hyoton",
                    "Huton",
                    "Doton",
                    "Suiton",
                ),
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Meisui",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=30 * 1000,
                skill_allowlist=("Bhavacakra",),
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Kassatsu",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=15 * 1000,
                damage_mult=1.3,
                skill_allowlist=(
                    "Fuma Shuriken",
                    "Raiton",
                    "Doton",
                    "Suiton",
                    "Goka Mekkyaku",
                    "Huton",
                    "Hyosho Ranryu",
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
        Skill(name="Hide", is_GCD=False, timing_spec=instant_timing_spec)
    )
    return skill_library
