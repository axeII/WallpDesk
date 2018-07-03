

DIR="./wall-desk"

install:
	ifdef PIP3
	@echo $(ccgreen)"[INFO] Installing PIP3"$(ccend)
	@curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
	@sudo python3 get-pip.py --user
endif

ifdef PYTHON3
	@pip3 install numpy --user
	@pip3 install cv2 --user
	@pip3 install opencv-python --user
	@pip3 install astral --user
else
	@echo $(ccred)"[Error] python3.6 is not installed... cannot continue"$(ccend)
endif

build:
	cd $(DIR) && zip -r "../app.zip" * && cd .. 
	echo '#!/usr/local/bin/python3' | cat - app.zip > walld
	chmod +x walld

clean:
	rm app.zip
	rm walld
