def findMissingPRNs(array):
    missing_values = []
    expected_value = array[0]
    
    for value in array:
        while value != expected_value:
            missing_values.append(expected_value)
            expected_value += 1
        expected_value += 1
        
    return missing_values