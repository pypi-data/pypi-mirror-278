import sys

from sae_dashboard.neuronpedia.neuronpedia_runner import (
    NeuronpediaRunner,
    NeuronpediaRunnerConfig,
)

# we use another python script to launch this using subprocess to work around OOM issues - this ensures every batch gets the whole system available memory
# better fix is to investigate and fix the memory issues

SAE_ID = sys.argv[1]
SAE_PATH = sys.argv[2]
OUTPUTS_DIR = sys.argv[3]
SPARSITY_THRESHOLD = int(sys.argv[4])
N_BATCHES_SAMPLE = int(sys.argv[5])
N_PROMPTS_SELECT = int(sys.argv[6])
N_CONTEXT_TOKENS = int(sys.argv[7])
FEATURES_AT_A_TIME = int(sys.argv[8])
START_BATCH_INCLUSIVE = int(sys.argv[9])
END_BATCH_INCLUSIVE = int(sys.argv[10])

cfg = NeuronpediaRunnerConfig(
    sae_id=SAE_ID,
    sae_path=SAE_PATH,
    outputs_dir=OUTPUTS_DIR,
    sparsity_threshold=SPARSITY_THRESHOLD,
    n_batches_to_sample_from=N_BATCHES_SAMPLE,
    n_prompts_to_select=N_PROMPTS_SELECT,
    n_context_tokens=N_CONTEXT_TOKENS if N_CONTEXT_TOKENS != 0 else N_CONTEXT_TOKENS,
    n_features_at_a_time=FEATURES_AT_A_TIME,
    start_batch=START_BATCH_INCLUSIVE,
    end_batch=END_BATCH_INCLUSIVE,
)

runner = NeuronpediaRunner(cfg)
runner.run()
