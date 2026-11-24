from PIL import Image
from pathlib import Path
from boids import run_number

# creating directories

run_dir = Path(f'./results/run_{run_number:03d}')
figures_dir = Path(f'./results/run_{run_number:03d}/figures')


# pouring all images into a list 

frames = []
image = Path(figures_dir / 'figure_000.png')
counter = 0

while image.exists():
    img = Image.open(image)
    frames.append(img)
    image = Path(figures_dir / f"figure_{counter+1:03d}.png")
    counter += 1


# making gif

frames[0].save(
   run_dir / "animation.gif",
    save_all=True,
    append_images=frames[1:],
    duration = 80,
    loop=0
)
