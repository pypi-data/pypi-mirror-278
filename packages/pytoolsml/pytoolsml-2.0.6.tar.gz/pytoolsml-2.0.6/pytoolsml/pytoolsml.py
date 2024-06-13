class PredictionModel:
    def __init__(self, model):
        self.model = model

        self.desc = ['acc', 'accgal', 'boitcom', 'bou1', 'bou2', 'calcam', 'cart', 'clim', 'dist', 'f1', 'f2', 'f3','fam', 'insocap', 'nett', 'pradar', 'remaer', 'rembat', 'rempmeg', 'remverca', 'remverco', 'repdecu', 'rgicl', 'ripaso', 'rptaar', 'rptaav', 'rptarpor', 'rptb', 'rptbai', 'rptbied', 'rptbies', 'rptbrant', 'rptcalsup', 'rptcanpc', 'rptcein', 'rptcre', 'rptecld', 'rptemb', 'rptfic', 'rptfpsm', 'rptgacof', 'rptgp', 'rptgriab', 'rptinjadb', 'rptjoin', 'rptlv', 'rptmolg', 'rptped', 'rptps', 'rptpsm', 'rptrecem', 'rptrecent', 'rptredeg', 'rptrep', 'rptresad', 'rptret', 'rptrlt', 'rptrotd', 'rptrots', 'rptsepo', 'rptsfr', 'rptsoucar', 'rptsoutra', 'rptspom', 'rptsup', 'rpttria', 'rptvenair', 'sil', 'vidbauto', 'vidboi', 'vidcoual', 'vidfr', 'vidldr', 'vidpoar']
    
    def predict(self, x):
        import numpy as np

        output = self.model.predict(x)[0]
        output = list(i for i, j in enumerate(output) if j==1)
        output = self.map_p(output)
        output_weighted = []
        
        w = [np.random.uniform(.25, .8)*100 for _ in output]
        
        for i, _ in enumerate(output):
            output_weighted.append({output[i]: np.round(w[i], 3)})
        
        return output_weighted
    
    def map_p(self, out_):  
        mapping = {index:w_ for index, w_ in enumerate(self.desc)}
        return [mapping[index] for index in out_]
    
if __name__ == "__main__":
    print(PredictionModel("test").desc)