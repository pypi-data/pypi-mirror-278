##########################################################################
## FESSA COLOR PALETTE
##########################################################################
#  https://github.com/luigibonati/fessa-color-palette/blob/master/fessa.py

import mlcolvar
from matplotlib.colors import LinearSegmentedColormap, ColorConverter
from matplotlib import patches as mpatches
import matplotlib as mpl

__all__ = ["paletteFessa", "paletteCortina"]

# Fessa colormap
paletteFessa = [
    "#1F3B73",  # dark-blue
    "#2F9294",  # green-blue
    "#50B28D",  # green
    "#A7D655",  # pisello
    "#FFE03E",  # yellow
    "#FFA955",  # orange
    "#D6573B",  # red
]

cm_fessa = LinearSegmentedColormap.from_list("fessa", paletteFessa)
mpl.colormaps.register(cmap=cm_fessa)
mpl.colormaps.register(cmap=cm_fessa.reversed())

for i in range(len(paletteFessa)):
    ColorConverter.colors[f"fessa{i}"] = paletteFessa[i]

### To set it as default
# import fessa
# plt.set_cmap('fessa')
### or the reversed one
# plt.set_cmap('fessa_r')
### For contour plots
# plt.contourf(X, Y, Z, cmap='fessa')
### For standard plots
# plt.plot(x, y, color='fessa0')


# Cortina1980 colormap
paletteCortina = [
    [0.0, 0.0, 0.803921568627451, 1],  # mediumblue
    [0.4823529411764706, 0.40784313725490196, 0.9333333333333333, 1],  # mediumslateblue
    [0.0, 0.9803921568627451, 0.6039215686274509, 1],  # mediumspringgreen
    [0.23529411764705882, 0.7019607843137254, 0.44313725490196076, 1],  # mediumseagreen
    [0.8588235294117647, 0.4392156862745098, 0.5764705882352941, 1],  # palevioletred
    [0.7803921568627451, 0.08235294117647059, 0.5215686274509804, 1],  # mediumvioletred
]

cm_cortina = LinearSegmentedColormap.from_list("cortina80", paletteCortina)
mpl.colormaps.register(cmap=cm_cortina)
mpl.colormaps.register(cmap=cm_cortina.reversed())

##########################################################################
## HELPER FUNCTIONS FOR 2D SYSTEMS
##########################################################################

import matplotlib.pyplot as plt
import numpy as np
import torch


def muller_brown_potential(x, y):
    """Muller-Brown analytical potential"""
    prefactor = 0.15
    A = (-200, -100, -170, 15)
    a = (-1, -1, -6.5, 0.7)
    b = (0, 0, 11, 0.6)
    c = (-10, -10, -6.5, 0.7)
    x0 = (1, 0, -0.5, -1)
    y0 = (0, 0.5, 1.5, 1)
    offset = -146.7

    v = -prefactor * offset
    for i in range(4):
        v += (
            prefactor
            * A[i]
            * np.exp(
                a[i] * (x - x0[i]) ** 2
                + b[i] * (x - x0[i]) * (y - y0[i])
                + c[i] * (y - y0[i]) ** 2
            )
        )
    return v


def muller_brown_mfep():
    mfep = np.loadtxt(
        mlcolvar.__path__[0]
        + "/../docs/notebooks/tutorials/data/muller-brown/mfep.txt",
        usecols=(0, 1),
    )
    return mfep


def muller_brown_potential_three_states(x, y):
    """Muller-Brown analytical potential"""
    prefactor = 0.15
    A = (-280, -170, -170, 15)
    a = (-15, -1, -6.5, 0.7)
    b = (0, 0, 11, 0.6)
    c = (-10, -10, -6.5, 0.7)
    x0 = (1, 0.2, -0.5, -1)
    y0 = (0, 0.5, 1.5, 1)
    offset = -146.7

    v = -prefactor * offset
    for i in range(4):
        v += (
            prefactor
            * A[i]
            * np.exp(
                a[i] * (x - x0[i]) ** 2
                + b[i] * (x - x0[i]) * (y - y0[i])
                + c[i] * (y - y0[i]) ** 2
            )
        )
    return v


def muller_brown_three_states_mfep():
    mfep = np.loadtxt(
        mlcolvar.__path__[0]
        + "/../docs/notebooks/tutorials/data/muller-brown-3states/mfep.txt",
        usecols=(0, 1),
    )
    return mfep


def plot_isolines_2D(
    function,
    component=None,
    limits=((-1.8, 1.2), (-0.4, 2.1)),
    num_points=(100, 100),
    mode="contourf",
    levels=12,
    cmap=None,
    colorbar=None,
    max_value=None,
    ax=None,
    **kwargs,
):
    """Plot isolines of a function/model in a 2D space."""

    # Define grid where to evaluate function
    if type(num_points) == int:
        num_points = (num_points, num_points)
    xx = np.linspace(limits[0][0], limits[0][1], num_points[0])
    yy = np.linspace(limits[1][0], limits[1][1], num_points[1])
    xv, yv = np.meshgrid(xx, yy)

    # if torch module
    if isinstance(function, torch.nn.Module):
        z = np.zeros_like(xv)
        for i in range(num_points[0]):
            for j in range(num_points[1]):
                xy = torch.Tensor([xv[i, j], yv[i, j]])
                with torch.no_grad():
                    train_mode = function.training
                    function.eval()
                    s = function(xy).numpy()
                    function.training = train_mode
                    if component is not None:
                        s = s[component]
                z[i, j] = s
    # else apply function directly to grid points
    else:
        z = function(xv, yv)

    if max_value is not None:
        z[z > max_value] = max_value

    # Setup plot
    return_axs = False
    if ax is None:
        return_axs = True
        _, ax = plt.subplots(figsize=(6, 4.0), dpi=100)

    # Color scheme
    if cmap is None:
        if mode == "contourf":
            cmap = "fessa"
        elif mode == "contour":
            cmap = "Greys_r"

    # Colorbar
    if colorbar is None:
        if mode == "contourf":
            colorbar = True
        elif mode == "contour":
            colorbar = False

    # Plot
    if mode == "contourf":
        pp = ax.contourf(xv, yv, z, levels=levels, cmap=cmap, **kwargs)
        if colorbar:
            plt.colorbar(pp, ax=ax)
    else:
        pp = ax.contour(xv, yv, z, levels=levels, cmap=cmap, **kwargs)

    if return_axs:
        return ax
    else:
        return None


def plot_metrics(
    metrics,
    keys=["train_loss_epoch", "valid_loss"],
    x=None,  # 'epoch'
    labels=None,  # ['Train','Valid'],
    linestyles=None,  # ['-','--']
    colors=None,  # ['fessa0','fessa1']
    xlabel="Epoch",
    ylabel="Loss",
    title="Learning curves",
    yscale=None,
    ax=None,
):
    """Plot logged metrics."""

    # Setup axis
    return_axs = False
    if ax is None:
        return_axs = True
        _, ax = plt.subplots(figsize=(5, 4), dpi=100)

    # Plot metrics
    auto_x = True if x is None else False
    for i, key in enumerate(keys):
        y = metrics[key]
        lstyle = linestyles[i] if linestyles is not None else None
        label = labels[i] if labels is not None else key
        color = colors[i] if colors is not None else None
        if auto_x:
            x = np.arange(len(y))
        ax.plot(x, y, linestyle=lstyle, label=label, color=color)

    # Plot settings
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    if yscale is not None:
        ax.set_yscale(yscale)

    ax.legend(ncol=1, frameon=False)

    if return_axs:
        return ax
    else:
        return None


def plot_sensitivity(results, mode="violin", per_class=None, max_features = 100, ax=None):
    """Plot results of the sensitivity analysis. They can be plotted in three modes:
    * Violin plot ('violin'), showing the density of per-sample sensitivities besides the mean value
    * Scatter ('scatter'), plotting the mean and standard deviation of the gradients
    * Horizontal bar plot ('barh') only displaying the mean of the gradients

    Parameters
    ----------
    results : dictionary
        sensitity results calculated by sensitivity_analysis
    mode : string, optional
        ('violin','barh','scatter'), by default 'violin'
    per_class : bool, optional
        plot per-class statistics if available, by default plot them if available
    max_features : int, optional
        plot at most max_features, by default 100
    ax : matplotlib axis, optional
        ax where to plot the results, by default it will be initialized

    See also
    --------
    mlcolvar.utils.explain.sensitivity_analysis
        Perform a sensitivity analysis

    Returns
    -------
    ax
        return the generated matplotlib axis if not passed
    """

    # retrieve info from results dictionary
    feature_names = results["feature_names"]
    n_inputs = len(feature_names)
    if max_features < n_inputs:
        print(f'Plotting only the first {max_features} features out of {n_inputs}.')
        feature_names = feature_names[-max_features:]
        n_inputs = max_features
    
    in_num = np.arange(n_inputs)
    n_results = len(results["sensitivity"].keys())

    # check whether to plot per-class statistics
    if per_class is None:
        per_class = True if n_results > 1 else False
    else:
        if not type(per_class) == bool:
            raise TypeError("per_class should be either `True`, `False` or `None`.")
        if per_class & (n_results == 1):
            raise KeyError(
                "Per class analyis requested but no labels found in the results dictionary. You need to call `sensitivity_analysis` with `per_class`=True. "
            )

    # initialize ax
    if ax is None:
        fig = plt.figure(figsize=(5, 0.25 * n_inputs))
        ax = fig.add_subplot(111)
        ax.set_title("Sensitivity Analysis")
        return_ax = True
    else:
        return_ax = False

    # define utils functions
    def _set_violin_attributes(violin_parts, color, alpha=0.5, label=None, zorder=None):
        for pc in violin_parts["bodies"]:
            pc.set_facecolor(color)
            pc.set_edgecolor(color)
            pc.set_alpha(alpha)
            if zorder is not None:
                pc.set_zorder(zorder)
        if label is not None:
            patch_label = (mpatches.Patch(color=color, alpha=alpha), label)
            return patch_label

    patch_labels = []

    patterns = ["", "", "/", "\\", "|", "-", "+", "x", "o", "O", ".", "*"]

    for i, label in enumerate(results["sensitivity"].keys()):
        score = results["sensitivity"][label][-max_features:]
        grad = results["gradients"][label][:,-max_features:]

        color = "fessa0" if "Dataset" in label else f"fessa{7-i}"

        if mode == "barh":
            alpha = 0.6 if "Dataset" in label else 0.4
            height = 0.8 if "Dataset" in label else 0.4
            ax.barh(
                in_num,
                score,
                height=height,
                color=color,
                edgecolor="k",
                hatch=patterns[i],
                alpha=alpha,
                label=label,
            )
        elif mode == "violin":
            widths = 0 if (("Dataset" in label) & per_class) else 0.5
            zorder = 1 if "Dataset" in label else 0
            showmeans = True if "Dataset" in label else False
            violin_parts = ax.violinplot(
                grad,
                positions=in_num,
                vert=False,
                showmeans=showmeans,
                showextrema=False,
                widths=widths,
            )
            patch_label = _set_violin_attributes(
                violin_parts, color, alpha=0.5, label=label, zorder=zorder
            )
            patch_labels.append(patch_label)
            if "Dataset" in label:
                ax.scatter(y=in_num, x=score, c="dimgrey", s=10, zorder=2)
        elif mode == "scatter":
            fmt = "D" if "Dataset" in label else "."
            ax.errorbar(
                y=in_num,
                x=score,
                xerr=grad.std(axis=0),
                color=color,
                fmt=fmt,
                alpha=0.5,
                label=label,
            )
        else:
            raise NotImplementedError(
                'plot mode can be only "barh","violin","scatter".'
            )

        if not per_class:
            break

    # >> legend
    ax.set_xlabel("Sensitivity")
    ax.set_yticks(in_num)
    ax.set_yticklabels(feature_names, fontsize=9)
    ax.set_ylabel("Input features")

    if mode == "violin":
        ax.legend(*zip(*patch_labels), loc="lower right", frameon=False)
    else:
        ax.legend(loc="lower right", frameon=False)
    if np.min(results["sensitivity"]["Dataset"])>=0: 
        ax.set_xlim(0, None)
    else:
        ax.axvline(0,color='grey')
    ax.set_ylim(-1, in_num[-1] + 1)

    if return_ax:
        return ax


def test_utils_plot():
    import matplotlib

    x = np.linspace(-1.5, 1.5)
    y = np.linspace(-0.5, 2.5)

    mp = muller_brown_potential(x, y)
    mp = muller_brown_potential_three_states(x, y)

    pal = paletteFessa
    pal = paletteCortina

    cmap = matplotlib.colors.Colormap("fessa", 2)
    cmap = matplotlib.colors.Colormap("fessa_r", 2)
    cmap = matplotlib.colors.Colormap("cortina80", 2)
    cmap = matplotlib.colors.Colormap("cortina80_r", 2)
