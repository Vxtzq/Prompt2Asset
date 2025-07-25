python3 download_model.py
mkdir sprite
mkdir sprite_output
mkdir mesh_output

python3 character_gen.py
python3 IS-Net/Inference.py
python3 inference.py
cd UniRig
bash launch/inference/generate_skeleton.sh --input ../mesh_output/mesh.glb --output ../results/rigged_mesh.fbx 
bash launch/inference/generate_skin.sh --input ../results/rigged_mesh.fbx --output ../results/rigged_mesh.fbx

bash launch/inference/merge.sh --source ../results/rigged_mesh.fbx --target ../mesh_output/mesh.glb --output ../results/mesh_final.glb

rm -r mesh_output
rm -r tmp
cd ..
