from random import randint

def IsPrime (num):
    # Check a number, whether it's prime or not
    # Input :   num (int)
    # Output :  isPrime (1 if it's prime, 0 if it isn't)

    isPrime = 1
    j = 1
    factor = 0
    while (j<=num) and (isPrime):
        if (num%j==0):
            factor = factor + 1
        if (j==num) and ((factor<2) or (factor>2)):
            isPrime = 0
        elif (j<num) and (factor>2):
            isPrime = 0
        j = j+1
    return isPrime

def ValidationPrime (num):
    # Validate a number, is it's prime then it will return the number
    # If it isn't prime, search the nearest prime number (higher the number)
    # Input :   num (int)
    # Output :  num_prime (prime int)

    isPrime = IsPrime(num)
    if (isPrime):
        num_prime = num
        return num_prime
    else:
        # Cari bilangan prima terdekat (iterasi ke atas)
        found = 0
        start = num+1
        while not(found):
            boolPrime =  IsPrime(start)
            if (boolPrime):
                found = 1
                num_prime = start
            start = start+1
        return num_prime

def GenerateKey(p, q):
    # Generate Key e and d for RSA
    # Input :   p and q (prime numbers)
    # Output :  array (e, d, n) --> key pair public-private-n

    n = p*q
    toitent_euler = (p-1)*(q-1)
    e = toitent_euler
    while (e >= toitent_euler):
        e = randint (2, toitent_euler)
        e = ValidationPrime(e)

    found = 0
    k = 1
    while not(found):
        d = (1+k*toitent_euler)/e
        if ((e*int(d))%toitent_euler == 1):
            found = 1    
        k = k+1
    d = int(d)

    arr = [e, d, n]
    return arr

def RandomKey(size):
    # Generate random p, q for RSA (key)
    # Input :  -
    # Output :  array (p, q) 
    
    max = 2**size-1
    min = 2**(size/2)-1

    p = randint (min, max)
    p = ValidationPrime(p)
    q = p 
    while (q == p):
        q = randint (min, max)
        q = ValidationPrime(q)
    
    return [p,q]