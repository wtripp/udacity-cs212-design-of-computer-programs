# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes 
# a string as input and returns the i and j indices that 
# correspond to the beginning and end indices of the longest 
# palindrome in the string. 
#
# Grading Notes:
# 
# You will only be marked correct if your function runs 
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    if not text: return (0, 0)
    
    palindromes = []
    i = 0; j = 2
    for _ in range(len(text) - 1):
        t = text[i:j]
        if text[i] == text[j-1]:
            start, end = expand_palindrome(text, i, j)
            palindromes.append((start, end))
        j += 1
        
        if j > len(text): break
        if text[i] == text[j-1]:
            start, end = expand_palindrome(text, i, j)
            palindromes.append((start, end))
        i += 1
    
    maxlen = 0
    maxpal = ()
    for p in palindromes:
        if abs(p[0] - p[1]) > maxlen:
            maxpal = p
    return maxpal

def expand_palindrome(text, i, j):
    t = text[i:j]
    start = i
    end = j
    while end < len(text):
        start -= 1
        end += 1
        if start < 0:
            break
        if is_palindrome(text[start:end]):
            i = start
            j = end
    return i, j

def is_palindrome(text):
    return text.lower() == text[::-1].lower()

    
def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    return 'tests pass'

print test()