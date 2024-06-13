# SupSpec

Hello! Thank you for using **SupSpec**!\
`SupSpec` (**Sup**ernova **Spec**tra Fitter) is a quick tool which aids in finding the velocity structure of spectral features throughout the supernova ejecta. This code is designed to require minimal user interaction and can ingest an arbitrarily large number of spectra. With it, one can infer both the velocity of supernova ejecta expansion, and the relative depths of various elements in the ejecta. The user can input spectral data in a range of formats (.txt, .data, .out, etc.), choose a spectral line and window, and receive an output of graphs. 


## Installation

`SupSpec` is available on `pip` and can be installed using:

```
pip install supspec
```

## Using SupSpec

Before using `SupSpec`, store all your data in a folder called "data". Then, open terminal at the location and run `run.py`. 

```
python run.py 
```

You can also pass in 3 arguments at the terminal: mode, directory, and extension.
- **Mode**: `-v` at the end of the command activates verbose mode. The default is quiet mode.
- **Directory**: `-d <directory>` at the end of the command sets that directory as the directory which holds spectroscopy data. The default directory is a folder called "data" inside the current directory.
- **Extension**: `-e <extension>` extends the type of file for spectroscopy data in addition to .txt, .data, or .out files.

In verbose mode, the user can check the window of each spectrum, change the number of walkers and iterations, and view the results of every walker. In quiet mode, figures will not pop up but simply stored inside the Result folder.

For example, if I wish to use verbose mode, and my data is stored in a folder called `spectra/`. I would type in the command:

```
python run.py -v -d spectra
```
