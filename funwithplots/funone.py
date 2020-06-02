# Import the necessary packages and modules
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# Uncomment following line to see the effect
# mpl.rcParams['lines.linewidth'] = 5

# Prepare the data
x = np.linspace(0, 1, 100)
f1 = lambda x: x ** 2
f2 = lambda x: 1 - (1 - 0.5 * x) ** 3
# Plot the data
plt.plot(x, x, label='x = y')
plt.plot(x, f1(x), label='x^2')
plt.plot(x, f2(x), label='corona')

# Add a legend
plt.legend()

# Show the plot
plt.show()
