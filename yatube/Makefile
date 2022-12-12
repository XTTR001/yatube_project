WORKDIR = ./  # в переменную WORKDIR записываем название папки с питоновскими файлами, которую будем стилизовать

style:
	black -S -l 79 $(WORKDIR)
	isort $(WORKDIR)
	flake8 $(WORKDIR)
