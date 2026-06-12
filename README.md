# RGCR Algorithm Comparison

## Overview
This project evaluates and compares the `rgcr` function against two other implementations:
1. `avg_solution`: A naive approach that sorts items based on their average scores.
2. `rgcr_fast`: An optimized and improved version of the original `rgcr` function.

## Performance Evaluation
Based on the generated performance plots, the following observations were made:
* **Metrics:** The `rgcr` algorithm successfully outperforms the naive `avg_solution` in both Recall and Kendall Tau metrics.
* **Runtime:** The `avg_solution` executes faster than the standard `rgcr`. While `avg_solution` remains faster than the optimized `rgcr_fast` as well, the runtime difference between them has been significantly reduced.

## Execution Methodology
To facilitate a proper comparison between the pre-optimization and post-optimization versions of the function, the testing workflow was structured as follows:
* Two distinct virtual environments were established, each configured with a different downloaded version of the project.
* The script was initially executed in the first environment to evaluate the standard `rgcr` and `avg_solution`. 
* Upon switching to the second virtual environment, `rgcr_fast` was appended to the script, and the execution was resumed. 
* This process completed seamlessly without execution conflicts. The testing framework did not redundantly re-evaluate the original `rgcr` function, as its prior execution results were successfully loaded from the `simple_comparison.csv` file.

## Memory Limitations and Edge Cases
During extended executions with large input spaces, a notable constraint was observed: the program terminates due to memory exhaustion rather than reaching a predefined time limit. 

Key observations include:
* When configured with 20 reviewers, the program consistently crashes upon reaching 30,000 items.
* When the input size was explicitly capped at 30,000 items, sporadic crashes still occurred, occasionally failing at approximately 20,000 items.
* Throughout these intensive test runs, the maximum recorded execution time prior to a memory crash was approximately 13 seconds.