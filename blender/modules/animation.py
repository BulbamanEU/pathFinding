import bpy
import math

start_frame = 1
end_frame = 100

def no_rotation(n, max_speed=5):
    agent_name = f'Agent{n}'
    path_name = f'Path{n}'

    agent_obj = bpy.data.objects.get(agent_name)
    path_obj = bpy.data.objects.get(path_name)

    if agent_obj and path_obj and path_obj.type == 'CURVE':

        # Calculate the total length of the path
        path_length = path_obj.data.splines[0].calc_length()

        # Calculate the time (in frames) required to traverse the path at max speed
        frame_duration = (path_length / max_speed) * bpy.context.scene.render.fps

        follow_path_constraint = agent_obj.constraints.new(type='FOLLOW_PATH')
        follow_path_constraint.target = path_obj

        follow_path_constraint.use_curve_follow = False
        follow_path_constraint.use_fixed_location = True
        follow_path_constraint.offset_factor = 0.0

        agent_obj.rotation_mode = 'XYZ'

        path_obj.data.use_path = True
        path_obj.data.path_duration = int(frame_duration)  # Convert to integer

        # Insert keyframes for movement along the path
        follow_path_constraint.offset_factor = 0.0
        agent_obj.keyframe_insert(data_path="constraints[\"Follow Path\"].offset_factor", frame=start_frame)

        follow_path_constraint.offset_factor = 1.0
        agent_obj.keyframe_insert(data_path="constraints[\"Follow Path\"].offset_factor", frame=start_frame + int(frame_duration))

    else:
        print(f"Agent or Path not found for index {n}: {agent_name}, {path_name}")

