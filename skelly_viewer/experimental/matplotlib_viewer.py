from typing import Union

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from skelly_viewer.experimental.plotly.data_loader import DataLoader

class AnimationCreator:
    def __init__(self, data_by_frame):
        self.data_by_frame = data_by_frame["data_by_frame"]
        self.info = data_by_frame["info"]

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        self.ax.set_xlim([-2000, 2000])
        self.ax.set_ylim([-2000, 2000])
        self.ax.set_zlim([-2000, 2000])

        self.anim = animation.FuncAnimation(self.fig, self.animate, frames=len(self.data_by_frame), interval=1000 / 30,
                                            blit=False)

    def animate(self, frame_number: Union[str, int]):
        self.ax.clear()
        self.ax.set_xlim([-3000, 3000])
        self.ax.set_ylim([-3000, 3000])
        self.ax.set_zlim([-3000, 3000])

        body = self.data_by_frame[str(frame_number)]["body"]
        connections = self.info["names_and_connections"]["body"]["connections"]
        body_names = list(body.keys())

        for connection in connections:
            x_values = [body[body_names[connection[0]]]['x'], body[body_names[connection[1]]]['x']]
            y_values = [body[body_names[connection[0]]]['y'], body[body_names[connection[1]]]['y']]
            z_values = [body[body_names[connection[0]]]['z'], body[body_names[connection[1]]]['z']]

            self.ax.plot(x_values, y_values, z_values, 'purple')

        self.ax.scatter(
            np.array([point["x"] for point in body.values()]),
            np.array([point["y"] for point in body.values()]),
            np.array([point["z"] for point in body.values()]),
            c='purple',
        )

    def show(self):
        plt.show()


if __name__ == "__main__":
    SAMPLE_DATA_PATH = r"C:\Users\jonma\freemocap_data\recording_sessions\freemocap_sample_data"
    data_loader = DataLoader(SAMPLE_DATA_PATH)
    data_by_frame = data_loader.load_data_by_frame()

    anim_creator = AnimationCreator(data_by_frame)
    anim_creator.show()
