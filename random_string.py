# from clearml import Task

# # create an dataset experiment
# task = Task.init(project_name="pipeline examples", task_name="random string and concat")

# # only create the task, we will actually execute it later
# task.execute_remotely()

# # add and upload local file containing our toy dataset
# task.upload_artifact('dataset', artifact_object=local_iris_pkl)

from clearml import Task

import random
import string
import time
from local_module import test_print

task = Task.init(project_name="pipeline examples", task_name="random string and concat")
# task.execute_remotely()


args = {
    'string_list': '',
}

# store arguments, later we will be able to change them from outside the code
task.connect(args)

random.seed(time.time())

random_char = random.choices(string.ascii_lowercase)[0]
print("Random char : "+random_char)

string_list = args['string_list']+random_char

test_print()

# print("String from this task : "+string_list)

print(string_list)

args['string_list'] = string_list

print('uploading artifacts')
task.upload_artifact('list_of_string', args['string_list'])
print('artifacts of this task:')
print(args['string_list'])

# we are done
print('Task done')