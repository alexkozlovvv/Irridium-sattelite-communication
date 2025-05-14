# Irridium sattelite communication
Проект с помощью которого исследовался метод проактивного отслеживания спутников с использованием библиотеки Skyfield. 
Основная цель метода - сокращение энергопотребления в условиях отдаленной местности, где основным видом коммуникации является
спутниковая связь.


### App usage:
* `SBD_spam_binary.py` – for rapidly sending binary data to satellite
* `SBD_spam_text.py` – for rapidly sending text data to satellite
* `send_binary_with_schedule.py` – for sending binary data using satellites schedule
* `send_with_schedule.py` – for sending text data using satellites schedule
* `skyfield_prediction.py` – generates satellite schedule

### Structures:
* `satellites_skyfield.py` – Satellite class based on skyfield library
* `IridiumModem.py` – Modem class with low-level communication
* `read_config.py` – for config file reading
* `message_generate.py` – for sending message generation

### Config files
* `config.yaml` – here written all configs for satellite prediction and message send

### CI/CD scripts
* `source raspberry_pull.sh` – pulls new version from repo. Use first argument `branch_name` for pulling different branch (`master` by default)
* `source raspberry_install_and_update.sh` – same as pull, but additionally install all system requirements

## How to send messages to satellite manually:
1) `AT` returns `OK` if everything connected and works fine
2) `AT+SBDWT=<YOUR_MESSAGE_UP_TO_120_BYTES>` returns `OK` if message buffered and ready for send
3) `AT+SBDI` returns `SBDI: 2, <SEND_NUM>, 2, 0, 0, 0` if there is error in send and `SBDI: 1, 4, 0, 0, 0, 0` if message sent successfully

### Log file example
* Example log file is `example.log`