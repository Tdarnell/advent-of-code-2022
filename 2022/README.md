## Advent of code - Tdarnell

This is my attempt at the [Advent of Code](https://adventofcode.com) annual challenges.

I'm currently using this as an opportunity to demonstrate my skills in Python and to learn more about the language. I'm also using this as an opportunity to learn more about git and GitHub.

I intend to complete the challenges first in Python, and then in Julia using it as an opportunity to learn the language from the ground up.

## [Challenges 2022](puzzle_solutions/2022/)

### Day 1 through 6:

I was playing catch up on these challenges, and still have days 7 - 9 to complete. These were interesting puzzles, and I particularly enjoyed the box stacking puzzle in day 5, though I am sure a much more efficient solution exists utilising regex.

### Day 7

I got very stuck on this challenge, I think I was overthinking the problem and will return to it fresh. My attempted method was essentially dictionaries within dictionaries to build a filesystem. The recursive nature of this was not easy to handle!

19/12/2022 - I restarted the puzzle from scratch and I am very happy with my solution. I used a loop to build the filesystem, and then a while loop to replace the sizes of all subdirectories with the sum of their subdirectories. After part 1 was solved part 2 was nice and simple.

### Day 8

This one was a tough problem to wrap my head around! I had to look at hints to understand the problem, and then I was able to solve it. My initial thinking did not take into account the ability to see taller trees past the current tallest seen, even if there was a gap of smaller trees in between.

I am aware that my solution is not the most efficient, if I was allowing myself to use libraries such as numpy I would have had a much easier time of it.

I wanted to solve this challenge without using any non standard python libraries as far as possible, so I had to think about how to solve it without them. I think my approach of rows and columns was a good one, though I may come back to this and try to improve it using numpy.

I enjoyed creating visual representations of the solution for [part 1](outputs/2022/day8_part1_visible_trees.txt) and [part 2](outputs/2022/day8_part2_visualise.txt).

### Day 9

I have solved this one, and it was a fun challenge, though I did need to resort to looking at hints. My method of simulating rope physics worked for part 1, but not for part 2. I had to look at the hints to understand why my approach was not calculating the correct answer for part 2, and then I was able to solve it.

### Day 10

I found this challenge to be simpler than the last few days, and I was able to solve it without resorting to hints. I did end up taking advice from the subreddit to use unicode characters for the display for part 2, which made it much easier to read.

I liked having a puzzle output that was a [visual representation](outputs/2022/day10_part2_CRT.txt) of the solution, and I think I will try to do this more in the future.

### Day 11

I liked this challenge as I needed to go away and learn something new! I found part 1 to be fairly simple but did not initially know how to approach part 2. After doing some research into managing integer overflow I discovered modulo arithmetic and was able to solve the problem. I enjoyed learning about this new concept and I think I will use it more in the future. [Terminal output with timers](outputs/2022/day11_terminal_output.txt).
