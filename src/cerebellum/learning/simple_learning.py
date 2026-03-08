class SimpleLearning:

    def update(self, memory, experience):

        memory.store(
            "last_experience",
            experience
        )
    