New-Item -ItemType File -Name LICENSE
New-Item -ItemType File -Name pyproject.toml
New-Item -ItemType File -Name README.md
New-Item -ItemType File -Name setup.cfg


New-Item -ItemType Directory -Path src/sortingalgorithms
New-Item -ItemType File -Path src/sortingalgorithms/_init_.py
New-Item -ItemType File -Path src/sortingalgorithms/bubble_sort.py
New-Item -ItemType File -Path src/sortingalgorithms/insertion_sort.py
New-Item -ItemType File -Path src/sortingalgorithms/quick_sort.py


New-Item -ItemType Directory -Path tests/sortingalgorithms
New-Item -ItemType File -Path tests/sortingalgorithms/test_bubble_sort.py
New-Item -ItemType File -Path tests/sortingalgorithms/test_insertion_sort.py
New-Item -ItemType File -Path tests/sortingalgorithms/test_quick_sort.py