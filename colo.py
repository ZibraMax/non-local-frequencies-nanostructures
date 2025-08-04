import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as interp


df = pd.read_csv("Cubos_Enmallado.csv")
groups = df.groupby("l/R")

for nombre, grupo in groups:
    grupo = grupo.drop_duplicates()
    grupo = grupo[grupo['z1'] == 0.5]
    grupo = grupo.sort_values(by='ne')
    _X = grupo['ne'].values**(1/3)
    _Y = grupo["eta1"].values

    # Drop duplicates in _X and _Y
    unique_indices = np.unique(_X, return_index=True)[1]
    _x = _X[unique_indices].tolist()
    _y = _Y[unique_indices].tolist()
    _x += [max(_x) + 1]
    _y += [_y[-1]]
    ne = np.linspace(2, 12, 11)
    X = (ne)
    Y = interp.interp1d(_x, _y, kind='quadratic', fill_value='extrapolate')(X)

    # Get relative error in Y
    YY = []
    for i in range(len(Y)-1):
        YY.append(abs((Y[i+1] - Y[i]) / Y[i]))
    YY = np.array(YY)
    plt.plot(X[:-1], YY*100, "o-", label=f'l/R={nombre:.2f}')
plt.grid()
plt.xlabel('$ne_x$')
plt.ylabel('$\\Delta \\eta_{nl}|_{z_1=0.5} [\\%]$')
# Horizontal line at 0.5%
plt.axhline(y=0.5, color='r', linestyle='--', label='0.5%')
plt.ylim(0, 5)
plt.legend()
plt.tight_layout()
plt.savefig('error_eta.png', dpi=300, bbox_inches='tight')
plt.show()
