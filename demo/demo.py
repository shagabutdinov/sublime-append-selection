# -----------------------
# case 1, select forward
# -----------------------
test = call_function(test1, test2)
if test == None:
  return

test_type, test_value = test
if test_type == "call_test":
  print(test)

# -----------------------
# case 2, select backward
# -----------------------

test = call_function(test1, test2)
if test == None:
  return

test_type, test_value = test
if test_type == "call_test":
  print(test, test_value)

# -----------------------
# case 3, select word
# -----------------------

test = call_function(result1, result2)
if test == None:
  return

result_type, result_value = test
if result_type == "call_result":
  print(test)