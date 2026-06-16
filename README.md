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

## Results
You can see the results in the *.png files in results.

### Examples

1. **Kendall-Tau Distance Comparison**

   <img width="640" height="480" alt="image" src="https://github.com/user-attachments/assets/e798e938-a938-454f-91d3-585161fe717e" />
   
   This graph illustrates the Kendall-Tau distance between the algorithms' outputs and the ground truth. A lower value indicates a solution closer to the target. As shown, the `rgcr` algorithm consistently maintains a distance well below 1,000, whereas the `avg_solution` distance climbs as high as 7,000. These results are averaged over 10 runs using 10 different seeds.

2. **Recall 5**

   <img width="640" height="480" alt="image" src="https://github.com/user-attachments/assets/ad37284f-c76c-482d-aadb-a22c2970d8b8" />
   
   This graph presents the Recall 5 metric, measuring the number of overlapping items between the algorithm's top-5 output and the ground truth. The `rgcr` algorithm achieves a perfect score of 5, successfully identifying the top 5 ranked items (with the exception of the 20-reviewer case, where it remains near 5). In contrast, the `avg_solution` exhibits significantly lower recall. The non-integer values represent an average over 10 runs.

3. **Runtime Comparison**

   <img width="640" height="480" alt="image" src="https://github.com/user-attachments/assets/e73c9d1f-1252-49a4-80e9-63d0b5c06fea" />
   
   This graph compares the execution time of each algorithm. While `avg_solution` remains the fastest, the optimization of `rgcr` into `rgcr_fast` significantly reduces its runtime compared to the original implementation. Despite this improvement, `rgcr_fast` remains slightly slower than the `avg_solution`. Detailed comparisons between the different versions and the baseline are available in the results package.
