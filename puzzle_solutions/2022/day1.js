const fs = require('fs');

const input = fs.readFileSync('../../inputs/2022/day1.txt', 'utf8').split('\r\n\r\n');

function parseInput(input) {
    // This function will read the input text file and return an array of data
    const parsedInput = input.map((line) => {
        // Do something with each line of input
        line = line.split('\r\n');
        for (let i = 0; i < line.length; i++) {
            line[i] = parseInt(line[i]);
            if (isNaN(line[i])) {
                line.splice(i, 1);
            }
        }
        return line;
    });
    return parsedInput;
}

function getElves(input, number = 1) {
    // This function will read the input text file and return the answer to part 1
    const parsedInput = parseInput(input);
    // console.log(parsedInput);
    // find which elf is carrying the most calories and how many calories they have
    let most = Array(number).fill(0);
    for (let i = 0; i < parsedInput.length; i++) {
        let sum = 0;
        for (let j = 0; j < parsedInput[i].length; j++) {
            sum += parsedInput[i][j];
        }
        // if the sum is bigger than any of the numbers in most, we need to add it to most
        // and remove the smallest number from most
        if (sum > Math.min(...most)) {
            most.push(sum);
            most.sort((a, b) => a - b);
            most.shift();
        }
    }
    // console.log(most);
    return most;
}

let most_calories = getElves(input);
console.log("Part 1: the elf carrying the most calories has " + most_calories + " calories.");
let most_3_calories = getElves(input, 3);
console.log("Part 2: the elves carrying the most calories have " + most_3_calories +
    " calories. Their sum is " + most_3_calories.reduce((a, b) => a + b) + ".");