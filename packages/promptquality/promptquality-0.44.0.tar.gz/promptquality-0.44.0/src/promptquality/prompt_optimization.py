from pathlib import Path
from typing import List, Optional
from warnings import warn

from promptquality.helpers import (
    create_project,
    create_prompt_optimization_job,
    create_run,
    create_template,
    upload_dataset,
)
from promptquality.set_config import set_config
from promptquality.types.config import Config
from promptquality.types.prompt_optimization import (
    PromptOptimizationConfiguration,
    PromptOptimizationPayload,
    PromptOptimizationResult,
)
from promptquality.types.run import GetMetricsRequest
from promptquality.utils.name import ts_name

PROMPT_OPTIMIZATION_WARNING = (
    "The optimize_prompt feature is not yet release for public use. "
    "Please be aware that the response will not be useful until the "
    "feature is fully released."
)


def optimize_prompt(
    prompt_optimization_config: PromptOptimizationConfiguration,
    train_dataset: Path,
    val_dataset: Optional[Path] = None,
    project_name: Optional[str] = None,
    run_name: Optional[str] = None,
    config: Optional[Config] = None,
) -> PromptOptimizationPayload:
    """
    Optimize a prompt for a given task.

    This function takes a prompt and a list of evaluation criteria, and optimizes the
    prompt for the given task. The function uses the OpenAI API to generate and evaluate
    prompts, and returns the best prompt based on the evaluation criteria.

    Parameters
    ----------
    prompt_optimization_config : PromptOptimizationConfiguration
        Configuration for the prompt optimization job.
    train_dataset : Path
        Path to the training dataset.
    val_dataset : Optional[Path], optional
        Path to the validation dataset, by default None. If None we will use a subset of the training dataset.
    project_name : Optional[str], optional
        Name of the project, by default None. If None we will generate a name.
    run_name : Optional[str], optional
        Name of the run, by default None. If None we will generate a name.
    config : Optional[Config], optional
        pq config object, by default None. If None we will use the default config.

    Returns
    -------
    PromptOptimizaton
        Object that can be polled to see progress and current prompt.
    """
    warn(PROMPT_OPTIMIZATION_WARNING)
    config = config or set_config()

    project = create_project(project_name, config)
    template_response = create_template(
        prompt_optimization_config.prompt,
        project.id,
        # Use project name as template name if not provided.
        template_name=project.name,
        config=config,
    )
    train_dataset_id = upload_dataset(
        train_dataset,
        project.id,
        template_response.selected_version_id,
        config,
    )
    val_dataset_id = (
        upload_dataset(
            val_dataset,
            project.id,
            template_response.selected_version_id,
            config,
        )
        if val_dataset is not None
        else None
    )
    run_id = create_run(
        project.id,
        run_name=run_name or ts_name(prefix=f"{template_response.name}-v{template_response.selected_version.version}"),
        config=config,
    )

    prompt_optimization_config.validation_dataset_id = val_dataset_id
    job_id = create_prompt_optimization_job(
        prompt_optimization_configuration=prompt_optimization_config,
        project_id=project.id,
        run_id=run_id,
        train_dataset_id=train_dataset_id,
        config=config,
    )

    return PromptOptimizationPayload(
        job_id=job_id,
        project_id=project.id,
        run_id=run_id,
        train_dataset_id=train_dataset_id,
        validation_dataset_id=val_dataset_id,
        config=config,
    )


def fetch_prompt_optimization_result(
    prompt_optimization_payload: PromptOptimizationPayload,
    config: Optional[Config] = None,
) -> List[PromptOptimizationResult]:
    """
    Fetch the prompt optimization results.

    Parameters
    ----------
    prompt_optimization_payload : PromptOptimizationPayload
        Payload object returned by the `optimize_prompt` function.

    Returns
    -------
    List[PromptOptimizationResult]
        List of prompt optimization results.
    """
    warn(PROMPT_OPTIMIZATION_WARNING)
    config = config or set_config()

    project_id = prompt_optimization_payload.project_id
    run_id = prompt_optimization_payload.run_id

    results: List[PromptOptimizationResult] = []
    metrics_request = GetMetricsRequest(project_id=project_id, run_id=run_id)
    all_metrics = config.api_client.get_metrics(metrics_request)
    for metric in all_metrics:
        results.append(
            PromptOptimizationResult(
                key=metric["key"],
                epoch=metric["epoch"],
                **metric["extra"],
            )
        )

    return results
