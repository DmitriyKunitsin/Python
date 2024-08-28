name_file = 'test.txt'

try:
    with open(name_file, 'w') as f:
        f.write('Hello, World!')
except Exception as e:
    print(e)
finally:
    f.close()

import os
if os.path.exists(name_file):
    os.remove(name_file)
else:
    print("Файл не создан")