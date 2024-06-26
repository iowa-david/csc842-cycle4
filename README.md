# System Performance Monitoring Utility

Logging of key system performance metrics along with the applications that are taking extra resources

# video link
https://youtu.be/T1MvyPTyD3I

## Description

Originally, I wanted to find information related to what is running on the computer at startup along with what services are running. But after seeing Group 1 presentations, I saw something similar had been done. In keeping with the theme of viewing computer usage, I decided to look at what can be done for creating a performance monitoring process. I wanted to put something together that can be run across multiple environments and gather information at a point in time to be able to look to see if there is any resource contention at a particular point in time. In addition, I had not done threaded programming in Python and wanted to get familiarity with await async processing.


## Table of Contents

  - Requirements
  - Installation
  - Use
  - Three Main Points
  - Why I am interested
  - Areas of Improvement

## Requirements
- Python 3
- Psutil  library
- Location to store the data (I’m using sqlite in this example)


## Installation

1. Clone the repository

   git clone https://github.com/iowa-david/csc842-cycle4.git


          

## Use

  python3 machine_usage.py

  higher or lower thresholds for CPU and Memory usage percentages can be changed by using the _THRESHOLD global variable

  the time to sleep between intervals is set by using the _WAIT global variable


## Three Main Points
  - The tool should leverage libraries that allow for running across different platforms.
  - Distill the information into a format so it can be saved easily into a reporting platform to query across different times.
  - Capture specific programs that are using more than identified threshold for CPU and memory to look to see if they are causing system issues.

## Why I am Interested
In my day job, I have worked to find what system processes are causing issues, historically there have not been tools that help to find this information very effectively and narrowing them down causes a headache. Some of the issues I have found historically have been when new tools are installed on the server where my applications are running. They have been from multiple logging frameworks running on one machine for instance. Having a tool that stores baseline information and compares from week to week would allow for me to compare what tools are being run at a time to alleviate system performance issues. This can help to determine if scheduled tasks are negatively impacting system performance by bulk processing or other targeted issues.

## Areas of Improvement

- I would like to have this set up for any myriad of storage options, SQL Server, SQL lite, Mongo, etc.
- Automate anomaly detection across times of day to determine if there are outlier processes running on different days or from week to week.
- Look into other tools that can be used to tie more functionality together and extend the tool such as osquery to access data via a sql like API.

## for more information
[psutil](https://github.com/giampaolo/psutil)

[OSQuery](https://github.com/giampaolo/psutil](https://github.com/osquery/osquery?tab=readme-ov-file))
