
def customHash(Password):
    hash_value = 0  
    prime = 257
 
    for char in Password:
        ascii_val = ord(char)  # Convert character to ASCII
        hash_value = (hash_value * prime) ^ (ascii_val << 3)  # Bitwise XOR and shift
        hash_value = hash_value % (10**8)  # Keep it within a fixed length
 
    return hex(hash_value)[2:]  # Convert to hex and remove '0x' prefix

def strongPassword(password):
    # Check if the password meets the criteria
    # At least 8 characters long
    if len(password)<=8:
        return False
    hasUpper=False
    hasDigit=False
    hasSpecial=False
    specialChars="!£$%^&*()_-+=[{]}#~'@:;/?.>,<\"|`¬"
    # Check for at least one uppercase letter, one digit, and one special character
    for char in password:
        # Check if the character is uppercase, digit, or special character
        # If it is, set the corresponding flag to True
        if char.isupper():
            hasUpper=True
        elif char.isdigit():
            hasDigit=True
        elif char in specialChars:
            hasSpecial=True
    # If all three flags are True then the password is strong 
    return hasUpper and hasDigit and hasSpecial