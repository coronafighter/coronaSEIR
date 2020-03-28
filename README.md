# coronavirus SEIR model

Simple SEIR model Python script for the COVID-19 pandemic with real world data.  
  
Purpose is to easily be able to experiment and better understand what is happening currently and what might happen in the near future.  
  
What I learned: Activating containment measures early can save lives.  

## Other models
* Nice webgui: http://gabgoh.github.io/COVID/index.html  
* Another great web based model: https://neherlab.org/covid19/  
* rewrite of this project with sophisticated code: https://github.com/cfculhane/coronaSEIR  

## Disclaimer
This is not a scientific or medical tool. Use at your own risk. BETA! There might be serious bugs.  

## Features
* SEIR epidemic model
* Reduced R0 after a certain amount of days to account for containment measures.
* Delays to allow for lagging official data etc.
* hopefully easily readable code
* Real world data automatically updated every three hours from Johns Hopkins CSSE (https://github.com/CSSEGISandData/2019-nCoV) via https://github.com/ExpDev07/coronavirus-tracker-api
* country population data (https://github.com/samayo/country-json)
* can exclude countries, e.g. world without China
* check out screenshots below

## Installation / Requirements / Documentation
Needs Python 3.x installed. Tested on Ubuntu. Should run on Window and Mac, too.
  
```
# everything after the hash symbol # is a comment
$ git clone https://github.com/coronafighter/coronaSEIR  # create local copy
$ pip3 install --upgrade numpy scipy matplotlib python-dateutil  # might need sudo -H pip3 ...
$ python3 ./main_coronaSEIR.py
read data: 843103 bytes
r0: 5.20    r1: 1.30
doubling0 every ~3.4 days
day 60
 Infected: 119363 0.2
 Infected found: 1085 0.0
 Hospital: 787 0.0
 Recovered: 44584 0.1
 Deaths: 17 0.0
data points for Italy: 40
first data: 2020-01-31
latest data: 2020-03-10 (you can update the data manually by running fetch_data.py)

$python3 ./world_data.py  # to just plot current numbers

$python3 ./deaths_per_capita.py  # might be a better measure than cases per capita

$ git pull origin master  # update to latest version, might overwrite local changes

```  
No GUI, you need to alter the script and run again to experiment.  
  
Note: Make sure you got correct number for population and available ICU units for your country.
  
## ToDo
* idea: compare optimal fit doubling time for all countries
* idea: compare death rate by testing capacity --> extrapolate fit curve to find real death rate
* make R0 and days0 lists to be able to have more than two phases
* add data about intensive care units
* ventilator patients separately?
* make parsing code cleaner / simpler
* be more precise in differentiation between hospitalization and ICU
* X automatic date offset
* X maybe find a better fit with lower R0 - the infectious time seems to be quite short?
* X add proper list of populations
* X use real dates instead of days?

## Credits
Based on:  
https://github.com/ckaus/EpiPy  
https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/  
  
API/Data:
https://github.com/ExpDev07/coronavirus-tracker-api
https://github.com/samayo/country-json
  
Formulas:  
https://hal.archives-ouvertes.fr/hal-00657584/document  
https://institutefordiseasemodeling.github.io/Documentation/general/model-seir.html  
  
Parameters:  
https://www.reddit.com/r/COVID19/comments/fbdzc1/coronavirus_epidemiology_metaanalysis_and/  
https://www.reddit.com/r/COVID19/comments/fbxk43/update_open_source_simple_coronavirus_modeling/  
timeline https://www.reddit.com/r/COVID19/comments/fd6lmg/infectionfatalityratio_ifr_of_covid19_is/  
https://www.reddit.com/r/COVID19/comments/ffzqzl/estimating_the_asymptomatic_proportion_of_2019/  
https://www.reddit.com/r/Coronavirus/comments/f8k2nj/why_sarscov2_is_not_just_the_flu_with_sources/ 
gamma: Generation time (serial interval): https://www.medrxiv.org/content/10.1101/2020.03.05.20031815v1  
also: http://www.cidrap.umn.edu/news-perspective/2020/03/short-time-between-serial-covid-19-cases-may-hinder-containment  
Relationship hospitalized/ICU/death https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/Imperial-College-COVID19-NPI-modelling-16-03-2020.pdf  
r0 ~ 3 https://www.newscientist.com/article/2238578-uk-has-enough-intensive-care-units-for-coronavirus-expert-predicts/  
sigma: Infection occurs before symptoms (Drosten): https://www.medrxiv.org/content/10.1101/2020.03.08.20032946v1.full.pdf  
Number of asymptomatics: https://www.zmescience.com/medicine/iceland-testing-covid-19-0523/  
some more in the source code

## Screenshots
![model run](https://github.com/coronafighter/coronaSEIR/blob/master/screenshots/model_run.png)
![model run](https://github.com/coronafighter/coronaSEIR/blob/master/screenshots/model_run2.png)
![data](https://github.com/coronafighter/coronaSEIR/blob/master/screenshots/data.png)

## License
MIT license
