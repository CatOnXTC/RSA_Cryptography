from random import randint, randrange

class RSAgenerator:

    def __init__(self):

        self.max = 9999
        self.min = 1000
        self.p = self.getPrime()
        self.q = self.getPrime(self.p)
        self.n = self.p * self.q
        self.phi = (self.p -1)* (self.q-1)
        self.e = self.getE()
        self.d = self.getD()

    def getPrime(self, x = 0):
        random = randint(self.min, self.max - 1)
        while not self.isPrime(random) or random == x:
            random = randint(self.min, self.max - 1)
        return random

    def nwd(self, a, b):
        while a != b:
            if a > b:
                a -= b
            else:
                b -= a
        return a

    def getE(self):
        e = 2
        result = self.nwd(self.phi, e)
        while result != 1:
            e+=1
            result = self.nwd(self.phi, e)
        return e

    def getD(self):
        d = 1
        result = self.e *d -1
        while result%self.phi!=0:
            d+=1
            result = self.e * d - 1
        return d

    def privateKey(self):
        return (self.d, self.n)

    def publicKey(self):
        return (self.e, self.n)


    def isPrime(self, n):
        if n!=int(n):
            return False
        n=int(n)
        if n==0 or n==1 or n==4 or n==6 or n==8 or n==9:
            return False
    
        if n==2 or n==3 or n==5 or n==7:
            return True
        s = 0
        d = n-1
        while d%2==0:
            d>>=1
            s+=1
        assert(2**s * d == n-1)
    
        def trial_composite(a):
            if pow(a, d, n) == 1:
                return False
            for i in range(s):
                if pow(a, 2**i * d, n) == n-1:
                    return False
            return True  
    
        for i in range(8):
            a = randrange(2, n)
            if trial_composite(a):
                return False
    
        return True  