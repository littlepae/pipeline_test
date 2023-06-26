from clearml import Task
from clearml.automation import PipelineController


def pre_execute_callback_example(a_pipeline, a_node, current_param_override):
    # type (PipelineController, PipelineController.Node, dict) -> bool
    print(
        "Cloning Task id={} with parameters: {}".format(
            a_node.base_task_id, current_param_override
        )
    )
    # if we want to skip this node (and subtree of this node) we return False
    # return True to continue DAG execution
    return True


def post_execute_callback_example(a_pipeline, a_node):
    # type (PipelineController, PipelineController.Node) -> None
    print("Completed Task id={}".format(a_node.executed))
    # if we need the actual executed Task: Task.get_task(task_id=a_node.executed)
    return


# Connecting ClearML with the current pipeline,
# from here on everything is logged automatically
pipe = PipelineController(
    name="MMG heatmap pipeline", project="MMG pipeline", version="0.0.1", add_pipeline_tags=False
)

pipe.add_parameter(
    "start_list_of_sting",
    "Sring of this pipeline :"
)

pipe.set_default_execution_queue("default")

pipeline_parameter = pipe.get_parameters()
print(pipeline_parameter["start_list_of_sting"])

pipe.add_step(
    name="stage_1",
    base_task_project="pipeline examples",
    base_task_name="random string and concat",
    parameter_override={"General/string_list": "${pipeline.start_list_of_sting}"},
)

pipe.add_step(
    name="stage_2",
    parents=["stage_1"],
    base_task_project="pipeline examples",
    base_task_name="random string and concat",
    parameter_override={
        "General/string_list": "${stage_1.artifacts.list_of_string.preview}",
    },
)

pipe.add_step(
    name="stage_3",
    parents=["stage_2"],
    base_task_project="pipeline examples",
    base_task_name="random string and concat",
    parameter_override={
        "General/string_list": "${stage_2.artifacts.list_of_string.preview}",
    },
)

pipe.add_step(
    name="stage_4",
    parents=["stage_3"],
    base_task_project="pipeline examples",
    base_task_name="random string and concat",
    parameter_override={
        "General/string_list": "${stage_3.artifacts.list_of_string.preview}",
    },
)

print("${stage_3.artifacts.list_of_string.preview}")

# pipeline_parameter = Task.current_task().artifacts.get()
# print(pipeline_parameter)

# pipe.add_step(
#     name="stage_train",
#     parents=["stage_process"],
#     base_task_project="pipeline examples",
#     base_task_name="Pipeline step 3 train model",
#     parameter_override={"General/dataset_task_id": "${stage_process.id}"},
# )

# pipe.add_step(
#     name="stage_train_branch_1",
#     parents=["stage_train"],
#     base_task_project="pipeline examples",
#     base_task_name="Pipeline step 3 train model",
#     parameter_override={"General/dataset_task_id": "${stage_process.id}"},
#     # execution_queue="For train model only",
# )

# pipe.add_step(
#     name="stage_train_branch_2",
#     parents=["stage_train"],
#     base_task_project="pipeline examples",
#     base_task_name="Pipeline step 3 train model",
#     parameter_override={"General/dataset_task_id": "${stage_process.id}"},
#     # execution_queue="For train model only",
# )

# pipe.add_step(
#     name="stage_train_branch_3",
#     parents=["stage_train"],
#     base_task_project="pipeline examples",
#     base_task_name="Pipeline step 3 train model",
#     parameter_override={"General/dataset_task_id": "${stage_process.id}"},
#     # execution_queue="For train model only",
# )

# pipe.add_step(
#     name="stage_train_branch_4",
#     parents=["stage_train_branch_3"],
#     base_task_project="pipeline examples",
#     base_task_name="Pipeline step 3 train model",
#     parameter_override={"General/dataset_task_id": "${stage_process.id}"},
#     # execution_queue="For train model only",
# )

# pipe.add_step(
#     name="stage_train_end_of_branch",
#     parents=["stage_train_branch_1","stage_train_branch_2","stage_train_branch_4"],
#     base_task_project="pipeline examples",
#     base_task_name="Pipeline step 3 train model",
#     parameter_override={"General/dataset_task_id": "${stage_process.id}"},
# )

# pipe.add_step(
#     name="stage_train_branch2_1",
#     parents=["stage_train_end_of_branch"],
#     base_task_project="pipeline examples",
#     base_task_name="Pipeline step 3 train model",
#     parameter_override={"General/dataset_task_id": "${stage_process.id}"},
# )

# pipe.add_step(
#     name="stage_train_branch2_2",
#     parents=["stage_train_end_of_branch"],
#     base_task_project="pipeline examples",
#     base_task_name="Pipeline step 3 train model",
#     parameter_override={"General/dataset_task_id": "${stage_process.id}"},
# )

# pipe.add_step(
#     name="stage_train_end_of_branch2",
#     parents=["stage_train_branch2_1","stage_train_branch2_2"],
#     base_task_project="pipeline examples",
#     base_task_name="Pipeline step 3 train model",
#     parameter_override={"General/dataset_task_id": "${stage_process.id}"},
# )

# for debugging purposes use local jobs
# pipe.start_locally()

# Starting the pipeline (in the background)
# pipe.start()
pipe.start_locally(run_pipeline_steps_locally=True)

print("Pipeline done")