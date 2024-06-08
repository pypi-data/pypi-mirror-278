# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from composabl_core.agent.agent import Agent
from composabl_core.agent import SkillGroup
from composabl_core.examples.demo.agent import (
    sensors_box,
    sensors_dictionary,
    sensors_discrete,
    sensors_multi_binary,
    sensors_multi_discrete,
    sensors_tuple,
    target_skill_box,
    target_skill_dictionary,
    target_skill_discrete,
    target_skill_multi_binary,
    target_skill_multi_discrete,
    target_skill_nested_scenario,
    target_skill_tuple,
    target_skill_custom_action_space,
    expert_skill_controller_box,
    pass_through_skill_controller,
)

agent_dictionary = Agent()
agent_dictionary.add_sensors(sensors_dictionary)
agent_dictionary.add_skill(target_skill_dictionary)

agent_box = Agent()
agent_box.add_sensors(sensors_box)
agent_box.add_skill(target_skill_box)

agent_discrete = Agent()
agent_discrete.add_sensors(sensors_discrete)
agent_discrete.add_skill(target_skill_discrete)

agent_multidiscrete = Agent()
agent_multidiscrete.add_sensors(sensors_multi_discrete)
agent_multidiscrete.add_skill(target_skill_multi_discrete)

agent_multibinary = Agent()
agent_multibinary.add_sensors(sensors_multi_binary)
agent_multibinary.add_skill(target_skill_multi_binary)

agent_tuple = Agent()
agent_tuple.add_sensors(sensors_tuple)
agent_tuple.add_skill(target_skill_tuple)

agent_nested_scenario = Agent()
agent_nested_scenario.add_sensors(sensors_dictionary)
agent_nested_scenario.add_skill(target_skill_nested_scenario)

agent_setpoint = Agent()
agent_setpoint.add_sensors(sensors_discrete)
agent_setpoint.add_skill(target_skill_custom_action_space)
agent_setpoint.add_skill(pass_through_skill_controller)
skill_group = SkillGroup(target_skill_custom_action_space, pass_through_skill_controller)
agent_setpoint.add_skill_group(skill_group=skill_group)

agent_controller = Agent()
agent_controller.add_skill(expert_skill_controller_box)
agent_controller.add_sensors(sensors_box)

agents_for_space = {
    "box": agent_box,
    "dictionary": agent_dictionary,
    "discrete": agent_discrete,
    "multidiscrete": agent_multidiscrete,
    "multibinary": agent_multibinary,
    "tuple": agent_tuple,
    "set_point": agent_setpoint,
    "controller_box": agent_controller,
}
