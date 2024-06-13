import subprocess
from datetime import datetime, timedelta
import time

startTime = time.time()


current_day = datetime.today() - timedelta(days=1)
date_target = current_day.strftime('%d_%m_%Y')

program_list = ['routine_data.py', 'routine_wallet.py', 'routine_wallet_type.py',
                'routine_community.py', 'routine_community_type.py', 'routine_community_reduce.py']

for program in program_list:
    subprocess.call(['python', program, date_target])
    print("Finished: " + program)


executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))