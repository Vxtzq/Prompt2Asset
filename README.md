# Prompt2Asset
Full pipeline to generate a fully functionnal asset from a single prompt

# Installation

To keep existing version : 

``pip install --no-deps --no-index --find-links=. --no-warn-script-location --no-cache-dir --ignore-installed -r requirements.txt``

or 

``pip install -r requirements.txt``

# Usage

For riggable character :

``./generate_character.sh --prompt "prompt" --negative_prompt "negative prompt" --rig --use_pose --pose_image "character_pose.png"``


For generic riggable object :

``./generate_character.sh --prompt "prompt" --negative_prompt "negative prompt" --rig``

For background asset :

``./generate_character.sh "prompt"``



