class Rep_Manager:
    def __init__(self, user, score,):
        self.user = user
        self.score = score

    def sub(self):
        return self.score + 250.0

    def follow(self):
        return self.score + 100.0

    def timeout(self):
        return self.score + -50.0

    def ban(self):
        return self.score + -1000

    def rank(self):
        good = self.score <= 700.0
        ok = self.score == 400.0-699.99
        bad = self.score >= 399.99

