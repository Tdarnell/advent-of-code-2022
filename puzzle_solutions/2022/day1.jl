"""
This is my first Julia script, and it's a puzzle solution!
"""


# Load the input data
input = open("inputs/2022/day1.txt", "r");
split_input = split(read(input, String), "\r\n");

# Part 1

function sum_elves(input)
    sums = []
    sum = 0
    for i in eachindex(input)
        if input[i] == ""
            # println("Found a blank line at index $i")
            push!(sums, sum)
            sum = 0
        else
            sum = sum + parse(Int, input[i])
        end
    end
    # println("The sum of all the numbers is $(sum(sums))")
    return sums    
end

function find_highest_sum(sums, num = 1)
    highest_sums = Array{Int}(undef, num)
    for i in 1:num
        highest_sums[i] = maximum(sums)
        deleteat!(sums, findall(x -> x == maximum(sums), sums))
    end
    return highest_sums
end


sums = sum_elves(split_input)
highest_sum = find_highest_sum(sums, 3)
println("The highest sum is $highest_sum")

close(input);