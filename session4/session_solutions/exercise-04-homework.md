# Session 4 Homework

## Video

Link: https://www.youtube.com/watch?v=XKu_SEDAykw

## My understanding of the problem

Requirements: There are a sequence of random numbers a pair should add up to a given sum (i.e. 8)
If a pair adds up or does not add up note this

Rules: you can store the numbers in an array, or sort them in any order
Cannot re-use the same index, all numbers are int data types
- or + integers
take a pair and compare to all previous numbers before it, use a hash table

## My thought process

1. Binary Search Tree: At first I thought to iterate through and compare all combinations of numbers by finding the start, end, of the sequence of numbers
   but as mentioned in the video this is sequential and might miss potential pairs
2. Hash table: Then it could be possible to use a hash table to look up each number in the sequence and find out what number is required to sum up to the target num
   So in this way a hash table can be built one sequence number at a time, until we find a matching pair
3. But instead we could leave the sequence unsorted, start with a pair fand group largest numbers and smallest
   Then use the pair to find all the numbers previous to the current number (store in memory) to find pairs that sum up

## My Python solution

```python

def loc_summed_pairs(arr, target):
    setofnums = set()
    n         = len(arr)

    #initialise vars for left and right of arrand var for setofnumbers to process, finally var to hold append to results arr
    setofnums = set()
    left      = 0
    right     = len(arr) -1

    # compare left of arr to right to order nums low to high
    while left < right:
        total = arr[left] + arr[right]

        if total == target:
            #Use pointer search
            left += 1
            right -= 1
            return arr[left], arr[right]

        elif total < target:
            left += 1

        else:
            #Use hash table
            for i in arr:
                complement = target - i
                if complement in setofnums:
                   yield complement, i
                setofnums.add(i)
            return

# function call
nums = [1,2,4,4,5,6,7,8]
target_sum = 11

print(list(loc_summed_pairs(nums, target_sum)))

```

## Complexity
This depends on the approach taken at first with a nested array the time complexity was 0(n) and space 0(log n) - if also using a sorted array

- Time complexity: 0(n)
- Space complexity: 0(1)

## Comparison with the video solution

What was similar?

Initially I had the idea from the nested loops hint in the video to use a brute force method to iterate over all sequences with a nested loop

What was different?

I then attempted the nested loop on my own by using an array initialisation and two loops (parent --> child) i,j --> but this was too performance heavy and eventually ended by updating the solution to also use a BST method, eventual changes made to use n+1, then appending the array, which was a big mistake, and led to an infinite loop by iterating over the array again (dangerous)
I needed help to think through the problem, as I was not thinking in terms of efficiency and best time/space complexity outcome.
It taught me to prioritise solutions with the best time/space complexity, and to think out loud and iterate a solution by refactoring


## Interview reflection

What would you do better next time when explaining your thinking?

## I would approach the problem with time/space objectives as a priority, and learn the different methods that python uses: i.e. BST, linear approach or sorting methods like bubble sort or insert sort
## or just unsorted with a set pair as a starting point which I would not have thought of...
## (i.e. to solve the actual problem in the most immediate efficient way).
## Unfortunately I did not have the requisite knowledge to think the solution through on my own, so I recognised this gap in my thinking...I am learning
