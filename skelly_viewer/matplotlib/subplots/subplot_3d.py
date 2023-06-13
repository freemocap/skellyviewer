from typing import Union

import numpy as np

from skelly_viewer.matplotlib.subplots.base_subplot import BasePlot, PLOT_COLOR, MARKER_SIZE


class Subplot3d(BasePlot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.axis = self.figure.add_subplot(self.grid_spec[0, 0], projection='3d')
        self.set_axis_limits()

    def clear(self):
        self.axis.clear()

    def set_axis_limits(self):
        self.axis.set_xlim(self.axis_limits["x"])
        self.axis.set_ylim(self.axis_limits["y"])
        self.axis.set_zlim(self.axis_limits["z"])

    def draw_body_parts_connection(self, body_parts: dict, body_parts_names: list, connection: tuple):
        x_values = [body_parts[body_parts_names[connection[0]]]['x'], body_parts[body_parts_names[connection[1]]]['x']]
        y_values = [body_parts[body_parts_names[connection[0]]]['y'], body_parts[body_parts_names[connection[1]]]['y']]
        z_values = [body_parts[body_parts_names[connection[0]]]['z'], body_parts[body_parts_names[connection[1]]]['z']]
        self.axis.plot(x_values, y_values, z_values, PLOT_COLOR)

    def scatter_body_parts(self, body_parts: dict):
        self.axis.scatter(
            np.array([point["x"] for point in body_parts.values()]),
            np.array([point["y"] for point in body_parts.values()]),
            np.array([point["z"] for point in body_parts.values()]),
            c=PLOT_COLOR,
            s=MARKER_SIZE,
        )

    def animate(self, frame_number: Union[str, int]):
        self.clear()
        self.set_axis_limits()
        body_parts = self.data_by_frame[str(frame_number)]["body"]
        connections = self.info["names_and_connections"]["body"]["connections"]
        body_parts_names = list(body_parts.keys())
        for connection in connections:
            self.draw_body_parts_connection(body_parts, body_parts_names, connection)
        self.scatter_body_parts(body_parts)