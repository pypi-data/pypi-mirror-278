# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import gymnasium.spaces as spaces
from composabl_core.agent.scenario.scenario import Scenario
from composabl_core.agent.skill.skill import Skill, SkillOptions
from composabl_core.examples.demo.agent import scenarios
from composabl_core.examples.demo.agent.controller import (
    ControllerExpertBox,
    ControllerExpertDict,
    ControllerExpertDiscrete,
    ControllerExpertMultiDiscrete,
    ControllerExpertTuple,
    ControllerRandomBox,
    ControllerRandomDict,
    ControllerRandomDiscrete,
    ControllerRandomMultiDiscrete,
    ControllerRandomTuple,
    ControllerPassThrough,
    ControllerSelector
)
from composabl_core.examples.demo.agent.teacher import (
    Teacher,
    TeacherSpaceBox,
    TeacherSpaceDictionary,
    TeacherSpaceDiscrete,
    TeacherSpaceMultiBinary,
    TeacherSpaceMultiDiscrete,
    TeacherSpaceTuple,
)

expert_skill_controller_box = Skill("expert-controller", ControllerExpertBox)
random_skill_controller_box = Skill("random-controller", ControllerRandomBox)
selector_sill_controller_box = Skill("selector-controller", ControllerSelector)
pass_through_skill_controller = Skill("pass-through-controller", ControllerPassThrough)

expert_skill_controller_discrete = Skill("expert-controller", ControllerExpertDiscrete)
random_skill_controller_discrete = Skill("random-controller", ControllerRandomDiscrete)

expert_skill_controller_multi_discrete = Skill("expert-controller", ControllerExpertMultiDiscrete)
random_skill_controller_multi_discrete = Skill("random-controller", ControllerRandomMultiDiscrete)

expert_skill_controller_dict = Skill("expert-controller", ControllerExpertDict)
random_skill_controller_dict = Skill("random-controller", ControllerRandomDict)

expert_skill_controller_tuple = Skill("expert-controller", ControllerExpertTuple)
random_skill_controller_tuple = Skill("random-controller", ControllerRandomTuple)

target_skill_nested_scenario = Skill("teacher-skill-nested-scenario", Teacher)
target_skill_box = Skill("teacher-skill-box", TeacherSpaceBox)
target_skill_discrete = Skill("teacher-skill-discrete", TeacherSpaceDiscrete)
target_skill_multi_discrete = Skill("teacher-skill-multidiscrete", TeacherSpaceMultiDiscrete)
target_skill_multi_binary = Skill("teacher-skill-multi-binary", TeacherSpaceMultiBinary)
target_skill_dictionary = Skill("teacher-skill-dictionary", TeacherSpaceDictionary)

# used to test resume training with scenarios
target_skill_dictionary.add_scenario({"test": "test"})
target_skill_dictionary.add_scenario({"test": "test", "nested": {"test": "test"}})
target_skill_dictionary.add_scenario({"test": "test", "nested": {"test": "test", "double_nested": {"test": "test"}}})

target_skill_tuple = Skill("teacher-skill-tuple", TeacherSpaceTuple)
target_skill_custom_action_space = Skill("teacher-skill-custom-action-space", TeacherSpaceDiscrete, SkillOptions(action_space=spaces.Discrete(3)))

target_skills = [
    target_skill_nested_scenario,
    target_skill_box,
    target_skill_discrete,
    target_skill_multi_discrete,
    target_skill_multi_binary,
    target_skill_dictionary,
    target_skill_tuple,
    target_skill_custom_action_space
]

for ts in target_skills:
    for scenario_dict in scenarios:
        ts.add_scenario(Scenario(scenario_dict))

target_skill_nested_scenario.add_scenario({
    "test": "test",
    "nested": {
        "test": "test",
        "double_nested": {
            "test": "test"
        }
    }
})

skills_for_space = {
    "box": target_skill_box,
    "discrete": target_skill_discrete,
    "multidiscrete": target_skill_multi_discrete,
    "multibinary": target_skill_multi_binary,
    "dictionary": target_skill_dictionary,
    "tuple": target_skill_tuple,
    "set_point": target_skill_custom_action_space
}
