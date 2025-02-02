### Getting Started
First of all we have to clone this repository,
``` bash
git clone git@github.com:BonnBytes/position_we_need_more_tests_in_ml.git
```
in a next step, to use the code in this project you need to configure an environment. 
To do that create a `.env`-file with the following content

``` bash
PYTHONPATH=.
OPENREVIEW_USERNAME=YOUR_OPENREVIEW_ACCOUNT_NAME
OPENREVIEW_PASSWORD=YOUR_PASSWORD
```


### Reusability
After cloning and navigating into this repository, you can install the code in this repository via pip.

``` bash
pip install .
```

### Download the data run
To aggregate the statistical data we used for the paper run the command below.

``` bash
./run_all.sh
```
