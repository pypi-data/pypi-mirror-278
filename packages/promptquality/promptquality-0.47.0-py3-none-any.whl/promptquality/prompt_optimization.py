from pathlib import Path
from typing import List, Optional
from warnings import warn

from pydantic import UUID4

from promptquality.helpers import (
    create_project,
    create_prompt_optimization_job,
    create_run,
    create_template,
    get_job_status,
    upload_dataset,
)
from promptquality.set_config import set_config
from promptquality.types.config import Config
from promptquality.types.prompt_optimization import (
    PromptOptimizationConfiguration,
    PromptOptimizationEpochResult,
    PromptOptimizationResults,
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
) -> UUID4:
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
    job_id: UUID4
        Unique identifier required to fetch Prompt Optimization results.
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

    return job_id


def fetch_prompt_optimization_result(
    job_id: Optional[UUID4] = None,
    config: Optional[Config] = None,
) -> PromptOptimizationResults:
    """
    Fetch the prompt optimization results.

    Parameters
    ----------
    job_id : UUID4
        Unique identifier required to fetch Prompt Optimization results.

    Returns
    -------
    PromptOptimizationResults
        - best_prompt: The best prompt based on the evaluation criteria.
        - train_results: List of epoch results for the training dataset.
            Sorted by epoch ascending.
        - val_results: List of epoch results for the validation dataset.
            Sorted by epoch ascending.
    """
    warn(PROMPT_OPTIMIZATION_WARNING)
    config = config or set_config()
    job_id = job_id or config.current_prompt_optimization_job_id
    if job_id is None:
        raise ValueError("job_id is required.")

    job = get_job_status(job_id, config)
    project_id, run_id = job.project_id, job.run_id

    results: List[PromptOptimizationEpochResult] = []
    metrics_request = GetMetricsRequest(project_id=project_id, run_id=run_id)
    all_metrics = config.api_client.get_metrics(metrics_request)
    for metric in all_metrics:
        results.append(
            PromptOptimizationEpochResult(
                key=metric["key"],
                epoch=metric["epoch"],
                **metric["extra"],
            )
        )

    train_results = [result for result in results if result.key == "prompt_optimization_train"]
    val_results = [result for result in results if result.key == "prompt_optimization_val"]
    best_prompt = max(results, key=lambda x: x.rating).new_prompt
    return PromptOptimizationResults(best_prompt=best_prompt, train_results=train_results, val_results=val_results)
