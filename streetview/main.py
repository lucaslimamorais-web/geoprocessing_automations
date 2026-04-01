import tkinter as tk
import webbrowser
from pyproj import Transformer

def abrir_maps():
    entrada = entry.get().strip()
    zona_str, easting_str, northing_str = entrada.replace(",", ".").split()
    zona_num = int(zona_str[:-1])
    hemisferio = zona_str[-1].upper()

    easting = float(easting_str)
    northing = float(northing_str)

    if hemisferio == "N":
        epsg_code = f"326{zona_num:02d}"
    else:
        epsg_code = f"327{zona_num:02d}"

    transformer = Transformer.from_crs(f"EPSG:{epsg_code}", "EPSG:4326", always_xy=True)
    lon, lat = transformer.transform(easting, northing)

    maps_url = f"https://www.google.com/maps/@{lat},{lon},15z"
    street_url = f"https://www.google.com/maps?q&layer=c&cbll={lat},{lon}"

    webbrowser.open(maps_url)
    webbrowser.open(street_url)

root = tk.Tk()
root.title("StreetView")

label = tk.Label(root, text="Cole as coordenadas UTM:")
label.pack()

entry = tk.Entry(root, width=40)
entry.pack()

botao = tk.Button(root, text="Abrir no Google Maps", command=abrir_maps)
botao.pack()

root.mainloop()
