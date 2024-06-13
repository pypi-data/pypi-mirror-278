# plotdelice 📊
A collection of functions to plot old school style graphs with significance bars and automated stat testing (still verify it is the adequate test for your data).
## Install
```python
pip install PlotDelice
```
## Gallery
**Violin plot**

```python
from plotdelice.graphs import violinplot_delice, scatterplot_delice, markerplot_delice, barplot_delice
import pandas as pd

# read data
df = pd.read_csv("path_to_your_file.csv")

# define what you want to plot
x_group = "genotype"
y_variable = "angle"
y_label = r'Somite Angle [°]'

# plot
violinplot_delice(df,x_group,y_variable,violin_width=0.8,y_label=y_label,palette="Greens_d",point_size=40,jitter=0.09)
```


![alt text](assets/image.png)

**Scatter plot**
![alt text](assets/scatter.png)
**Custom marker plot**
```python
from svgpath2mpl import parse_path

# df['coords'] contains an svg path for each custom marker
df['coords'] = df['coords'].apply(parse_path)
fig, axs = markerplot_delice(df,"solidity","eccentricity","kmeans","coords",add_regression='logx',palette='Set2',figsize=(10,5))
```
![alt text](assets/marker.png)



