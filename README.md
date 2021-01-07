
# Table of Contents

1.  [Requirements](#org7b8f8cc)
2.  [Install](#orgeb8b95d)
3.  [Basic Usage](#org09f85b1)
4.  [Tips](#org89ea913)
    1.  [Map container volume when running](#org3202aaf)

This is a crawler tool to aid in the metric collection of gitlab issues.

The application read issues' html **files** from `./app/html/` and print metrics to stdout.


<a id="org7b8f8cc"></a>

# Requirements

[Docker](https://www.docker.com)


<a id="orgeb8b95d"></a>

# Install

Clone this repository into your machine. Ex:

    git clone git@gitlab.com:qualyteam-group/qualyteam-novos-projetos/issue-spider.git

`cd` to its directory and build a docker image from the `Dockerfile`:

    docker build . -t issue-spider


<a id="org09f85b1"></a>

# Basic Usage

Put issues' html files at `./app/html/` and run the container interactively:

    docker run --rm -it

The issues' metrics will be printed. Example output:

    
    >>> Scraping metrics for "Registrar cópias controladas (#3061) "...
    
    READY TO TEST PLANNING	TEST PLANNING	READY TO DEVELOPMENT	DEVELOPMENT	READY TO REVIEW	REVIEW	READY TO TEST	TEST	READY TO HOMOLOGATION	HOMOLOGATION	DONE
    30/11/2020 18:10	01/12/2020 09:24	01/12/2020 10:10	04/12/2020 09:46	17/12/2020 08:16	17/12/2020 09:08	04/01/2021 14:18	04/01/2021 14:32	05/01/2021 10:26	05/01/2021 11:02	05/01/2021 13:28
    
    <<<
    >>> Scraping metrics for "Tabela de coleta do kpi não sendo atualizada ao filtrar novo período (#3082)"...
    
    BACKLOG	READY TO DEVELOPMENT	DEVELOPMENT	READY TO REVIEW	REVIEW	READY TO TEST	TEST	READY TO HOMOLOGATION	HOMOLOGATION	DONE
    17/12/2020 11:05	18/12/2020 10:47	18/12/2020 14:45	18/12/2020 17:11	04/01/2021 08:35	04/01/2021 09:41	04/01/2021 09:54	04/01/2021 11:20	05/01/2021 11:02	05/01/2021 13:28
    
    <<<
    >>> Scraping metrics for "Ajustar Navbar para mobile (#3083) "...
    
    READY TO DEVELOPMENT	DEVELOPMENT	READY TO REVIEW	REVIEW	READY TO TEST	TEST	READY TO HOMOLOGATION	HOMOLOGATION	DONE
    17/12/2020 15:40	18/12/2020 11:53	18/12/2020 14:44	04/01/2021 08:35	04/01/2021 09:41	04/01/2021 10:59	04/01/2021 13:44	05/01/2021 11:02	05/01/2021 13:28
    
    <<<
    Done!


<a id="org89ea913"></a>

# Tips


<a id="org3202aaf"></a>

## Map container volume when running

It is **highly** recommended to check in which directory your browser saves html pages and map it to `./app/html/` when running the container, so it won't be necessary to move files around before running the app. Just right click and save the pages from the browser and run the applicaton.

Linux example given html files are stored in the Desktop:

    docker run --rm -itv ~/Downloads/:/app/app/html/ issue-spider

Windows example with User's `Downloads` directory:

    docker run --rm -itv %userprofile%\Downloads\:/app/app/html/ issue-spider

