# Function to convert 'G01', 'G02', etc. to 1, 2, etc.
def convert_satlabel_to_prn(value):
    return int(value[1:])


# Function to convert 'G01', 'G02', etc. to 'G'
def convert_satlabel_to_const(value):
    return value[0]

def format_prn(prn):
        # Format PRN with leading zeros if needed based on the maximum length found
        if len(str(prn)) < 2:
            return f"0{prn}"
        else:
            return prn

def missing_prns_before(array):
    missing_prns_array = []
    if not array:
        return missing_prns_array

    array.sort()  # Ensure the array is sorted to handle missing PRNs correctly

    expected_value = 1  # Start checking from 1 assuming PRNs start from 1
    prev_const = convert_satlabel_to_const(array[0])
    
    for sat in array:
        prn = convert_satlabel_to_prn(sat)
        const = convert_satlabel_to_const(sat)
        
        while prn > expected_value:
            # Format the PRN with leading zeros and add it to the list
            missing_prns_array.append(f"{const}{format_prn(expected_value)}")
            expected_value += 1
        
        if const != prev_const:
            expected_value = 1  # Reset expected value for the new constant
            prev_const = const
        
        # Update expected value to the current PRN
        expected_value = prn + 1
    
    return missing_prns_array
    
            
