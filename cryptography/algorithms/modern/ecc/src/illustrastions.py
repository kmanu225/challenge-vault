import matplotlib.pyplot as plt
import numpy as np
from random import randint


class CartesianPlan:
    x_plots = 0
    y_plots = 0
    axes = None
    fig = None
    x = None
    y = None

    def __init__(self, n_plots: tuple, title: str):
        self.n_plots = n_plots
        self.title = title

    def init_plot(self):
        fig, axes = plt.subplots(self.n_plots[0], self.n_plots[1])

        # Move left y-axis and bottom x-axis to centre, passing through (0,0)
        for i in range(self.n_plots[0]):
            for j in range(self.n_plots[1]):
                ax = axes[i, j]
                ax.spines["left"].set_position("center")
                ax.spines["bottom"].set_position("center")

                # Eliminate upper and right axes
                ax.spines["right"].set_color("none")
                ax.spines["top"].set_color("none")

                # Show ticks in the left and lower axes only
                ax.xaxis.set_ticks_position("bottom")
                ax.yaxis.set_ticks_position("left")

                # Equalize x and y axes scales
                ax.set_aspect("equal", adjustable="box")

        self.fig = fig
        self.axes = axes

    def increment_plots(self):
        if self.y_plots < self.n_plots[1] - 1:
            self.y_plots += 1
        else:
            self.y_plots = 0
            self.x_plots += 1

    def curve2(self, window, function, parameters, title=None):
        ax = self.axes[self.x_plots, self.y_plots]
        precision = 1000j
        y, x = np.ogrid[-window:window:precision, -window:window:precision]
        ax.contour(x.ravel(), y.ravel(), function(x, y, parameters), [0])
        ax.grid(True)
        if title is not None:
            ax.set_title(title)
        self.increment_plots()

    def curve(self, x, y, delimiter=None, title=None):
        self.x = x
        self.y = y
        ax = self.axes[self.x_plots, self.y_plots]

        if delimiter is not None:
            ax.plot(x, y, delimiter)
        else:
            ax.plot(x, y)
        ax.grid(True)
        if title is not None:
            ax.set_title(title)
        self.increment_plots()

    def show(self):
        self.fig.suptitle(self.title)
        plt.show()


def examples_smooth_curves(title="Smooth curves"):

    plan = CartesianPlan((2, 3), title)
    plan.init_plot()

    # **Ellipse**
    ellipse = lambda a, b, t: (a * np.cos(t), b * np.sin(t))
    a, b, t = 2, 2, np.linspace(0, 2 * np.pi, 100)
    x, y = ellipse(a, b, t)
    plan.curve(
        x,
        y,
        title=rf"$\left(\frac{{X}}{{{a}}}\right)^2 + \left(\frac{{Y}}{{{b}}}\right)^2 = 1$",
    )

    a, b = 3, 2
    x, y = ellipse(a, b, t)
    plan.curve(
        x,
        y,
        title=rf"$\left(\frac{{X}}{{{a}}}\right)^2 + \left(\frac{{Y}}{{{b}}}\right)^2 = 1$",
    )

    # **Cosine Function**
    cosinus = lambda t: (t, np.cos(t))
    t = np.linspace(-np.pi, np.pi, 100)
    x, y = cosinus(t)
    plan.curve(x, y, title=rf"$Y = \cos(X)$")

    # **Parabola**: Standard form \( Y = aX^2 + bX + c \)
    parabola = lambda a, b, c, x: (x, a * x**2 + b * x + c)
    a, b, c = 1, 0, 0
    x = np.linspace(-2, 2, 100)
    x, y = parabola(a, b, c, x)
    plan.curve(x, y, title=rf"$Y = {a}X^2 + {b}X + {c}$")

    # **Hyperbola**: Standard form \( \frac{X^2}{a^2} - \frac{Y^2}{b^2} = 1 \)
    hyperbola = lambda a, b, t: (a * np.cosh(t), b * np.sinh(t))
    a, b, t = 2, 1, np.linspace(-2, 2, 100)
    x1, y1 = hyperbola(a, b, t)
    x2, y2 = -x1, y1  # Second branch of hyperbola
    x = np.concatenate([x1, x2])
    y = np.concatenate([y1, y2])
    plan.curve(
        x,
        y,
        delimiter=".",
        title=rf"$\left(\frac{{X}}{{{a}}}\right)^2 - \left(\frac{{Y}}{{{b}}}\right)^2 = 1$",
    )

    # **Elliptic Curve**: \( Y^2 = X^3 + aX + b \)
    curve = lambda a, b, x: np.sqrt(x**3 + a * x + b)
    a, b = -1, 1  # Example parameters
    x_np = np.linspace(-2, 2, 300)
    x = []
    y_pos = []
    y_neg = []
    for x_i in x_np:
        if x_i**3 + a * x_i + b >= 0:
            x.append(x_i)
            y_i = curve(a, b, x_i)
            y_pos.append(y_i)
            y_neg.append(-y_i)

    x = np.concatenate([x[::-1], x])
    y = np.concatenate([y_pos[::-1], y_neg])

    plan.curve(x, y, title=rf"$Y^2 = X^3 + {a}X + {b}$")

    plan.show()


def examples_weirstrass(title="Weirstrass form"):

    plan = CartesianPlan((2, 3), title)
    plan.init_plot()

    # **Elliptic Curve**: \( Y^2 = X^3 + aX + b \)
    weierstrass = lambda x, y, parameters: (
        y**2 + parameters[0] * x * y + parameters[1] * y
    ) - (x**3 + parameters[2] * x**2 + parameters[3] * x + parameters[4])

    ec_sigular = lambda x, y, parameters: x**3 + parameters[0] * x**2 - y**2

    window = 2
    parameters = [
        [0, 0, 0, -1, 0],
        [0, 0, 0, -1, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, -1, -1],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
    ]
    for param in parameters:

        plan.curve2(
            window,
            weierstrass,
            param,
            title=rf"$Y^2 + {param[0]}xy + {param[1]}y = X^3 + {param[2]}X^2 + {param[3]}X+ {param[4]}$",
        )

    # plan.curve2(window, ec_sigular, [1], title=rf"$Y^2 = X^3 + X^2$")
    plan.show()


def examples_edward(title="Edward form"):

    plan = CartesianPlan((2, 5), title)
    plan.init_plot()

    # **Edward Curve**: \( Y^2 + X^2 = 1 + dX^2Y^2 \)
    edward = lambda x, y, parameters: y**2 + x**2 - (1 + parameters[0] * (x * y) ** 2)
    window = 2
    parameters = [
        [-2000],
        [-20],
        [-2],
        [0],
        [7 / 10],
        [8 / 10],
        [9 / 10],
        [1],
        [20],
        [200],
    ]
    for param in parameters:

        plan.curve2(
            window,
            edward,
            param,
            title=rf"$Y^2 + X^2 = 1 + {param[0]}X^2Y^2$",
        )

    # plan.curve2(window, ec_sigular, [1], title=rf"$Y^2 = X^3 + X^2$")
    plan.show()


def examples_montgomery(title="Montgomery form"):

    plan = CartesianPlan((2, 3), title)
    plan.init_plot()

    # **Elliptic Curve**: \( Y^2 = X^3 + aX + b \)
    weierstrass = lambda x, y, parameters: parameters[1] * y**2 - (
        x**3 + parameters[0] * x**2 + x
    )

    window = 5
    parameters = [
        [-1, 1],
        [3, 1],
        [-2, 1],
        [1, -1],
        [-3, -1],
        [3, 0],
    ]
    for param in parameters:

        plan.curve2(
            window,
            weierstrass,
            param,
            title=rf"${param[1]}Y^2 = X^3 + {param[0]}X^2 + X$",
        )

    # plan.curve2(window, ec_sigular, [1], title=rf"$Y^2 = X^3 + X^2$")
    plan.show()


if __name__ == "__main__":
    # examples_smooth_curves()
    # examples_weirstrass()
    # examples_edward()
    examples_montgomery()
