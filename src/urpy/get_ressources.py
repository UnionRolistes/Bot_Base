from importlib import resources


def get_planning_anncmnt_mdl() -> str:
    return resources.read_text('urpy.templates', "planning_annoucement_template.txt")
