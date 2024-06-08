import time


from ama_xiv_combat_sim.kill_time_estimator.test_kill_time_estimator import TestKillTimeEstimator
from ama_xiv_combat_sim.simulator.calcs.test_compute_damage_utils import TestComputeDamageUtils
from ama_xiv_combat_sim.simulator.game_data.patch_655.test_jobs import TestJobs
# from ama_xiv_combat_sim.simulator.game_data.patch_70.test_jobs import TestJobs
from ama_xiv_combat_sim.simulator.calcs.test_stat_fns import TestStatFns
from ama_xiv_combat_sim.simulator.skills.test_skills import TestSkills
from ama_xiv_combat_sim.simulator.specs.test_timing_spec import TestTimingSpec
from ama_xiv_combat_sim.simulator.test_damage_simulator import TestDamageSimulator
from ama_xiv_combat_sim.simulator.test_end_to_end import TestEndToEnd
from ama_xiv_combat_sim.simulator.test_utils import TestUtils
from ama_xiv_combat_sim.simulator.testing.all_test import AllTest
from ama_xiv_combat_sim.simulator.timeline_builders.test_rotation_builder import TestRotationBuilder
from ama_xiv_combat_sim.simulator.timeline_builders.test_damage_builder import TestDamageBuilder
from ama_xiv_combat_sim.simulator.timeline_builders.test_snapshot_and_application_events import TestSnapshotAndApplicationEvents
from ama_xiv_combat_sim.simulator.timeline_builders.test_rotation_builder_and_damage_builder_integration_test import TestRotationBuilderAndDamageBuilderIntegration
from ama_xiv_combat_sim.simulator.trackers.test_status_effect_spec import TestStatusEffectSpec
from ama_xiv_combat_sim.simulator.trackers.test_status_effect_tracker import TestStatusEffectTracker
from ama_xiv_combat_sim.simulator.trackers.test_job_resource_tracker import TestJobResourceTracker
from ama_xiv_combat_sim.simulator.trackers.test_combo_tracker import TestComboTracker

all_tests = AllTest()
all_tests.register_test_class(TestTimingSpec())
all_tests.register_test_class(TestSkills())
all_tests.register_test_class(TestUtils())
all_tests.register_test_class(TestStatusEffectSpec())
all_tests.register_test_class(TestStatFns())
all_tests.register_test_class(TestRotationBuilder())
all_tests.register_test_class(TestSnapshotAndApplicationEvents())
all_tests.register_test_class(TestStatusEffectTracker())
all_tests.register_test_class(TestJobResourceTracker())
all_tests.register_test_class(TestComboTracker())
all_tests.register_test_class(TestRotationBuilderAndDamageBuilderIntegration())
all_tests.register_test_class(TestDamageBuilder())
all_tests.register_test_class(TestComputeDamageUtils())
all_tests.register_test_class(TestDamageSimulator())
all_tests.register_test_class(TestKillTimeEstimator())
all_tests.register_test_class(TestEndToEnd())
all_tests.register_test_class(TestJobs())

st = time.time()
all_tests.run_all()
end = time.time()
print('Tests completed in {}s.'.format(end-st))