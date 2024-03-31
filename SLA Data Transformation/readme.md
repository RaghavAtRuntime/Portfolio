# SLA Configuration File Generation

## Description
`SLAconfig.py` generates SLA configuration files for any given Asset Contract List. This is done by reading the asset list csv document and cross-referencing it with `master_reference.csv`, which contains the time information for each remedy contract ID.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Testing](#testing)
- [Contact](#contact)

## Installation <a name="installation"></a>
The contents of this folder, in their entirety, may be placed in a single directory. After configuration (see [Configuration](#configuration)), the script is ready to run (see [Usage](#usage)).
The script requires Python version 3.11.1 to be installed. This can be done by downloading the appropriate installer from the [Python website](https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe).

If already installed, the version can be checked using `python3 --version`.

The functionality also requires `master_reference.csv`. Further setup instructions are in the [Configuration](#configuration) section.
No 3rd-party libraries are required; only standard Python libraries are used.

## Usage <a name="usage"></a>
The script can be used by simply running it through a command prompt or terminal window opened in the directory containing the script, using the command `python3 SLAconfig.py`.
The message 'Output file generated successfully.' should appear once the `SLA.cfg` file has been generated at the configured output directory.

## Configuration <a name="configuration"></a>
The configurable variables in the script are capitalized global variables, declared right after the import statements. For reference:
- `ENCODING` is set to `'latin-1'` by default but can be changed to the desired CSV encoding choice.
- `ASSET_LIST_FILE` is the filepath to the asset contract list.
- `MASTER_REFERENCE` is the filepath to the master reference CSV, which is set by default to be in the same directory as the script.
- `OUTPUT_FILE` is the desired output directory; the cfg file can be renamed to something other than `SLA.cfg` as well.

Any of these variables can be modified for convenience.
Additionally, it is assumed (and written in the preconditions of the script) that the asset contract list has two header lines.

## Testing <a name="testing"></a>
The script automatically runs a test to check whether the number of companies in the output configuration file match the number of companies in the asset contract list.
This ensures no entry has been missed.

## Contact <a name="contact"></a>
- Name: Raghav Sinha
- Email: astroraghav04@gmail.com
