import json
import numpy as np
import os


def parse_json(json_str):
    """Parse a JSON string into a Python dictionary.

    Args:
        json_str (str): The JSON string to parse.

    Returns:
        dict: The parsed JSON object.
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e


FOLDER = "Cubos"
syms = []
files = os.listdir(FOLDER)
files = [os.path.join(FOLDER, file) for file in files]
for file in files:
    if file.endswith('.json'):
        with open(file, 'r') as f:
            json_str = f.read()
            try:
                parsed_json = parse_json(json_str)
                parsed_json['properties']['material'] = file.split('_')[0]
                syms.append(parsed_json)
            except ValueError as e:
                print(e)
    elif file.endswith('.npy'):
        data = np.load(file, allow_pickle=True)
        print(f"Loaded numpy array from {file}: {data}")
    else:
        print(f"Unsupported file type: {file}")
with open(f'{FOLDER}.txt', 'w') as f:
    f.write("rho,l,C11,C12,C44,duration,name,material,R,z1,l/R,Ct,eta1,eta2,eta3,eta4,eta5,eta6\n")
    for sym in syms:
        rho = sym['properties']['rho'][0]
        l = sym['properties']['l']
        C = sym['properties']['C']
        C11 = C[0][0]
        C12 = C[0][1]
        C44 = C[3][3]
        if C11 == 1280000000:
            material = 'Carbonium'
        elif C11 == 182500000:
            material = 'Germanium'
        elif C11 == 223100000:
            material = 'Siliconium'

        duration = sym['properties']['duration']
        name = sym['properties']['name']
        # CaCube_8.05_2.0_20250428-105421
        L = float(name.split('_')[1])
        z1 = sym['properties']['z1']
        if FOLDER == 'Cubos':
            R = L/1.612
        else:
            R = L
        l_R = l/R
        Ct = (C44/rho)**0.5
        etas = []
        for solution in sym['solutions']:
            eigv = solution['info']['eigv']
            omega = eigv**0.5
            eta = omega*R/Ct

            if eigv > 1e-3:
                etas.append(round(eta, 7))
        etas = np.unique(etas)
        etas = [str(i) for i in etas]
        etas = ','.join(etas)
        f.write(
            f"{rho},{l},{C11},{C12},{C44},{duration},{name},{material},{R},{z1},{l_R},{Ct},{etas}\n")
a = 0
