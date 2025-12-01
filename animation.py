import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

VALID_CENTERS = ["sun", "earth", "asteroid"]

class Animation(object):
    
    def __init__(self, bodies):
        self.data_set = np.array(bodies, dtype=object)
        self.set_size = len(bodies)
    
    def update(self, frame):
        xs, ys = self.get_centered_positions(frame, self.center_name)
        bodies = self.data_set[frame]

        self.scat.set_offsets(np.column_stack((xs, ys)))

        for label, x, y, body in zip(self.labels, xs, ys, bodies):
            label.set_position((x, y))
            label.set_text(body.label)

        return (self.scat, *self.labels)

    def get_centered_positions(self, frame, center_name):
        bodies = self.data_set[frame]

        center_body = None
        for b in bodies:
            if b.label.lower() == center_name.lower():
                center_body = b
                break

        if center_body is None:
            raise ValueError(f"Body '{center_name}' not found in frame {frame}.")

        cx, cy = center_body.position

        xs = [b.position[0] - cx for b in bodies]
        ys = [b.position[1] - cy for b in bodies]

        return xs, ys

    def create_plot(self):
        all_centered = []
        for f in range(self.set_size):
            xs, ys = self.get_centered_positions(f, self.center_name)
            all_centered.append((xs, ys))

        xs = np.array([x for frame in all_centered for x in frame[0]])
        ys = np.array([y for frame in all_centered for y in frame[1]])

        max_abs_x = max(abs(xs.min()), abs(xs.max()))
        max_abs_y = max(abs(ys.min()), abs(ys.max()))
        half_range = max(max_abs_x, max_abs_y)

        pad = half_range * 0.2 if half_range != 0 else 1.0
        lim = half_range + pad
        xlim = (-lim, lim)
        ylim = (-lim, lim)

        fig, ax = plt.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)

        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.set_aspect('equal', adjustable='box')
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)

        self.scat = ax.scatter([], [])
        self.ax = ax

        self.labels = [
            ax.text(0, 0, "", fontsize=9, ha='left', va='bottom')
            for _ in range(len(self.data_set[0]))
        ]

        ani = animation.FuncAnimation(
            fig,
            self.update,
            frames=self.set_size,
            interval=300,
            repeat=True,
            blit=True
        )

        return ani

    def animate(self, center="sun", save=False, filename='animation.gif'):
        if center not in VALID_CENTERS:
            print("Invalid center declaration in animate function call.")
            print("Valid declarations: \"sun\", \"earth\", \"asteroid\".")
            return

        self.center_name = center
        ani = self.create_plot()

        if save:
            print(f"Saving animation to {filename}...")
            ani.save(
                filename,
                fps=15,
                dpi=150,
                writer="ffmpeg" if filename.endswith(".mp4") else "pillow"
            )
            print("Saved!")

        else:
            plt.show()