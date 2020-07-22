# Italy Air Quality Aggregator (ITAQA)


<a href="https://github.com/albertosantagostino/ITAQA-air-quality-aggregator/commits/master" target="\_parent"><img alt="GitHub - License" src="https://img.shields.io/github/last-commit/albertosantagostino/ITAQA-air-quality-aggregator?label=latest%20commit"></a> <a href="https://github.com/albertosantagostino/ITAQA-air-quality-aggregator/issues" target="\_parent"><img alt="ITAQA open issues" src="https://img.shields.io/github/issues-raw/albertosantagostino/ITAQA-air-quality-aggregator"></a>

![ITAQA](docs/img/banner.png)

**ITAQA** is a framework built to **aggregate** Italy air quality data, collecting automatically measurements from different sources. It provides scripts and utilities to query data, analyze it and create visualizations

### The question that sparked this project

The idea of collecting and measuring air pollution in this period of time originated from this thought:

> As a consequence of the SARS-CoV-2 outbreak in Italy ([Wikipedia link](https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Italy)), will there be a measurable **effect on the air pollution** in the affected region(s) due to the "more people working from home therefore **less traffic**" effect? If yes, is this reduction strongly correlated with the level of lockdown enforced by the Italian government in these weeks/months?

More in general, the purpose of the framework is to provide national air pollution data in an **uniform and accessible way**

(If you are interested in learning more on ITAQA's origin, you should read [this post on my blog](https://albertosantagostino.github.io/blog/2020/05/29/ITAQA_introduction_en))

## Objectives

* Create a single place to orchestrate the download of pollution data from different Italy regions (through **ARPA** websites)
  * Unfortunately, ARPA websites are very diverse among Italian regions (as an example, see the websites of [ARPA Piemonte](http://www.arpa.piemonte.it/) vs [ARPA Lombardia](https://www.arpalombardia.it/Pages/ARPA_Home_Page.aspx) vs [ARPA Emilia-Romagna](https://www.arpae.it/))
    As far as I know a single way to collect pollution data from all the stations distributed on the whole country with a "single national API call" doesn't exist
* Build a tool to graphically visualize data and history of pollutants in different areas of the country
* Search correlation between big "behavior-changing" events and air pollution

## Usage

#### Overview

The core concept of ITAQA are **AirQualityStation** (or **AQS**) objects. They represent sensors holding time indexed pollution data for a specific location

Data aggregation and download is performed by **crawlers**, scripts that obtain pollution records for a specific region and time, parse and store them in **AirQualityStationCollection** (or **AQSC**) objects

#### Installation

Clone the repository (`git clone git@github.com:albertosantagostino/ITAQA-air-quality-aggregator.git`), check that you have Python 3.8 (`python --version`) and install all the needed packages (directly via `poetry install`, refer to [Poetry's documentation](https://python-poetry.org/docs/basic-usage/#installing-dependencies))

#### Invocation

The main entrypoint is the script `itaqa.py`. Run it using the `-h` parameter to see the built-in help

```
itaqa.py [MODE] [parameters] [-h]
```

**Available modes**  

```
download      Download data, serialize and save it in a AQSC object
update        Given an existing AQSC collection, update it with the most recent data
test          Run all the unit tests
sandbox       Run a special section for debugging/testing purposes
```
#### Example

If you want to perform a data download to check if everything is working, you can perform the following steps:

**Data download**  
Download data from Lombardia for the first month of 2020:  
```
python3 itaqa.py download --region lombardia --min_date 20200101 --max_date 20200201  
```

The message _"Download completed!"_ indicates the successful download and serialization of all the requested data. Air quality information for the specified period has been stored in a AQSC object (a special collection that encapsulates multiple AQS, saved as a `.msgpack` file)

**Data analysis and visualization**  
While ITAQA is currently meant for developers, a basic GUI to explore and view data is ready to be used. Start the GUI with the command:  
```
python3 itaqa.py view
```
A graphical application will start. Select the folder where the data is stored to see the AQS objects and to visualize the contained data directly in a browser using the correspondent button.

As an alternative, data can be loaded and explored directly editing the sandbox section of `itaqa.py`, and invoking the main script in this way:

```
python3 itaqa.py sandbox
```

## Architecture
<p align="center">
  <img src="docs/architecture/architecture.png" title="ITAQA Architecture" width="500" />
</p>

## FAQ

**Why make this project? Why not reuse one of the already existing air quality plots and websites?**

> The first use case is to investigate the thesis above ("*Has lockdown a measurable effect on air quality? In what measure?"*)  
> Nevertheless, the aim of this project is broader: create a set of reusable air quality analysis tools that unify all different sources from the regions of Italy

**There is already an air quality/pollution aggregator, you can find it and use it at this link...**

> Nice! I didn't check if this thing was already existing, because if I do this all the time, I wouldn't get any projects done :)  
> (I'm mainly developing this as a personal project, to learn stuff in the process)

**What are these regional "ARPA"?**

> These are *"Agenzie Regionali per la Protezione Ambientale"* (*Regional Environmental Protection Agency*), Italian governmental agencies that collect and analyze air, water, acoustic and soil pollution data on all the territory

**Do you plan to publish some visualizations/plots produced?**

> Yes! As soon as I have something worth showing that I consider interesting, I will publish it in [my blog](https://albertosantagostino.github.io/)

**Can I contribute?**

> Yes, of course, refer to [CONTRIBUTING](CONTRIBUTING.md) to find all the needed information (setup, developer environment, workflow)

## ARPA Websites

| **Region**                                                   | ARPA Website                                                 | Simple crawler | Complete AQSC |
| ------------------------------------------------------------ | ------------------------------------------------------------ | -------------- | ------------- |
| [Abruzzo](http://www.comuni-italiani.it/13/index.html)       | [ARTA Abruzzo](https://www.artaabruzzo.it/)                  |                |               |
| [Basilicata](http://www.comuni-italiani.it/17/index.html)    | [ARPA Basilicata](http://www.arpab.it/)                      |                |               |
| [Calabria](http://www.comuni-italiani.it/18/index.html)      | [ARPA Calabria](http://www.arpacampania.it/)                 |                |               |
| [Campania](http://www.comuni-italiani.it/15/index.html)      | [ARPA Campania](http://www.arpacampania.it/)                 |                |               |
| [Emilia-Romagna](http://www.comuni-italiani.it/08/index.html) | [ARPA Emilia-Romagna](https://www.arpae.it/)                 | ✔️              |               |
| [Friuli-Venezia Giulia](http://www.comuni-italiani.it/06/index.html) | [ARPA Friuli-Venezia-Giulia](http://www.arpa.fvg.it/cms/)    |                |               |
| [Lazio](http://www.comuni-italiani.it/12/index.html)         | [ARPA Lazio](http://www.arpalazio.gov.it/)                   |                |               |
| [Liguria](http://www.comuni-italiani.it/07/index.html)       | [ARPA Liguria](https://www.arpal.liguria.it/)                |                |               |
| [Lombardia](http://www.comuni-italiani.it/03/index.html)     | [ARPA Lombardia](https://www.arpalombardia.it/Pages/ARPA_Home_Page.aspx) | ✔️              | ✔️             |
| [Marche](http://www.comuni-italiani.it/11/index.html)        | [ARPA Marche](https://www.arpa.marche.it/)                   |                |               |
| [Molise](http://www.comuni-italiani.it/14/index.html)        | [ARPA Molise](http://www.arpamolise.it/)                     |                |               |
| [Piemonte](http://www.comuni-italiani.it/01/index.html)      | [ARPA Piemonte](http://www.arpa.piemonte.it/)                | ✔️              |               |
| [Puglia](http://www.comuni-italiani.it/16/index.html)        | [ARPA Puglia](http://www.arpa.puglia.it/web/guest/arpa_home) |                |               |
| [Sardegna](http://www.comuni-italiani.it/20/index.html)      | [ARPA Sardegna](http://www.sardegnaambiente.it/arpas/)       |                |               |
| [Sicilia](http://www.comuni-italiani.it/19/index.html)       | [ARPA Sicilia](https://www.arpa.sicilia.it/)                 |                |               |
| [Toscana](http://www.comuni-italiani.it/09/index.html)       | [ARPA Toscana](http://www.arpat.toscana.it/)                 |                |               |
| [Trentino-Alto Adige](http://www.comuni-italiani.it/04/index.html) | [APPA Trento](http://www.appa.provincia.tn.it/) / [Ambiente Bolzano](https://ambiente.provincia.bz.it/) |                |               |
| [Umbria](http://www.comuni-italiani.it/10/index.html)        | [ARPA Umbria](http://www.arpa.umbria.it/)                    |                |               |
| [Valle d'Aosta](http://www.comuni-italiani.it/02/index.html) | [ARPA Valle d'Aosta](https://www.arpa.vda.it/it)             |                |               |
| [Veneto](http://www.comuni-italiani.it/05/index.html)        | [ARPA Veneto](https://www.arpa.veneto.it/)                   |                |               |

## License

This project and its source code are distributed under the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)
