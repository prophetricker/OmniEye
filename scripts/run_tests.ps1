$ErrorActionPreference = "Stop"

python -m unittest discover -s depth-service\tests -t depth-service
python -m unittest discover -s esp32-firmware\tests -t esp32-firmware
