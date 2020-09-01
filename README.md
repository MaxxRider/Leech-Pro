# Help and Support [Admin](https://telegram.dog/MaxxRider)
# working example group [Leech Here](https://telegram.dog/joinchat/OV5y_FarWaGaNYUIYr6J9w)

# Telegram Torrent Leecher 🔥🤖

A Telegram Torrent (and youtube-dl) Leecher based on [Pyrogram](https://github.com/pyrogram/pyrogram)

# Benefits :-
    ✓ Telegram File mirrorring to cloud along with its unzipping, unrar and untar
    ✓ Drive/Teamdrive support/All other cloud services rclone.org supports
    ✓ Unzip
    ✓ Unrar
    ✓ Untar
    ✓ Custom file name
    ✓ Custom commands
    ✓ Get total size of your working cloud directory
    ✓ You can also upload files downloaded from /ytdl command to gdrive using `/ytdl gdrive` command.
    ✓ You can also deploy this on your VPS
    ✓ Option to select either video will be uploaded as document or streamable
    ✓ Added /renewme command to clear the downloads which are not deleted automatically.
    ✓ Added support for youtube playlist 😐
    ✓
    
# TO-DO
-   [x] Gdrive file clonning using Gclone

### Credit goes to SpEcHiDe for his Publicleech repo.

## installing...

### The Easy Way

#### STEPS (I did this to avoid the use of same button multiple times)

a)You have to fork this repo at first(Don't know how to🤔, Then google it😐)

b)Find `app.jso`. 🧐

c)Tap on that. 😬

d)Tap to edit and just add `n` at last of name (Don't touch code🤦). ✍️

e)It should look like `app.json`. 🎉

f)Then tap 👇👇

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy) #Revived

Better buy a vps 😐 and follow [this](https://github.com/gautamajay52/TorrentLeech-Gdrive#process-to-run-this-bot-on-vps)

### The Legacy Way
Simply clone the repository and run the main file:

```sh
git clone https://github.com/SpEcHiDe/PublicLeech.git
cd PublicLeech
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
# <Create config.py appropriately>
python3 -m tobrot
```

### an example config.py 👇
```py
from tobrot.sample_config import Config

class Config(Config):
  TG_BOT_TOKEN = ""
  APP_ID = 6
  API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
  AUTH_CHANNEL = [-1001234567890]
```

### Variable Explanations

##### Mandatory Variables

* `TG_BOT_TOKEN`: Create a bot using [@BotFather](https://telegram.dog/BotFather), and get the Telegram API token.

* `APP_ID`
* `API_HASH`: Get these two values from [my.telegram.org/apps](https://my.telegram.org/apps).
  * N.B.: if Telegram is blocked by your ISP, try our [Telegram bot](https://telegram.dog/UseTGXBot) to get the IDs.

* `AUTH_CHANNEL`: Create a Super Group in Telegram, add `@GoogleIMGBot` to the group, and send /id in the chat, to get this value.

* `RCLONE_CONFIG`: Create the rclone config using the rclone.org and read the rclone section for the next.

* `DESTINATION_FOLDER`: Name of your folder in ur respective drive where you want to upload the files using the bot.

* `OWNER_ID`: ID of the bot owner, He/she can be abled to access bot in bot only mode too(private mode).

##### Set Rclone

1. Set Rclone locally by following the official repo : https://rclone.org/docs/
2. Get your `rclone.conf` file.
will look like this
```
[NAME]
type = 
scope =
token =
client_id = 
client_secret = 

```
3. Only copy the config of drive u want to upload file.
4. Copy the entries of `rclone.conf` 
5. Your copied config should look like this:
 ```
type = 
scope =
token =
client_id = 
client_secret = 

and everythin except `[NAME]`

```

6. Paste copied config in `RCLONE_CONFIG`

7. Hit deploy button.
8. Examples:-
<p align="center">

  <img src="https://raw.githubusercontent.com/gautamajay52/TorrentLeech-Gdrive/master/rclone.jpg" width="470" height="150">

</p>

## FAQ

##### Optional Configuration Variables

* `DOWNLOAD_LOCATION`

* `MAX_FILE_SIZE`

* `TG_MAX_FILE_SIZE`

* `FREE_USER_MAX_FILE_SIZE`

* `MAX_TG_SPLIT_FILE_SIZE`

* `CHUNK_SIZE`

* `MAX_MESSAGE_LENGTH`

* `PROCESS_MAX_TIMEOUT`

* `ARIA_TWO_STARTED_PORT`

* `EDIT_SLEEP_TIME_OUT`

* `MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START`

* `FINISHED_PROGRESS_STR`

* `UN_FINISHED_PROGRESS_STR`

* `TG_OFFENSIVE_API`

* `CUSTOM_FILE_NAME`

* `LEECH_COMMAND`

* `YTDL_COMMAND`

* `GLEECH_COMMAND`

* `TELEGRAM_LEECH_COMMAND_G`

* `PYTDL_COMMAND_G`

* `UPLOAD_AS_DOC`: Takes two option True or False. If True file will be uploaded as document. This is for people who wants video files as document instead of streamable.

* `INDEX_LINK`: (Without `/` at last of the link, otherwise u will get error) During creating index, plz fill `Default Root ID` with the id of your `DESTINATION_FOLDER` after creating. Otherwise index will not work properly.
## Available Commands

* `/ytdl`: This command should be used as reply to a [supported link](https://ytdl-org.github.io/youtube-dl/supportedsites.html)

* `/pytdl`: This command will download videos from youtube playlist link and will upload to telegram.

* `/ytdl gdrive`: This will download and upload to your cloud.

* `/pytdl gdrive`: This download youtube playlist and upload to your cloud.

* `/leech`: This command should be used as reply to a magnetic link, a torrent link, or a direct link. [this command will SPAM the chat and send the downloads a seperate files, if there is more than one file, in the specified torrent]

* `/leech archive`: This command should be used as reply to a magnetic link, a torrent link, or a direct link. [This command will create a .tar.gz file of the output directory, and send the files in the chat, splited into PARTS of 1024MiB each, due to Telegram limitations]

* `/gleech`: This command should be used as reply to a magnetic link, a torrent link, or a direct link. And this will download the files from the given link or torrent and will upload to the cloud using rclone.

* `/gleech archive` This command will compress the folder/file and will upload to your cloud.

* `/leech unzip`: This will unzip the .zip file and dupload to telegram.

* `/gleech unzip`: This will unzip the .zip file and upload to cloud.

* `/leech unrar`: This will unrar the .rar file and dupload to telegram.

* `/gleech unrar`: This will unrar the .rar file and upload to cloud.

* `/leech untar`: This will untar the .tar file and upload to telegram.

* `/gleech untar`: This will untar the .tar file and upload to cloud..

* `/tleech`: This will mirror the telegram files to ur respective cloud cloud.

* `/tleech unzip`: This will unzip the .zip telegram file and upload to cloud.

* `/tleech unrar`: This will unrar the .rar telegram file and upload to cloud.

* `/tleech untar`: This will untar the .tar telegram file and upload to cloud.

* `/getsize`: This will give you total size of your destination folder in cloud.

* `/renewme`: This will clear the remains of downloads which are not getting deleted after upload of the file or after /cancel command. 


* [Only work with direct link for now]It is like u can add custom name as prefix of the original file name.
Like if your file name is `gk.txt` uploaded will be what u add in `CUSTOM_FILE_NAME` + `gk.txt`

Only works with direct link.No magnet or torrent.

And also added custom name like...

You have to pass link as 
`www.download.me/gk.txt | new.txt`

the file will be uploaded as `new.txt`.

## Process to run this BOT on VPS

- Clone this repo:
```
git clone https://github.com/gautamajay52/TorrentLeech-Gdrive torrentleech-gdrive
cd torrentleech-gdrive
```

- Install requirements
For Debian based distros
```
sudo apt install python3

sudo snap install docker
```
Install Docker by following the [official docker docs](https://docs.docker.com/engine/install/debian/)

## Setting up config file
```
cp tobrot/g_config.py tobrot/config.py
```
Follow and fill all the required variables that were already filled in the sample config file, but with your details. And you can also fill all other variables according to your need and all those are explained above already.

## Deploying

- Start docker daemon (skip if already running):
```
sudo dockerd
```
- Build Docker image:
```
sudo docker build . -t torrentleech-gdrive
```
- Run the image:
```
sudo docker run torrentleech-gdrive
```


## How to Use?

* send any one of the available command, as a reply to a valid link/magnet/torrent. 👊


## Credits, and Thanks to
* [GautamKumar(me)](https://github.com/gautamajay52/TorrentLeech-Gdrive) 😬
* [SpEcHiDe](https://github.com/SpEcHiDe/PublicLeech) for his wonderful code😚
* [Rclone Team](https://rclone.org) for theirs awesome tool☁️
* [Dan Tès](https://telegram.dog/haskell) for his [Pyrogram Library](https://github.com/pyrogram/pyrogram)
* [Robots](https://telegram.dog/Robots) for their [@UploadBot](https://telegram.dog/UploadBot)
* [@AjeeshNair](https://telegram.dog/AjeeshNait) for his [torrent.ajee.sh](https://torrent.ajee.sh)
* [@gotstc](https://telegram.dog/gotstc), @aryanvikash, [@HasibulKabir](https://telegram.dog/HasibulKabir) for their TORRENT groups
* [![CopyLeft](https://telegra.ph/file/b514ed14d994557a724cb.jpg)](https://telegra.ph/file/fab1017e21c42a5c1e613.mp4 "CopyLeft Credit Video")
