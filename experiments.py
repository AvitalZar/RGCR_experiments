import experiments_csv
from experiments_csv import multi_plot_results
from rgcr_lite.rgcr_methods import RGCR #venv_1
#from pref_voting.stochastic_methods import RGCR #venv_2
#from pref_voting.grade_profiles import GradeProfile #venv_2
from scipy.stats import kendalltau
import time
import numpy as np



def create_random_voters_list(num_of_voters=5, num_of_cands=20, reviewing_prob=0.3, seed=None):
	np.random.seed(seed)
	candidates = list(range(num_of_cands))
	voters = []
	for _ in range(num_of_voters):
		voter = {}
		val = 0
		for c in candidates:
			if np.random.rand() < reviewing_prob:
				voter[c] = val + np.random.randint(0, 10)+1
				val = voter[c]
		voters.append(voter)
	return voters


def probabilistic_run(func, seed, items, reviewers) -> dict:

	voters = create_random_voters_list(reviewers, items, seed=seed)
	list_of_items = list(range(items))

	start_time = time.time()
	ranking = func(voters, list_of_items)
	end_time = time.time()
	runtime = end_time - start_time


	target_set = set(list_of_items[-5:])
	top_5_ranked = set(ranking[:5])
	recall_5 = len(top_5_ranked.intersection(target_set))/5

	true_order = list_of_items[::-1]
	kendall_tau = kendalltau(ranking, true_order).statistic

	return {
		"ranking": ranking,
		"runtime sec.": runtime,
		"recall_5": recall_5,
		"kendall_tau": kendall_tau
	}


def avg_solution(voters, items):

	keys = {k for d in voters for k in d}
	grouped = {k: [d[k] for d in voters if k in d] for k in keys}
	ranking = sorted(grouped, key=lambda k: sum(grouped[k]) / len(grouped[k]), reverse=True)

	ranking_set = set(ranking)
	ranking += [item for item in items if item not in ranking_set]
	return ranking


def rgcr_solution(voters, items):
	scores = {value for v in voters for value in v.values()}
	gprofile = GradeProfile(voters, list(scores), candidates=items)
	return RGCR(gprofile, curr_cands = items)

def rgcr_fast_solution(voters, items):
	return RGCR(voters, curr_cands = items)

ex = experiments_csv.Experiment("results/", "simple_comparison.csv")

input_range = {
	"seed": range(10),
	"func": [rgcr_solution, 
		avg_solution
		, rgcr_fast_solution
        ],
	"items": range(10, 1000, 100),
	"reviewers": range(20, 100, 20)
}

ex.run_with_time_limit(probabilistic_run, input_range, time_limit=5)


# ==========================================
# Plotting
# ==========================================

csv_path = "results/simple_comparison.csv"

# 1. Runtime plot
multi_plot_results(
    results_csv_file=csv_path, 
    filter={"func": ["rgcr_solution", "avg_solution", "rgcr_fast_solution"], "reviewers": [20,80]}, 
    subplot_rows=1, 
    subplot_cols=2,
    x_field="items", 
    y_field="runtime sec.", 
    z_field="func", 
    subplot_field="reviewers", 
    sharex=True, 
    sharey=True, 
    mean=True, 
    save_to_file="results/plot_runtime.png"
)

# 2. Kendall-Tau Distance plot
multi_plot_results(
    results_csv_file=csv_path, 
    filter={"func": ["rgcr_solution", "avg_solution"], "reviewers": [20,80]}, 
    subplot_rows=1, 
    subplot_cols=2,
    x_field="items", 
    y_field="kendall_tau", 
    z_field="func", 
    subplot_field="reviewers", 
    sharex=True, 
    sharey=True, 
    mean=True, 
    save_to_file="results/plot_kendall_tau.png"
)

# 3. Recall plot
multi_plot_results(
    results_csv_file=csv_path, 
    filter={"func": ["rgcr_solution", "avg_solution"], "reviewers": [20,80]}, 
    subplot_rows=1, 
    subplot_cols=2,
    x_field="items", 
    y_field="recall_5", 
    z_field="func", 
    subplot_field="reviewers", 
    sharex=True, 
    sharey=True, 
    mean=True, 
    save_to_file="results/plot_recall.png"
)

# 4. Runtime rgcr_fast VS rgcr
multi_plot_results(
    results_csv_file=csv_path, 
    filter={"func": ["rgcr_solution", "rgcr_fast_solution"]}, 
    subplot_rows=1, 
    subplot_cols=4,
    x_field="items", 
    y_field="runtime sec.", 
    z_field="func", 
    subplot_field="reviewers", 
    sharex=True, 
    sharey=True, 
    mean=True, 
    save_to_file="results/plot_runtime_fast.png"
)

# 5. Runtime rgcr_fast VS avg
multi_plot_results(
    results_csv_file=csv_path, 
    filter={"func": ["avg_solution", "rgcr_fast_solution"]}, 
    subplot_rows=1, 
    subplot_cols=4,
    x_field="items", 
    y_field="runtime sec.", 
    z_field="func", 
    subplot_field="reviewers", 
    sharex=True, 
    sharey=True, 
    mean=True, 
    save_to_file="results/plot_runtime_fastVSavg.png"
)

def run_fast_rgcr(seed, items, reviewers):
	rev_prob = 1/reviewers
	voters = create_random_voters_list(reviewers, items, seed=seed, reviewing_prob=rev_prob)
	list_of_items = list(range(items))

	start_time = time.time()
	ranking = rgcr_fast_solution(voters, list_of_items)
	end_time = time.time()
	runtime = end_time - start_time

	return {
		"ranking": ranking,
		"runtime": runtime
	}

ex2 = experiments_csv.Experiment("results/", "fast_rgcr_runnings.csv")

input_range = {
	"seed": range(10),
	"reviewers": range(20, 10000, 1000),
	"items": range(10, 300000, 1000)
}

ex2.run_with_time_limit(run_fast_rgcr, input_range, time_limit=60)
