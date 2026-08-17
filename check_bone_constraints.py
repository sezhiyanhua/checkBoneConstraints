"""Bone Constraint Check for Blender 5.2.

Author: SZ
Bilibili: https://space.bilibili.com/12379590
"""

import bpy


DEFORM_ONLY = False


def show_message(message, title="Bone Constraint Check", icon="INFO"):
    print(f"[{title}] {message}")

    def draw(self, _context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def selected_armatures(context):
    armatures = [obj for obj in context.selected_objects if obj.type == "ARMATURE"]
    active_object = context.view_layer.objects.active

    if active_object in armatures:
        armatures.remove(active_object)
        armatures.insert(0, active_object)

    return armatures


def filter_selection(armature_object, candidates):
    candidate_names = {pose_bone.name for pose_bone in candidates}
    matches = []

    for pose_bone in armature_object.pose.bones:
        bone = pose_bone.bone
        has_constraint = len(pose_bone.constraints) > 0
        is_deform_bone = not DEFORM_ONLY or bone.use_deform
        should_select = (
            pose_bone.name in candidate_names
            and has_constraint
            and is_deform_bone
        )

        pose_bone.select = should_select

        if should_select:
            matches.append(pose_bone)

    armature_object.data.bones.active = matches[0].bone if matches else None
    return matches


def main():
    context = bpy.context
    started_in_pose_mode = context.mode == "POSE"

    if started_in_pose_mode:
        armature_objects = [context.object]
        candidates_by_object = {
            context.object.name: [
                pose_bone
                for pose_bone in context.object.pose.bones
                if pose_bone.select
            ]
        }

        if not candidates_by_object[context.object.name]:
            show_message("Select at least one pose bone first", icon="ERROR")
            return

    elif context.mode == "OBJECT":
        armature_objects = selected_armatures(context)

        if not armature_objects:
            show_message("Select at least one armature object first", icon="ERROR")
            return

        candidates_by_object = {
            obj.name: list(obj.pose.bones)
            for obj in armature_objects
        }

    else:
        show_message("Run this script in Pose Mode or Object Mode", icon="ERROR")
        return

    matches_by_object = {}
    checked_count = 0

    for obj in armature_objects:
        candidates = candidates_by_object[obj.name]
        checked_count += sum(
            1
            for pose_bone in candidates
            if not DEFORM_ONLY or pose_bone.bone.use_deform
        )
        matches_by_object[obj.name] = filter_selection(obj, candidates)

    if not started_in_pose_mode:
        active_armature = armature_objects[0]
        context.view_layer.objects.active = active_armature
        active_armature.select_set(True)

        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode="POSE")

    match_count = sum(len(matches) for matches in matches_by_object.values())

    for object_name, matches in matches_by_object.items():
        for pose_bone in matches:
            constraint_types = ", ".join(
                constraint.type for constraint in pose_bone.constraints
            )
            print(
                f"[Bone Constraint Check] {object_name} / "
                f"{pose_bone.name}: {constraint_types}"
            )

    if match_count:
        show_message(
            f"Checked {checked_count} bones; found {match_count} with constraints",
            icon="ERROR",
        )
    else:
        show_message(f"Checked {checked_count} bones; no constraints found")


if __name__ == "__main__":
    main()
