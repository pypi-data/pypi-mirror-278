class PredictionModel:
    def __init__(self, model):
        self.model = model

        from os import chdir
        from os.path import realpath, dirname
        chdir(dirname(realpath(__file__)))

        with open("./file.txt", "r") as file:
            self.desc = file.read().splitlines()
    
    def predict(self, x):
        import numpy as np

        output = self.model.predict(x)[0]
        output = list(i for i, j in enumerate(output) if j==1)
        output = self.map_p(output)
        output_weighted = []
        
        w = [np.random.uniform(.3, .8)*100 for _ in output]
        
        for i, _ in enumerate(output):
            output_weighted.append({output[i]: np.round(w[i], 3)})
        
        return output_weighted
    
    def map_p(self, out_):  
        mapping = {index:w_ for index, w_ in enumerate(self.desc)}
        return [mapping[index] for index in out_]
    
if __name__ == "__main__":
    print(PredictionModel("test").desc)