## More Rigorous Software Engineering Would Improve Reproducibility in Machine Learning Research

Source code for our [position paper on software engineering in machine learning](https://arxiv.org/pdf/2502.00902).
An example template repository for most concepts discussed in the paper is available [here](https://github.com/Deep-Learning-with-Jax/day_01_exercise_intro/tree/main). 

### Getting Started
First of all, we have to clone this repository,
``` bash
git clone git@github.com:BonnBytes/position_we_need_more_tests_in_ml.git
```
In the next step, you need to configure an environment to use the code in this project. 
To do that, create a `.env`-file with the following content.

``` bash
PYTHONPATH=.
OPENREVIEW_USERNAME=YOUR_OPENREVIEW_ACCOUNT_NAME
OPENREVIEW_PASSWORD=YOUR_PASSWORD
```

This crawler utilizes the Selenium package, which in turn requires an installed version of the Chrome browser.

### Reusability
After cloning and navigating into this repository, you can install the code in this repository via pip.

``` bash
pip install .
```

### Reproduction
To aggregate the statistical data we used for the paper, run the command below.

``` bash
./run_all.sh
```

### Run the tests
Set up a dotenv with your OpenReview account credentials. Make sure you set the
`OPENREVIEW_USERNAME` and `OPENREVIEW_PASSWORD` variables are set correctly. To run the tests, type
``` bash
nox -s test
```
into the console.





### Funding

The Bundesministerium für Bildung und Forschung (BMBF) supported research through its "BNTrAInee" (16DHBK1022) and "WestAI" (01IS22094A) projects. 
The sole responsibility for the content of the paper and this corresponding code lies with the authors.
<table>
<tr>
    <td><img src="https://github.com/Machine-Learning-Foundations/.github/blob/main/profile/img/nrw-logo.png" height="150"></td>
    <td><img src="https://github.com/Machine-Learning-Foundations/.github/blob/main/profile/img/BMBF_gefoerdert_2017_en.jpg" height="150"></td>
</tr>
</table>
