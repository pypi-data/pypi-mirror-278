__version__="0.1.5"

new_features = [
    "Added atomistic molecule definitions for tip3p, tip4p and tip5p water models. The molecules themselves are called 'SOL', but are placed in different parameter libraries.",
    [
        "Accessible using 'params:AA_tipXp' (e.g. solv:SOL:params:AA_tip4p).",
    ],
    "Also added molecule definitions for 'Na' (SOD) and 'CL' (CLA) ions in the 'AA' parameter library.",
    [
        "Accessible using 'params:AA' (e.g. pos:SOD:params:AA neg:CLA:params:AA).",
    ],
    "",
    "Added 'rotate_lipids' subargument to membrane argument which has two options:",
    [
        "True (default): Each lipid is rotated randomly around their z-axis",
        "False: Disables lipid rotation. All lipids will face the same direction.",
    ],
    "",
    "Added '--version'/'-version' argument to command line calls which prints the current version number",
    "Added '--version_changes'/'-version_changes' argument to command line calls which prints the changes from the previous to current version",
]

feature_changes = [
    "COBY no longer reads '#ifdef' and '#ifndef' statements but simply skips over them as they were not used anyways.",
    [
        "Prevents crashes caused by attempts to read files from '#include' statements placed within '#ifdef'/'#ifndef' if those files were not actually there.",
        "Done by simply commenting out various code related to it and skipping lines inside '#ifdef'/'#ifndef' statements. Will consider for the future if it should be completely removed or reimplemented.",
    ],
]

bug_fixes = [
    "Forgot to write in v0.1.4 changelog:",
    [
        "Fixed a bug with designating charges for molecules with only a single bead.",
    ],
]

minor_changes = [
    "Added code explanation for 'moleculetype_class'",
]

tutorial_changes = [
]

def version_change_writer(iterable, recursion_depth = 0):
    list_of_strings = []
    for i in iterable:
        if type(i) == str:
            list_of_strings.append("    " * recursion_depth + i)
        elif type(i) in [list, tuple]:
            list_of_strings.extend(version_change_writer(i, recursion_depth + 1))
    return list_of_strings

### Extra empty "" is to add a blank line between sections
all_changes = []
if len(new_features) > 0:
    all_changes += ["New:", new_features, ""]

if len(feature_changes) > 0:
    all_changes += ["Changes:", feature_changes, ""]

if len(bug_fixes) > 0:
    all_changes += ["Bug fixing:", bug_fixes, ""]

if len(minor_changes) > 0:
    all_changes += ["Minor changes:", minor_changes, ""]

if len(tutorial_changes) > 0:
    all_changes += ["Tutorial changes:", tutorial_changes]

version_changes_list = version_change_writer(all_changes)
version_changes_str = "\n".join(version_changes_list)

def version_changes():
    print(version_changes_str)

