from enum import Enum

import click
import click_log
import glom.core as gc
import logging
import pandas as pd
import yaml
from glom import glom, Assign, Delete
from linkml_runtime.utils.schemaview import SchemaView
from pprint import pformat

pd.set_option('display.max_columns', None)

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


meta_view = SchemaView("https://w3id.org/linkml/meta")


class Action(str, Enum):
    ADD_ATTRIBUTE = "add_attribute"
    ADD_EXAMPLE = "add_example"
    OVERWRITE_EXAMPLES = "overwrite_examples"
    REMOVE_ATTRIBUTE = "remove_attribute"
    REPLACE_ANNOTATION = "replace_annotation"
    REPLACE_ATTRIBUTE = "replace_attribute"


def add_attribute_handler(schema_dict, base_path, target, value):
    if target == "" or target is None:
        return

    # todo abort if slot is not multivalued
    #   alert use that value is being split on pipes
    slot_usage = glom(schema_dict, base_path)
    cv_path = target
    values_list = value.split("|")
    values_list = [x.strip() for x in values_list]
    target_already_present = cv_path in slot_usage

    if target_already_present:
        current_value = glom(slot_usage, cv_path)
        target_is_list = type(current_value) == list
        if target_is_list:
            augmented_list = current_value + values_list
        else:
            augmented_list = [current_value] + values_list
    else:
        augmented_list = values_list
    glom(schema_dict, Assign(f"{base_path}.{target}", augmented_list))


def add_example_handler(schema_dict, base_path, target, value):
    if target != "examples":
        return

    slot_usage = glom(schema_dict, base_path)
    cv_path = target
    examples_list = value.split("|")
    examples_list = [x.strip() for x in examples_list]
    assembled_list = []
    for example_item in examples_list:
        assembled_list.append({'value': example_item})

    target_already_present = cv_path in slot_usage
    if target_already_present:
        current_value = glom(slot_usage, cv_path)
        target_is_list = type(current_value) == list
        if target_is_list:
            augmented_list = current_value + assembled_list
        else:
            augmented_list = [current_value] + assembled_list
    else:
        augmented_list = assembled_list
    glom(schema_dict, Assign(f"{base_path}.{target}", augmented_list))


def overwrite_example_handler(schema_dict, base_path, target, value):
    if target != "examples":
        return

    examples_list = value.split("|")
    examples_list = [x.strip() for x in examples_list]
    assembled_list = []
    for example_item in examples_list:
        assembled_list.append({'value': example_item})
    logger.info(f"assembled_list: {assembled_list}")
    glom(schema_dict, Assign(f"{base_path}.{target}", assembled_list))


def replace_annotation_handler(schema_dict, base_path, target, value):
    if target == "" or target is None:
        return

    slot_usage = glom(schema_dict, base_path)
    annotation_object = {
        "tag": target,
        "value": value,
    }
    if "annotations" in slot_usage:
        glom(schema_dict, Assign(f"{base_path}.annotations.{target}", annotation_object))
    else:
        glom(schema_dict, Assign(f"{base_path}.annotations", {target: annotation_object}))


def replace_attribute_handler(schema_dict, base_path, target, value):
    if target == "" or target is None:
        return

    update_path = target
    fiddled_value = value

    # Ideally we could use glom's `missing` parameter to handle building the intermediate structures
    # when using a dotted path, but currently the `missing` Callable isn't called with enough
    # information to determine when to create a list vs. a dict. So we'll have to do it manually.
    # See: https://github.com/mahmoud/glom/issues/224
    target_parts = update_path.split(".")
    full_target = gc.Path.from_text(base_path)
    for index, target in enumerate(target_parts):
        is_last = index == len(target_parts) - 1
        full_target = gc.Path(full_target, target)
        if is_last:
            # If this is the last element of the target path, it's time to assign the value. But
            # first check if the target should be a boolean and convert the value as needed. Note
            # that `bool(value)` is not sufficient because `bool("false") == True`.
            from_meta = meta_view.get_slot(target)
            fm_range = from_meta.range if from_meta else None
            if fm_range == "boolean":
                if value.lower() == "true":
                    fiddled_value = True
                elif value.lower() == "false":
                    fiddled_value = False
                else:
                    logger.warning(f"While setting ${full_target}, boolean value not recognized: {value}")
            glom(schema_dict, Assign(full_target, fiddled_value))
        else:
            # If this is not the last element of the target path, we need to ensure that the
            # intermediate structures are created. If the next target is an integer, we'll assume
            # that the current target should be a list. If the next target is not an integer, we'll
            # assume that the current target should be a dict.
            try:
                next_target = target_parts[index + 1]
                target_length = int(next_target) + 1
            except ValueError:
                target_length = None

            try:
                # If the target is already present, we'll use it as the basis for the next value.
                # If the existing value is a list and the next target is an integer, we'll pad the
                # list with empty dicts to the target length.
                existing_value = glom(schema_dict, full_target)
                if (isinstance(existing_value, list)
                        and target_length is not None
                        and len(existing_value) < target_length):
                    next_value = existing_value + [{} for _ in
                                                   range(target_length - len(existing_value))]
                else:
                    next_value = existing_value
            except gc.PathAccessError:
                # If the target is not present, we'll create the next value as a list of empty dicts
                # if the next target is an integer, or as an empty dict otherwise.
                if target_length is not None:
                    next_value = [{} for _ in range(target_length)]
                else:
                    next_value = {}
            glom(schema_dict, Assign(full_target, next_value))


def remove_attribute_handler(schema_dict, base_path, target, value):
    if target == "" or target is None:
        return

    glom(schema_dict, Delete(f"{base_path}.{target}"))


handler_map = {
    Action.ADD_ATTRIBUTE: add_attribute_handler,
    Action.ADD_EXAMPLE: add_example_handler,
    Action.OVERWRITE_EXAMPLES: overwrite_example_handler,
    Action.REMOVE_ATTRIBUTE: remove_attribute_handler,
    Action.REPLACE_ANNOTATION: replace_annotation_handler,
    Action.REPLACE_ATTRIBUTE: replace_attribute_handler,
}


@click.command()
@click_log.simple_verbosity_option(logger, default="WARNING")
@click.option("--yaml_input", type=click.Path(exists=True), required=True)
@click.option("--modifications_config_tsv", type=click.Path(exists=True), required=True)
@click.option("--validation_config_tsv", type=click.Path(exists=True), required=True)
@click.option("--yaml_output", type=click.Path(), required=True)
def modifications_and_validation(yaml_input: str, modifications_config_tsv: str, validation_config_tsv: str,
                                 yaml_output: str):
    """
    :param yaml_input:
    :param config_tsv:
    :param yaml_output:
    :return:
    """

    # todo be defensive
    # parameterize?

    with open(yaml_input, 'r') as stream:
        try:
            schema_dict = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            logger.warning(e)

    mod_rule_frame = pd.read_csv(modifications_config_tsv, sep="\t")
    mod_rule_frame['class'] = mod_rule_frame['class'].str.split("|")
    mod_rule_frame = mod_rule_frame.explode('class')

    # todo break out overwrites first
    for row_num, row in mod_rule_frame.iterrows():

        base_path = f"classes.{row['class']}.slot_usage.{row['slot']}"

        class_query = f"classes.{row['class']}"
        class_results_dict = glom(schema_dict, class_query)
        if "slot_usage" not in class_results_dict:
            logger.info(f"slot_usage missing from {row['class']}")
            add_usage_path = f"classes.{row['class']}.slot_usage"
            add_usage_dict = {"placeholder": {"name": "placeholder"}}
            glom(schema_dict, Assign(add_usage_path, add_usage_dict))
            logger.info(pformat(schema_dict['classes'][row['class']]['slot_usage']))
        else:
            logger.info(f"slot_usage already present in {row['class']}")
            slot_usage = schema_dict['classes'][row['class']]['slot_usage']
            if len(slot_usage.keys()) > 1 and "placeholder" in slot_usage.keys():
                del slot_usage['placeholder']

        usage_query = f"classes.{row['class']}.slot_usage"
        usage_dict = glom(schema_dict, usage_query)
        if row['slot'] not in usage_dict:
            logger.info(f"Adding {row['slot']} to {row['class']}'s slot_usage")
            add_slot_path = f"classes.{row['class']}.slot_usage.{row['slot']}"
            add_slot_dict = {"name": f"{row['slot']}"}
            glom(schema_dict, Assign(add_slot_path, add_slot_dict))
            logger.info(pformat(schema_dict['classes'][row['class']]['slot_usage'][row['slot']]))
        else:
            logger.info(f"{row['slot']} already present in {row['class']}'s slot_usage")

        try:
            logger.info(f"{row['slot']} {row['action']} {row['target']} {row['value']}")

            handler = handler_map.get(row['action'])
            if handler is not None:
                handler(schema_dict, base_path, row['target'], row['value'])
            else:
                action_str = row['action'] if not pd.isna(row['action']) else '<empty>'
                logger.warning(f"No handler for action '{action_str}' in row {row_num}")

        # todo refactor

        except gc.PathAccessError as e:
            logger.warning(e)

    # ============== apply validation rules ============== #
    # ==================================================== #

    # fetch validation_converter sheet as pd df
    validation_rules_df = pd.read_csv(validation_config_tsv, sep="\t", header=0)

    # loop through all induced slots associated with all classes
    # from the schema_dict and modify slots in place

    logger.info(f"VALIDATION UPDATES")

    for class_name, class_defn in schema_dict["classes"].items():

        # check if the slot_usage key exists in each class definition
        if "slot_usage" in class_defn and len(class_defn["slot_usage"]) > 0:

            # loop over slot_usage items
            for slot_name, slot_defn in schema_dict["classes"][class_name][
                "slot_usage"
            ].items():
                if "range" in slot_defn:
                    replacement_ranges = validation_rules_df.loc[
                        (validation_rules_df['from_type'] == 'linkml range') &
                        (validation_rules_df['to_type'] == 'DH datatype') &
                        (validation_rules_df['from_val'] == slot_defn['range']), "to_val"
                    ]
                    if len(replacement_ranges) > 0:
                        logger.info(
                            f"class_name: {class_name}; slot_name: {slot_defn['name']}; range: {slot_defn['range']}")
                        logger.info(f"replacement_ranges #{len(replacement_ranges)}: {replacement_ranges.iloc[0]}")
                        slot_defn['range'] = replacement_ranges.iloc[0]
                    replacement_patterns = validation_rules_df.loc[
                        (validation_rules_df['from_type'] == 'linkml range') &
                        (validation_rules_df['to_type'] == 'DH pattern regex') &
                        (validation_rules_df['from_val'] == slot_defn['range']), "to_val"
                    ]
                    if len(replacement_patterns) > 0:
                        logger.info(
                            f"class_name: {class_name}; slot_name: {slot_defn['name']}; range: {slot_defn['range']}")
                        logger.info(
                            f"replacement_patterns #{len(replacement_patterns)}: {replacement_patterns.iloc[0]}")
                        slot_defn['pattern'] = replacement_patterns.iloc[0]

                if "string_serialization" in slot_defn:
                    logger.info(
                        f"class_name: {class_name}; slot_name: {slot_defn['name']}; string_serialization: {slot_defn['string_serialization']}"
                    )
                    replacement_ranges = validation_rules_df.loc[
                        (validation_rules_df['from_type'].isin(
                            ['linkml string_serialization', 'MIxS string serialization'])) &
                        (validation_rules_df['to_type'] == 'DH datatype') &
                        (validation_rules_df['from_val'] == slot_defn['string_serialization']), "to_val"
                    ]
                    if len(replacement_ranges) > 0:
                        logger.info(
                            f"class_name: {class_name}; slot_name: {slot_defn['name']}; string_serialization: {slot_defn['string_serialization']}")
                        logger.info(f"replacement_ranges #{len(replacement_ranges)}: {replacement_ranges.iloc[0]}")
                        slot_defn['range'] = replacement_ranges.iloc[0]
                    replacement_patterns = validation_rules_df.loc[
                        (validation_rules_df['from_type'].isin(
                            ['linkml string_serialization', 'MIxS string serialization'])) &
                        (validation_rules_df['to_type'] == 'DH pattern regex') &
                        (validation_rules_df['from_val'] == slot_defn['string_serialization']), "to_val"
                    ]
                    if len(replacement_patterns) > 0:
                        logger.info(
                            f"class_name: {class_name}; slot_name: {slot_defn['name']}; range: {slot_defn.get('range')}")
                        logger.info(
                            f"replacement_patterns #{len(replacement_patterns)}: {replacement_patterns.iloc[0]}")
                        slot_defn['pattern'] = replacement_patterns.iloc[0]

        else:
            logger.warning(f"no slot_usage for {class_name}")
    with open(yaml_output, 'w') as f:
        yaml.dump(schema_dict, f, default_flow_style=False, sort_keys=False)


if __name__ == '__main__':
    modifications_and_validation()
