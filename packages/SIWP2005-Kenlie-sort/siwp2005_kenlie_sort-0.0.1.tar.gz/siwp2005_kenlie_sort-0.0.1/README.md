New-Item -ItemType File -Name LICENSE
New-Item -ItemType File -Name pyproject.toml
New-Item -ItemType File -Name README.md
New-Item -ItemType File -Name setup.cfg


New-Item -ItemType Directory -Path src/sortalgos
New-Item -ItemType File -Path src/sortalgos/_init_.py
New-Item -ItemType File -Path src/sortalgos/bubble_sort.py
New-Item -ItemType File -Path src/sortalgos/insertion_sort.py
New-Item -ItemType File -Path src/sortalgos/quick_sort.py


New-Item -ItemType Directory -Path tests/sortalgos
New-Item -ItemType File -Path tests/sortalgos/test_bubble_sort.py
New-Item -ItemType File -Path tests/sortalgos/test_insertion_sort.py
New-Item -ItemType File -Path tests/sortalgos/test_quick_sort.py 