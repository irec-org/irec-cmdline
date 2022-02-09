<h1 align="center">iRec-cmdline</h1>

## Introduction

iRec-cmdline contains a set of command line interfaces to the iRec library with complete integration to MLflow. This configuration is ready to use and serves as the next-generation environment for interactive recommender system researches.

## Install

Clone the repository:

    git clone https://github.com/irec-org/irec-cmdline/

Install iRec with pip:

    pip install irec
    
## Examples

Under app/ folder is a example of a application using iRec and MLflow, where different experiments can be run with easy using existing recommender systems.

Check this example of a execution using the example application:

    cd app
    metrics=(Hits Precision Recall);
    models=(Random MostPopular UCB ThompsonSampling EGreedy);
    metric_evaluator="IterationsMetricEvaluator"
    bases=("Netflix 10k" "Good Books" "Yahoo Music 10k");
    # run agents
    ./run_agent_best.py --dataset_loaders "${bases[@]}" --agents "${models[@]}"
  
    # evaluate agents using the metrics and metric evaluator defined
    ./eval_agent_best.py --dataset_loaders "${bases[@]}"\
    --agents "${models[@]}" --metrics "${metrics[@]}"\
    --metric_evaluator="$metric_evaluator"

    # print latex table with results and statistical test
    ./print_latex_table_results.py --dataset_loaders "${bases[@]}"\
    --agents "${models[@]}" --metrics "${metrics[@]}"\
    --metric_evaluator="$metric_evaluator"

<!--Also, check these examples using the framework in Python code:-->

<!--:TODO:-->

## Configuration Files

iRec has some configuration files to define an experiment, such as dataset settings, agents, policies and evaluation metrics. Below we present brief examples about each of the files available in this framework.

For more details on configuration files, go to [**configuration_files**](tutorials/configuration_files.ipynb)

[**dataset_loaders.yaml**](app/settings/dataset_loaders.yaml)

This configuration file stores all the configurations related to the bases that will be used during the execution of an experiment.

```yaml
'MovieLens 10M':
  DefaultValidationDatasetLoader:
    dataset_path: ./data/datasets/MovieLens 10M/
    train_size: 0.8
    test_consumes: 1
    crono: False
    random_seed: 0
︙
```

[**dataset_agents.yaml**](app/settings/dataset_agents.yaml)

This configuration file stores the settings of the agents (Recommenders) that will be used in the experiments.

```yaml
'MovieLens 10M':
  LinearUCB:
    SimpleAgent:
      action_selection_policy:
        ASPGreedy: {}
      value_function:
        LinearUCB:
          alpha: 1.0
          item_var: 0.01
          iterations: 20
          num_lat: 20
          stop_criteria: 0.0009
          user_var: 0.01
          var: 0.05
 ︙
```

[**agents_variables.yaml**](app/settings/agents_variables.yaml)

In this configuration file it is possible to define a search field for the variables of each agent, which will be used during the grid search

```yaml
PTS:
  num_lat: [10,20,30,40,50]
  num_particles: linspace(1,10,5)
  var: linspace(0.1,1,10)
  var_u: linspace(0.1,1,10)
  var_v: linspace(0.1,1,10)
```

[**evaluation_policies.yaml**](app/settings/evaluation_policies.yaml)

The evaluation policies are defined in this configuration file. To conduct an experiment, we need to define how the recommendation process will be executed and the user-item interactions. We specify these settings in this file according to the experiment's objectives.

```yaml
Interaction:
  num_interactions: 100
  interaction_size: 1
  save_info: False
︙
```

[**metric_evaluators.yaml**](app/settings/metric_evaluators.yaml)

This file defines the evaluation metrics for an experiment. This file is responsible for providing details on how to assess the interactions performed during the assessment process.

```yaml
UserCumulativeInteractionMetricEvaluator:
  interaction_size: 1
  interactions_to_evaluate:
    - 5
    - 10
    - 20
    - 50
    - 100
  num_interactions: 100
  relevance_evaluator_threshold: 3.999

︙
```

[**defaults.yaml**](app/settings/defaults.yaml)

This configuration file defines the general settings of an experiment. We can define the agents, the base, the policy and the evaluation metric, but also some additional information.

```yaml
agent: LinearUCB
agent_experiment: agent
data_dir: data/
dataset_experiment: dataset
dataset_loader: 'MovieLens 1M'
evaluation_experiment: evaluation
evaluation_policy: Interaction
metric: Hits
metric_evaluator: UserCumulativeInteractionMetricEvaluator
pdf_dir: pdf/
tex_dir: tex/
```
