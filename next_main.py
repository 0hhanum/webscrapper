from indeed_2 import get_all_jobs as indeed_get_jobs
from stackoverflow import get_jobs as stackoverflow_get_jobs
from save import save_to_file


indeed_jobs = indeed_get_jobs()
so_jobs = stackoverflow_get_jobs()

jobs = so_jobs + indeed_jobs

save_to_file(jobs)



