


# SlackBot


<!-- MarkdownTOC -->

- Install
- Find your bot profile
- Add env variable
    - `printbotid.py`
    - OR make env var permanent
- Scripts
    - `myRCT_bot.py`

<!-- /MarkdownTOC -->



---


## Install



```bash
sudo pip install slackclient
```


## Find your bot profile

+   API Token
    *   __This info is extremely important.__
+   Customize Name
+   Icon


## Add env variable

```bash
export SLACK_BOT_TOKEN='your slack token'
```

Or run `addSlackToken.sh` under `~/.slackBot`





### `printbotid.py`

```bash
python printbotid.py 
#   xoxb-*************************
#   Bot ID for my_rctoken is ***************
```

Then 

```bash
export BOT_ID=**************
```





### OR make env var permanent

```bash
vi ~/.bash_proflle

```


## Scripts

### `myRCT_bot.py`

```bash
python myRCT_bot.py    
#   myRCT bot connected and running!
#   ......
```








