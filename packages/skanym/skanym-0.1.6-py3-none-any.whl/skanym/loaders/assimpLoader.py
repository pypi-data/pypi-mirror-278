import sys
import warnings
from typing import List, Tuple
from pathlib import Path

import numpy as np
import quaternion
import pyassimp
from pyassimp.structs import Node
from pyassimp.postprocess import aiProcess_Triangulate, aiProcess_MakeLeftHanded
from line_profiler import profile

from skanym.loaders.iFileLoader import IFileLoader
from skanym.loaders.objectLoader import ObjectLoader
from skanym.structures.character.skeleton import Skeleton
from skanym.structures.character.joint import Joint
from skanym.structures.animation.animation import Animation
from skanym.structures.animation.animationCurve import AnimationCurve
from skanym.structures.animation.positionCurve import PositionCurve
from skanym.structures.animation.quaternionCurve import QuaternionCurve
from skanym.structures.animation.key import Key
from skanym.structures.data.transform import Transform
from skanym.utils import conversion


class AssimpLoader(IFileLoader):
    def __init__(self, path: Path):
        super().__init__(path)
        self.joints = None

    @profile
    def load_skeleton(self) -> Skeleton:
        # remove the .fbx extension
        # append "_skeleton.pkl" to the path
        obj_path = self._path.parent / "pkl" / (self._path.stem + "_skeleton.pkl")
        # check if the file exists
        # print(obj_path)
        if Path(obj_path).exists():
            # if it does, load the object from the file
            loader = ObjectLoader(Path(obj_path))
            return loader.load()
        
        # if the file does not exist, load the skeleton from the fbx file       
        with pyassimp.load(
            str(self._path),
            processing=(pyassimp.postprocess.aiProcess_Triangulate),
        ) as scene:
            if scene is None:
                raise Exception(f"Failed to load file: {self._path}")

            allNodeList = self._all_nodes_dfs(scene.rootnode)

            joints = self._create_joint_list(allNodeList)
            self.joints = joints

            jointNodeList = self._joint_nodes_dfs(scene.rootnode)

            skeleton = self._build_skeleton(joints, jointNodeList)

            # save the skeleton to a file
            loader = ObjectLoader(Path(obj_path))
            loader.save(skeleton)

            return skeleton

    @profile
    def load_animation(self) -> Animation:
        # remove the .fbx extension
        # append "_animation.pkl" to the path
        obj_path = self._path.parent / "pkl" / (self._path.stem + "_animation.pkl")
        # check if the file exists
        if Path(obj_path).exists():
            # if it does, load the object from the file
            loader = ObjectLoader(Path(obj_path))
            return loader.load()
            
        # print(f"Loading animation from {self._path}")
        # if the file does not exist, load the skeleton from the fbx file   
        with pyassimp.load(
            str(self._path),
            processing=(pyassimp.postprocess.aiProcess_Triangulate),
        ) as scene:
            if scene is None:
                raise Exception(f"Failed to load file: {self._path}")

            raw_duration = scene.animations[0].duration
            duration = raw_duration / scene.animations[0].tickspersecond
            animation = Animation(name=scene.animations[0].name, duration=duration)
            
            if self.joints is None:
                allNodeList = self._all_nodes_dfs(scene.rootnode)
                joints = self._create_joint_list(allNodeList)
            else:
                joints = self.joints

            animChannels = scene.animations[0].channels
            for channel in animChannels:
                failed_once = False
                for encoding in ["ascii", "utf-8"]:
                    try:
                        raw_name = channel.nodename.data
                        name = raw_name.decode(encoding)
                        if failed_once:
                            print(f"Decoded to {name} with encoding {encoding}")
                            failed_once = False
                        break
                    except Exception as e:
                        print(f"Failed to decode nodename {raw_name} with encoding {encoding}") 
                        failed_once = True

                joint_id = self._get_joint_id(name, joints)
                current_pos_curve = PositionCurve()
                current_rot_curve = QuaternionCurve()
                if joint_id == 0:
                    for pos_key in channel.positionkeys:
                        current_pos_curve.add_key(
                            Key(
                                time=pos_key.time / raw_duration,
                                value=np.array(
                                    [
                                        pos_key.value[0],
                                        pos_key.value[1],
                                        pos_key.value[2],
                                    ]
                                ),
                            )
                        )

                    animation.position_curves.append(
                        AnimationCurve(curve=current_pos_curve, id=joint_id)
                    )

                for rot_key in channel.rotationkeys:
                    q = np.quaternion(
                        rot_key.value[0],
                        rot_key.value[1],
                        rot_key.value[2],
                        rot_key.value[3],
                    )
                    bind_m = joints[joint_id].local_bind_transform.getTransformMatrix()     
                    m_rot = conversion.quaternionToRotationMatrix(q)
                    m = np.identity(4)
                    m[0:3, 0:3] = m_rot
                    delta_m = np.matmul(np.linalg.inv(bind_m), m)
                    delta_q = conversion.rotationMatrixToQuaternion(delta_m[0:3, 0:3])[0]

                    # if delta_q.w < 0:
                    #     delta_q = -delta_q
                    
                    current_rot_curve.add_key(
                        Key(
                            time=rot_key.time / raw_duration,
                            value=quaternion.as_float_array(delta_q),
                        )
                    )

                animation.rotation_curves.append(
                    AnimationCurve(curve=current_rot_curve, id=joint_id)
                )

            for joint_id in range(len(joints)):
                if joint_id not in [
                    anim_curve.id for anim_curve in animation.position_curves
                ]:
                    animation.position_curves.append(
                        AnimationCurve(curve=PositionCurve(), id=joint_id)
                    )
                if joint_id not in [
                    anim_curve.id for anim_curve in animation.rotation_curves
                ]:
                    animation.rotation_curves.append(
                        AnimationCurve(curve=QuaternionCurve(), id=joint_id)
                    )

            animation.position_curves.sort(key=lambda x: x.id)
            animation.rotation_curves.sort(key=lambda x: x.id)

            # save the animation to a file
            loader = ObjectLoader(Path(obj_path))
            loader.save(animation)

            return animation

    def set_path(self, path: Path):
        super().set_path(path)
        self.joints = None

    def _get_joint(self, name: str, joints: List[Joint]) -> Joint:
        for joint in joints:
            if joint.name == name:
                return joint
        return None

    def _get_joint_id(self, name: str, joints: List[Joint]) -> int:
        for i, joint in enumerate(joints):
            if joint.name == name:
                return i
        return -1

    def _is_joint_node(self, node: Node) -> bool:
        return not ("Translation" in node.name or "Rotation" in node.name)

    def _all_nodes_dfs(self, node: Node, allNodeList: List[Node] = None) -> List[Node]:
        if allNodeList is None:
            allNodeList = []
        for child in node.children:
            allNodeList.append(child)
            self._all_nodes_dfs(child, allNodeList)
        return allNodeList

    def _joint_nodes_dfs(
        self, node: Node, depth: int = 0, jointNodeList: List[Tuple[str, int]] = None
    ) -> List[Tuple[str, int]]:
        if jointNodeList is None:
            jointNodeList = []
        for child in node.children:
            if self._is_joint_node(child):
                jointNodeList.append((child.name, depth))
                depth += 1
            self._joint_nodes_dfs(child, depth, jointNodeList)
        return jointNodeList

    def _create_joint_list(self, allNodeList: List[Node]) -> List[Joint]:
        joints = []
        current_joint = None
        for node in allNodeList[::-1]:
            if not self._is_joint_node(node):
                if "Translation" in node.name:
                    current_joint.local_bind_transform.position = np.array(
                        [
                            node.transformation[0][3],
                            node.transformation[1][3],
                            node.transformation[2][3],
                        ]
                    )
                elif "Rotation" in node.name:
                    rm = (
                        np.array(
                            [
                                node.transformation[0][0],
                                node.transformation[1][0],
                                node.transformation[2][0],
                                node.transformation[0][1],
                                node.transformation[1][1],
                                node.transformation[2][1],
                                node.transformation[0][2],
                                node.transformation[1][2],
                                node.transformation[2][2],
                            ]
                        )
                        .reshape(3, 3)
                        .T
                    )
                    q = conversion.rotationMatrixToQuaternion(rm)[0]
                    current_joint.local_bind_transform.rotation = q

            else:
                current_pos = np.array(
                    [
                        node.transformation[0][3],
                        node.transformation[1][3],
                        node.transformation[2][3],
                    ]
                )
                current_rot = (
                    np.array(
                        [
                            node.transformation[0][0],
                            node.transformation[1][0],
                            node.transformation[2][0],
                            node.transformation[0][1],
                            node.transformation[1][1],
                            node.transformation[2][1],
                            node.transformation[0][2],
                            node.transformation[1][2],
                            node.transformation[2][2],
                        ]
                    )
                    .reshape(3, 3)
                    .T
                )
                q = conversion.rotationMatrixToQuaternion(current_rot)[0]
                # q.z = -q.z
                current_rotation = q

                current_joint = Joint(
                    node.name,
                    local_bind_transform=Transform(
                        position=current_pos, rotation=current_rotation
                    ),
                )
                joints.append(current_joint)

        joints.reverse()
        joints[0].local_bind_transform = Transform()
        return joints

    def _build_skeleton(self, joints, jointNodeList: List[Tuple[str, int]]) -> Skeleton:
        root = None
        parent_stack = []

        for name, depth in jointNodeList:
            current_joint = self._get_joint(name, joints)

            if depth == 0:
                root = current_joint
                parent_stack = [root]
            else:
                while len(parent_stack) > depth:
                    parent_stack.pop()
                parent_stack[-1].add_child(current_joint)
                parent_stack.append(current_joint)

        return Skeleton(root)

    def load_animations(self) -> List[Animation]:
        return NotImplementedError


if __name__ == "__main__":
    np.set_printoptions(precision=6, suppress=True)    
    np.set_printoptions(formatter={'float': lambda x: "{: 0.6f}".format(x)})
    
    directory = "C:/dev/GIM3D/mixamo_animations/db-test-animations/animations"
    for file in list(Path(directory).rglob("*.fbx"))[0:2]:
        file_path = file        
        loaderito = AssimpLoader(file_path)
        s = loaderito.load_skeleton()
        a = loaderito.load_animation()
        print("loaded", file_path)    
    print("Success")
    # for anim_curve in a.rotation_curves:
    #     print(s.get_joint_by_id(anim_curve.id).name)   
    #     for key in anim_curve.curve.keys[0:3]:
    #         # if a value is close to 0, set it to 0
    #         key.value = np.where(np.abs(key.value) < 1e-3, 0, key.value)
    #         print(key.value)
