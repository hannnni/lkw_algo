This directory contains a script for pivot point mode choice and a version file 
which explains its use. The script has two variants, one which uses more intermediate
variables and is more readable, and one which is written in more compact form and saves memory.

Look at Calculate procedures. I set up the example so that I can study how demand reacts to 
changes in PuT travel times. Change e.g. some running times, then run procedures and watch the 
displayed desire lines. What do the procedures do? First I calculate new PuT running times and 
multiply them by -1 to get utilities. Base case utilities for both PrT and PuT are already 
precalculated. Then I call the Python script. I added copious comments to it. You only need to 
modify the very last line, by plugging in the matrix numbers of your own model. With the comment 
you should be able to see which number stands for what. The last step is only for aesthetics:
I subtract the new PuT OD matrix from the old and use the result for the desire lines, so you 
see changes immediately.

What do you need to make this work on your PC?

1. Install the Python add-ons, when the Visum 11.0 setup offers to do so.

2. Open the version file pivotexample.ver.

3. Go to procedures, and change the path to pivot_fast.py or pivot_explained.py (step 3) to your own file locations. 
(These are always stored as absolute paths.)

4. Modify some PuT running times and run procedures.

In general: Read the comments in the script file to understand which parameters you should pass
to the main function.