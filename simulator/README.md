## 🚀 Installation

<details>
  <summary>A. Local Installation </summary>  
   . 
The back_end depends on [python-rocksdb](https://twmht.github.io/python-rocksdb/index.html) which builds rocksdb from c++ source when 
it is installed. A C++ compiler, compression libraries, and gflags must be available. The requirements for [building rocksdb](https://github.com/facebook/rocksdb/blob/main/INSTALL.md) are slightly different for each OS.  
  .  
Once rocksdb requirements are met, the most recent code can be installed directly from GitHub with:

```bash
$ git clone git+https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes.git
$ cd cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes
$ pip install simulator/front_end
$ pip install simulator/back_end
```
  
Or to install in development mode, use the following:

```bash
$ git clone git+https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes.git
$ cd cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes
$ pip install -e simulator/front_end
$ pip install -e simulator/back_end
```
  
</details>

<details>
  <summary>B. Local Openshift Installation</summary>
  
Install [OpenShift CodeReady Containers](https://developers.redhat.com/products/codeready-containers/overview) using the "Install OpenShift on your laptop" button.   
  In a command line terminal, use:    
`crc start` to launch the platform  
`eval $(crc oc-env)` to configure the OpenShift cli    
`oc login -u developer -p developer` to login  
  
  The GUI will be available at: https://api.crc.testing:6443  
  Follow Option C directions for building project sources.   
</details>

<details>
  <summary>C. MOC Openshift Installation </summary>   
.
  
Install the OpenShift [command line tool](https://docs.openshift.com/container-platform/4.9/cli_reference/openshift_cli/getting-started-cli.html#cli-getting-started)   
.    
Authenticate on [Mass Open Cloud](https://massopen.cloud/) and get a token to log into the command line oc interface.    
  
![CLI_TOKEN_HOWTO](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/simulator/openshift_cli.png)
.    
`/simulator/back_end_dependencies` contains a Docker file which prepares a centos7 image with all dependencies installed.  
 Use the two YAML files in this directory to create a buildstream location and build configuration on OpenShift for the image.   
.    
`/simulator/back_end` contains a Docker file which references the image stream set up in the previous step.  Use the two YAML files in this directory to create a buildstream location and build configuration on OpenShift for the image. This build config uses the OpenShift Source2Image(s2i) feature to copy the latest back_end source from this repository into the image, then it runs the cli.py file.    
.    
`/simulator/front_end` does not use a Docker file because there are fewer dependencies. Instead the build configuration directly uses a pre-built python s2i image. Use the two YAML files in this directory to create a buildstream location and build configuration on OpenShift for the image.
  
  
</details>

## 🚀 Usage

<details>
  <summary>A. Local Usage</summary>
.    
  
Get usage directions by running with --help option. 
```shell
$ python -m back_end --help
$ python -m front_end --help
```

There is a minimal hello world demo for testing the program (must be run in correct order, separate terminals).    
```shell
$ python -m front_end --hello_world
$ python -m back_end --hello_world
```

The full simulator can be run with a configuration that is hard-coded in the front_end cli.py file (must be run in correct order, separate terminals).     
```shell
$ python -m back_end --run
$ python -m front_end --run
```
</details>

<details>
  <summary>B. OpenShift Usage</summary>
.    
  
`simulator/front_end/src/traces/generate_trace_lists.py` is a helper script to generate datasets from the trace files on [tracer.filesystems.org](https://tracer.filesystems.org/). The file generated has a name that mimics the online directory structure replacing slashes with underscores. The end of the file name is a concatenation of all the trace users selected. There is a separate file generated per subdirectory of the website, containing tar archive file names. This file is copied into the front_end image when it is built and read line-by-line to open the correct trace files in order.   
.   
`simulator/experiment_configs/ex1` is an example of one experiment run. The directory contains a tab-separated spreadsheet. The columns of the spreadsheet are all of the possible algorithm parameters. Each row is a different combination of parameters, to be run one at a time. The automate.sh script reads this spreadsheet and uses the oc command line interface to create jobs for each parameter combo.    
.    
Create two persistent volume claims for the front_end to mount at runtime:      
`input-trace-files` is where the simulator will download files from [tracer.filesystems.org](https://tracer.filesystems.org/) if they do not already exist in persistent storage. The files are unzipped and read one at a time based on the list of trace file names provided via environment variable.    
  
`output-log-files` is where logs for each simulator run will be saved. While a front_end pod is running with this directory mounted, log files can be downloaded via the rsync command:
```shell
$ oc rsync cs6620-fall21-dedup-nodes-front-end-ex1:/var/output/ .
```
Run automate.sh to start the simulator.
  
</details>





### ⚖️ License

The code in this package is licensed under the MIT License.

<!--
### 📖 Citation

Citation goes here!
-->


### 🍪 Cookiecutter

This package was created with [@audreyfeldroy](https://github.com/audreyfeldroy)'s
[cookiecutter](https://github.com/cookiecutter/cookiecutter) package using [@cthoyt](https://github.com/cthoyt)'s
[cookiecutter-snekpack](https://github.com/cthoyt/cookiecutter-snekpack) template.
