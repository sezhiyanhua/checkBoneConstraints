# checkBoneConstraints

checkBoneConstraints is a Blender Python script that finds and selects bones with constraints.

In Object Mode, the script checks every bone in the selected armatures. In Pose Mode, it checks only the currently selected pose bones. Matching bones are selected and their constraint types are written to Blender's console.

## Compatibility

Designed for Blender 5.2.

## Requirements

- Blender with Python scripting support
- One or more armature objects

## Usage

1. Download `check_bone_constraints.py`.
2. Open Blender and switch to the **Scripting** workspace.
3. Open `check_bone_constraints.py` in the Text Editor.
4. In Object Mode, select one or more armature objects to check all their bones.
5. Alternatively, in Pose Mode, select the pose bones you want to check.
6. Click **Run Script**.

Bones with constraints are selected automatically. The result popup reports how many bones were checked and how many matches were found.

## Notes

- Set `DEFORM_ONLY = True` near the top of the script to check deform bones only.
- In Object Mode, the active armature is processed first and Blender switches to Pose Mode after the check.
- In Pose Mode, only the selected pose bones are checked.
- Constraint types for matching bones are written to Blender's console.
- Save a backup of important `.blend` files before running scripts that modify a selection or mode.

## Author

SZ

- [GitHub](https://github.com/sezhiyanhua)
- [Bilibili](https://space.bilibili.com/12379590)

## License

Released under the [MIT License](LICENSE).
