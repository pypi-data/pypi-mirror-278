# MB Century Downhole Data Toolkit

https://www.mbcentury.com/services 

This toolkit provides easy access to data that has been exported from one of MB Century's data logging applications. It is primarily used to access downhole data that has been collected using MB Century's data collection systems.


## Example use

Use pip to import the package.

```ccs
pip import pymbc
```

## Example python code

Open a CSV file containing PTS data, plot it against depth and time, and convert it to Well Test Analysis format.
```css
import pymbc as mbc
from pathlib import Path

csvfile = Path(r'tests\_20230626_PTS__A.csv')
mb = mbc.MbcLog()
mb.ReadMbCsv(csvfile)
fnotes = csvfile.parent / (csvfile.stem + '_notes' + csvfile.suffix)
mb.ReadNotes(fnotes)
mb.CreateRunLog()
plotdef = [mbc.PlotDefinition('Timedelta', 'Depth', 'slategray', '-', False),
           mbc.PlotDefinition('Timedelta', 'Pressure', 'royalblue', '-', False),
           mbc.PlotDefinition('Timedelta', 'Frequency', 'darkorange', '-', False),
           mbc.PlotDefinition('Timedelta', 'Temperature', 'indianred', '--', True)]
st,figt = mbc.PlotLog(mb, plotdef, title=mb.name, depthaxis=False)

plotdef = [mbc.PlotDefinition('Depth', 'Timedelta', 'black', '-', False),
           mbc.PlotDefinition('Depth', 'Speed', 'forestgreen', '--', True),
           mbc.PlotDefinition('Depth', 'Pressure', 'maroon', '-', False),
           mbc.PlotDefinition('Depth', 'Temperature', 'royalblue', '-', True)]
sd,figd = mbc.PlotLog(mb, plotdef, title=mb.name, depthaxis=True)  

pts = mb.PtsWellTestAnalysis()
	
```      

