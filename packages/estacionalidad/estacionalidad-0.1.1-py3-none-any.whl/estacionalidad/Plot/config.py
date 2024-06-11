import matplotlib.pyplot as plt
from matplotlib import font_manager
import os


FONT_PATH = os.path.join(
    os.getcwd(), "src/estacionalidad/fonts/Helvetica-Neue-LT-Std-77-Bold-Condensed_22542.ttf")

font_manager.fontManager.addfont(FONT_PATH)
prop = font_manager.FontProperties(fname=FONT_PATH)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()
