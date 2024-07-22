import matplotlib.pyplot as plt

def gridline(plot_type):
    for plot in plot_type:
        plot.grid(b=True, which='major', color='k', linestyle='-', alpha=0.3)
        plot.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.1)

cycle = {'magma':   ["#050418", "#3e0f72", "#7b2281", "#b3357a", "#ee5d5d", "#feb57c", "#fcf2b4"],
         'magma_compressed': ["#3e0f72", "#feb57c", "#fcf2b4"],
         'viridis': ["#fafa6e", "#c4ec74", "#92dc7e", "#64c987", "#39b48e", "#089f8f", "#00898a", "#08737f", "#215d6e", "#2a4858"]
        }



