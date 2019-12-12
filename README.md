# GITLAB-MANAGER

> Manage Merge requests and Releases with gitlab-api

This script is designed to help you deal with changelog.
When you want to add a changelog there's different ways to create it. And the main goal here it's to have it done automatically without committing a file each time.
The strategy relies on merge requests.

A Python script for:
* merge requests:
  * lists them wip or not
  * update a MR with label and milestone
* changelog:
  * print changelog for a certain milestone (aka next tag) in different output: json, text, html
  * push with the release API on gitlab your changelog

## Table of Contents

- [Description](#description)
- [Install](#install)
- [Usage](#usage)
- [Contribute](#contribute)
- [License](#license)

## Description

### Merge requests

Merge requests are a good way to work with git because it permit to review code easily in an environment of multiple users (or not)
You can also defined a list of merge requests wich will be merged for a certain release.
We will use two important features of MR: label and milestone.
* label:
  Tag to put on a MR:
  Example: You created 2 MRs for 2 different goals, the first one is a bug fix to correct some issue in your code. you can add the label FIX on your MR
  The second one is an important feature to add a functionality to your code you can then add a label Feature on this particular MR
* milestone:
  Milestone can be seen as tag. You have 3 MRs and you want the two first to be released at the next version of your code.
  You can add for example a tag 1.0.0 to them and a tag 2.0.0 for the last one.
  Now you know which MRs will be on which release.

### Changelog

Changelog is important for communication to your team, other teams or even any user of your code.
With a changelog, everyone knows differences between each release of your code.
But a changelog is difficult to maintain. Some people commit a file in their repo, others will print each commit on the changelog..
There's no better way of dealing with it. You have to find the right one suitable for you.

I think you realized that my way for generating a changelog is with merge requests.

With this script, I chose to use Gitlab feature called: Releases. 
There's an API given by Gitlab to manage them.  

So when I have a list of MRs for a certain milestone I can push that on gitlab and have a really nice changelog on Releases section of Gitlab.


## Install

This module requires [Python 3](https://www.python.org/downloads/).
You can [download it](https://www.python.org/downloads/) or install it with brew on Mac.

```
$ brew install python3
```

Clone this repository and install `pip` dependencies:

```
$ git clone https://github.com/Adriks976/gitlab-manager.git
$ cd gitlab-manager
$ pip3 install -r requirements.txt
```


## Usage

Important: To contact Gitlab API you need 2 parameters: an URL and a private token

You can speficy this parameters with the script or the best way is to have on your home a file called .python-gitlab.cfg

```
[global]
default=gitlab.com
ssl_verify = true
timeout = 5

[gitlab.com]
url = https://gitlab.com
private_token = YOUR_TOKEN
```


```
usage: gitlab-manager [-h] [--gitlab-url GITLAB_URL]
                      [--gitlab-token GITLAB_TOKEN]
                      project {mr,changelog} ...

manage gitlab api mr and changelog

positional arguments:
  project
  {mr,changelog}

optional arguments:
  -h, --help            show this help message and exit

  --gitlab-url GITLAB_URL
                        Specify gitlab url ex: https://gitlab.com
  --gitlab-token GITLAB_TOKEN
                        Specify private gitlab token
```

### Lists MRs

```
usage: gitlab-manager project mr ls [-h] [--wip {yes,no}]

optional arguments:
  -h, --help      show this help message and exit
  --wip {yes,no}  search wip or not
```


```
$ gitlab-manager MY_PROJECT_NAME mr ls
    Here is the list of MRs for your chosen project:

    [
      {
        "Author": "Adriks976",
        "Description": "Description for my new feature",
        "Id": 1,
        "Label": "Feature",
        "Title": "New feature",
        "Url": "https://gitlab.com/MY_PROJECT_NAME/merge_requests/1"
      },
      {
        "Author": "Adriks976",
        "Description": "Description for my bug fix",
        "Id": 2,
        "Label": "Fix",
        "Title": Wip: [Fix]: oupss there's a bug",
        "Url": "https://gitlab.com/MY_PROJECT_NAME/merge_requests/2"
      }
    ]

```


```
$ gitlab-manager MY_PROJECT_NAME mr ls --wip no
    Here is the list of MRs for your chosen project:

    [
      {
        "Author": "Adriks976",
        "Description": "Description for my new feature",
        "Id": 1,
        "Label": "Feature",
        "Title": "New feature",
        "Url": "https://gitlab.com/MY_PROJECT_NAME/merge_requests/1"
      }
    ]
    
```

```
$ gitlab-manager MY_PROJECT_NAME mr ls --wip yes
    Here is the list of MRs for your chosen project:

    [
      {
        "Author": "Adriks976",
        "Description": "Description for my bug fix",
        "Id": 2,
        "Label": "Fix",
        "Title": Wip: [Fix]: oupss there's a bug",
        "Url": "https://gitlab.com/MY_PROJECT_NAME/merge_requests/2"
      }
    ]
    
```

### Update a MR

You can add label and milestone.


```
usage: gitlab-manager project mr update [-h] [--label LABEL] [--tag TAG] mr_id

positional arguments:
  mr_id

optional arguments:
  -h, --help     show this help message and exit
  --label LABEL  put a speficic label ex: Feature
  --tag TAG      put a speficic tag ex: 0.2.0
```


```
$ gitlab-manager MY_PROJECT_NAME mr update 1 --label FEATURE --tag 0.1.0
    ### [FEATURE]: New feature

    *  Description for my new feature

        * by: Adriks976

        * Merge Request ID:1

```

### Generate changelog

```
usage: gitlab-manager project changelog print [-h] [--output {json,text,html}] tag

positional arguments:
  tag                   generate changelog for specific tag ex: 0.2.0

optional arguments:
  -h, --help            show this help message and exit
  --output {json,text,html}
                        Define the output you want for the changelog
```


```
$ gitlab-manager MY_PROJECT_NAME changelog print 0.1.0
    Your changelog for 0.1.0 on Project MY_PROJECT_NAME:

    [
      {
        "Author": "Adriks976",
        "Description": "Description for my new feature",
        "Id": 1,
        "Label": "Feature",
        "Title": "New feature",
        "Url": "https://gitlab.com/MY_PROJECT_NAME/merge_requests/1"
      }
    ]
```

```
$ gitlab-manager MY_PROJECT_NAME changelog print 0.1.0 --output text
    Your changelog for 0.1.0 on Project MY_PROJECT_NAME:

    ### [FEATURE]: New feature

    *  Description for my new feature

        * by: Adriks976

        * Merge Request ID:1
```

```
$ gitlab-manager MY_PROJECT_NAME changelog print 0.1.0 --output html
    Your changelog for 0.1.0 on Project MY_PROJECT_NAME:

    <table class="table table-condensed table-bordered table-hover"><thead><tr><th>Author</th><th>Description</th><th>Id</th><th>Label</th><th>Title</th><th>Url</th></tr></thead><tbody><tr><td>Adriks976</td><td>Description for my new feature</td><td>1</td><td>Feature</td><td>New feature</td><td>https://gitlab.com/MY_PROJECT_NAME/merge_requests/1</td></tr></tbody></table>
```

### Push changelog on Relases

```
usage: gitlab-manager project changelog push [-h] tag

positional arguments:
  tag         generate changelog for specific tag ex: 0.2.0

optional arguments:
  -h, --help  show this help message and exit
```


## Contribute

PRs accepted.

Small note: If editing the Readme, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## License

[MIT](LICENSE)