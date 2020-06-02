import matplotlib.pyplot as plt
import numpy as np
import time

i = 1
# צריך להבין איך מעדכנים את הגרף ולא איך לצייר מחדש כל פעם
while i < 5:
    # Prepare the data
    x = np.linspace(0, 10, 100)

    # Plot the data
    plt.plot(x + i**2, x, label='linear')

    # Add a legend
    plt.legend()

    # Show the plot
    plt.show()
    i += 1
    time.sleep(1)
