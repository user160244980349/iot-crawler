Web crawler for  privacy policies mining
----------------------------------------

This project is devoted to privacy policies mining and is now adopted for IoT
privacy
policies in English mining and for mining of websites privacy policies in
Russian.


How To
------

1. Copy `example.config.py` to `config.py` and make sure the temp dir under webdriver settings is reachable within your system.
1. Make virtual environment (recommended) with `python -m venv venv`.
1. Activate the virtual environment with `source venv/bin/activate`.
1. Execute `pip install -r requirements.txt`.
1. Execute `python main.py`.


Nuances which can take place
----------------------------

- The 4 config files i.e. `active_engines.py`, `active_modules.py`, `active_plugins.py` and `example.config.py` contain recommended settings to run the program and see what it actually does.
- The previous version of the crawler was outdated, an update has been provided.
- The marketplaces and other websites constantly improve their antiautomated usage capabilities, so it might turn that crawler is stuck on captcha (despite some counter arguments were delivered to overcome the issues).


Check list
----------

- [x] Multiprocessing
    - [x] Logging in separate process
    - [x] Proper termination

- [x] Scrapping
    - [x] Browser driver
    - [x] Disable cache
    - [x] Working with proxies
    - [x] Real user profile
    - [x] Scrapping plugins
        - [x] Amazon plugin
        - [x] Walmart plugin
        - [ ] Other ???
    - [x] Searching plugins
        - [x] Websites searching
        - [x] Websites filtering

- [ ] Policies
    - [x] Download policies
    - [x] Encoding mistakes
    - [x] Sanitization of policies
        - [x] Remove links
        - [x] Remove invisible elements
        - [x] Remove control elements
        - [x] Remove headers
        - [x] Remove footers
    - [x] Hash for policies
    - [x] Split by paragraphs
    - [ ] Policies metrics module
        - [x] Efficiency statistics
        - [x] Total policy length
        - [x] Tables yes/no and how many
        - [x] Lists yes/no and how many
        - [ ] Subsections yes/no how many and how long
    - [x] Manually added policies

- [ ] MailRuTop
    - [ ] header is not a p tag
    - [ ] more keywords to search
    - [ ] more templates for sanitization

Bugs
----

- [x] Synchronous run broken
- [x] Captcha fix for walmart plugin
- [x] Add keywords to search engine query
- [x] Wrong user agent setting
- [x] Reset headless mode after restart session
- [x] Change user agent on each request
- [x] Multiprocessing on scrapping causes captcha
- [x] Deadlock on exit
- [ ] Some encodings in Russian

MailRuTop
---------

Many categories are available for search. Configurable keywords for privacy
policies search.

IOT Devices Privacy Policies
----------------------------

This project is used to be an instrument for datasets creation

Marketplaces
------------

    amazon
    walmart

IOT Devices
-----------

    smart scale
    smart watche
    smart lock
    smart bulb
    indoor camera 
    outdoor camera 
    smart navigation system
    gps tracking device 
    voice controller
    tracking sensor 
    tracking device
    smart alarm clock
    smart thermostat
    smart plug
    smart light switch
    smart tv
    smart speaker
    smart thermometer
    smart video doorbell