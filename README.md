## Advent of code 2022 - Tdarnell

# Advent of code 2022

This is my attempt at the [Advent of Code 2022](https://adventofcode.com/2022) challenges. I'm using this as an opportunity to demonstrate my skills in Python and to learn more about the language. I'm also using this as an opportunity to learn more about git and GitHub.

I intend to complete the challenges first in Python, and then in Julia using it as an opportunity to learn the language from the ground up. 

## Challenges

### Day 1 through 6:

I was playing catch up on these challenges, and still have days 7 - 9 to complete. These were interesting puzzles, and I particularly enjoyed the box stacking puzzle in day 5, though I am sure a much more efficient solution exists utilising regex. 

### Day 7

I got very stuck on this challenge, I think I was overthinking the problem and will return to it fresh. My attempted method was essentially dictionaries within dictionaries to build a filesystem. The recursive nature of this was not easy to handle! 

### Day 8

This one was a tough problem to wrap my head around! I had to look at hints to understand the problem, and then I was able to solve it. My initial thinking did not take into account the ability to see taller trees past the current tallest seen, even if there was a gap of smaller trees in between. 

I am aware that my solution is not the most efficient, if I was allowing myself to use libraries such as numpy I would have had a much easier time of it. 

I wanted to solve this challenge without using any non standard python libraries as far as possible, so I had to think about how to solve it without them. I think my approach of rows and columns was a good one, though I may come back to this and try to improve it using numpy.