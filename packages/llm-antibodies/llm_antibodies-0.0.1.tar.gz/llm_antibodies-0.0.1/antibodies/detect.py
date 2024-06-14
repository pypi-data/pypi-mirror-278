class Detect:

    def __init__(self, llm_objective: str, rubrics: list[str]):
        self.objective = llm_objective
        self.rubrics = rubrics
        self.pipeline = lambda x: x == x
    
    def __call__(self, prompt, response = None):

        return self.pipeline(prompt)
