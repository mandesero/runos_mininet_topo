# Топология Mininet по .gml

Скрипт осуществляет подключение топологии заданной в файле <file_name>.gml к удаленному SDN контроллеру, с дальнейшим удалением линков, заданных в unlinks.txt в строке "N_TOPO + 1"

Список возможных топологий **./GML_files**

Запуск:
```
pipenv shell
pip3 install pygmlparser
pip3 install mininet

sudo python3 topology.py <NUMBER OF TOPO>
```

<NUMBER OF TOPO> - см. в density.txt (нумерация с 0)

