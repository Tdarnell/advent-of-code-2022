import sys
sys.path.append(".")
import utils
import re

# Using functions from https://stackoverflow.com/a/9558001 to evaluate mathmatical expressions
# as python built-in eval() is not a good idea!
import ast
import operator as op

# supported operators
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}

def eval_expr(expr):
    """
    >>> eval_expr('2^6')
    4
    >>> eval_expr('2**6')
    64
    >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
    -5.0
    """
    return eval_(ast.parse(expr, mode='eval').body)

def eval_(node):
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)

def input_formatter(input_txt: str):
    # This will take the input, split it by \n\n to get the monkeys
    # Then loop through the monkeys and get their starting items, operation, and test
    input_txt = input_txt.strip()
    monkeys_raw = input_txt.split("\n\n")
    monkeys = {}
    for monkey in monkeys_raw:
        # We are going to use regex to parse the monkey's input
        # First, get the monkey's number
        monkey_num = int(re.search(r"Monkey (\d+):", monkey).group(1))
        # Now lets get the starting items, and split them into a list
        monkey_items = re.search(r"Starting items: (.+)\n", monkey).group(1)
        # split the items into a list
        monkey_items = [int(i) for i in monkey_items.split(", ")]
        operation = re.search(r"Operation: new = (.+)\n", monkey).group(1)
        test = re.search(r"Test: (.+)\n", monkey).group(1)
        if_true = re.search(r"If true: throw to monkey (\d+)", monkey).group(1)
        if_false = re.search(r"If false: throw to monkey (\d+)", monkey).group(1)
        monkeys[monkey_num] = {
            "number": monkey_num,
            "items": monkey_items,
            "operation": operation,
            "test": test,
            "if_true": if_true,
            "if_false": if_false,
            "num_inspections": 0,
        }
    return monkeys

def monkey_business(monkeys: dict, monkey_num: int):
    """
    This function loops through a monkeys items, applies the operation, and tests the item
    """
    if len(monkeys) == 0:
        raise ValueError("No monkeys found!")
    if monkey_num not in monkeys:
        raise ValueError(f"Monkey {monkey_num} not found!")
    monkey = monkeys[monkey_num]
    if not isinstance(monkey, dict):
        raise TypeError("Monkey must be a dictionary!")
    if len(monkey) == 0:
        raise ValueError("No monkey found!")
    # Check if "items", "operation", "test", "if_true", and "if_false" are in the monkey
    if not all([i in monkey for i in ["items", "operation", "test", "if_true", "if_false"]]):
        raise ValueError("Monkey is missing one or more of the following: items, operation, test, if_true, if_false")
    print(f"Monkey {monkey_num} is inspecting {len(monkey['items'])} items")
    print(f"Monkey {monkey_num} starts with {monkey['items']}")
    items_ = monkey["items"].copy()
    num_inspections = len(items_)
    for item_worry in items_:
        # Apply the operation
        new_item_worry = eval_expr(monkey["operation"].replace("old", str(item_worry)))
        # After a monkey inspect an item, but before it tests your worru level
        # divide the new_item_worry by 3, and round down to the nearest integer
        new_item_worry = int(new_item_worry // 3)
        print(f"Monkey {monkey_num} applied the operation to {item_worry} and got {new_item_worry} (rounded down)")
        # Now we need to evalue the test, these seem to always be "divisible by X"
        # so for now I will assume that is the case, if that changes in part 2, I will update this
        test_val = int(monkey["test"].split(" ")[-1])
        if new_item_worry % test_val == 0:
            print(f"Monkey {monkey_num} tested {new_item_worry} and it was divisible by {test_val} (true) so it will throw to Monkey {monkey['if_true']}")
            # If true, throw to the monkey in "if_true"
            monkeys[int(monkey["if_true"])]["items"].append(new_item_worry)
            monkeys[monkey_num]["items"].remove(item_worry)
        else:
            print(f"Monkey {monkey_num} tested {new_item_worry} and it was not divisible by {test_val} (false) so it will throw to Monkey {monkey['if_false']}")
            # If false, throw to the monkey in "if_false"
            monkeys[int(monkey["if_false"])]["items"].append(new_item_worry)
            monkeys[monkey_num]["items"].remove(item_worry)
        print(f"Monkey {monkey_num} threw {new_item_worry} to Monkey {monkey['if_true'] if new_item_worry % test_val == 0 else monkey['if_false']}")
    monkeys[monkey_num]["num_inspections"] += num_inspections
    return monkeys


def get_most_active_monkeys(monkeys: dict, num: int = 2):
    # Will sort the monkeys dict by monkey["num_inspections"] and return the top num
    monkey_order = [i for i in sorted(monkeys, key=lambda x: monkeys[x]["num_inspections"], reverse=True) if monkeys[i]["num_inspections"] > 0]
    return monkey_order[:num]
    

    
if __name__ == "__main__":
    """
    Input is in the form:
    Monkey 0:
    Starting items: 78, 53, 89, 51, 52, 59, 58, 85
    Operation: new = old * 3
    Test: divisible by 5
        If true: throw to monkey 2
        If false: throw to monkey 7

    Monkey 1: ...
    """
    input_file = utils.get_input(day=11, year=2022)
    with open(input_file, "r") as f:
        input_text = f.read()
        monkeys = input_formatter(input_txt=input_text)
        for rounds in range(20):
            print(f"Round ({rounds + 1} of 20))")
            for monkey_num in monkeys.keys():
                monkeys = monkey_business(monkeys, monkey_num)
            print(f"After round {rounds + 1} the monkeys have:")
            for monkey_num in monkeys.keys():
                print(f"Monkey {monkey_num} has {len(monkeys[monkey_num]['items'])} items")
                print(f"Monkey {monkey_num} has {monkeys[monkey_num]['items']}")
        most_active = get_most_active_monkeys(monkeys)
        monkey_business_level = 1
        for i,m in enumerate(most_active, 1):
            print(f"Monkey {m} was the {i} most active with {monkeys[m]['num_inspections']} inspections")
            monkey_business_level *= monkeys[m]["num_inspections"]
        print(f"The Monkey Business Level is {monkey_business_level}")