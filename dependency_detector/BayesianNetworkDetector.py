"""Bayesian‑network detector using pgmpy on a Spark DataFrame.
* Converts the Spark DataFrame to pandas (or a sampled subset).
* Learns the structure with Hill Climb search + BIC score.
* Estimates CPDs with Maximum Likelihood.* Exposes `.model_` (pgmpy model) and a pandas DataFrame of edges.
"""
from dependency_detector.baseDetector import BaseDependencyDetector
from dependency_detector import logger
from pyspark.sql import DataFrame as SparkDF
from typing import Optional, List

class BayesianNetworkDetector(BaseDependencyDetector):
    
    def __init__(
        self,
        data: SparkDF,
        sample_fraction: float = 1.0,
        max_parents: int = 3):
        
        super().__init__(data)
        self.sample_fraction = sample_fraction
        self.max_parents = max_parents
        self.model_ = None
        self.edges_: Optional[List] = None
        
    def _to_pandas(self):
        if self.sample_fraction < 1.0:
            logger.info("Sampling %.0f%% of data for BN structure learning", self.sample_fraction*100)
            pdf = self.data.sample(withReplacement=False, fraction=self.sample_fraction).toPandas()
        else:
            pdf = self.data.toPandas()
        return pdf
    
    def compute_dependencies(self):
        from pgmpy.estimators import HillClimbSearch, MaximumLikelihoodEstimator
        try:
            from pgmpy.estimators import BDeu as BIC  # pgmpy<=0.1.23
        except ImportError:  # pgmpy >=1.0 removes BicScore from __init__
            try:
                from pgmpy.estimators.BIC import BIC  # type: ignore
            except ImportError: # Fallback to BDeuScore if BIC not available
                from pgmpy.estimators import BDeu as BIC  # type: ignore
                logger.warning("BicScore not found; using BDeuScore instead")
                
        pdf = self._to_pandas()
        logger.info("Learning BN structure on dataframe with shape %s", pdf.shape)
        est = HillClimbSearch(pdf)
        best_model = est.estimate(scoring_method=BIC(pdf), max_indegree=self.max_parents)
        # Parameter learning
        best_model.fit(pdf, estimator=MaximumLikelihoodEstimator)
        self.model_ = best_model
        # Create edge DataFrame
        
        import pandas as pd
        self.edges_ = pd.DataFrame(best_model.edges(), columns=["Parent", "Child"])
        logger.info("BN structure learning finished – %d edges", len(self.edges_))
        
        return self.edges_
    
    def visualize(self, out_path: str = "bayes_net.png"):
        if self.model_ is None:
            raise ValueError("Run compute_dependencies() first")
        
        import matplotlib.pyplot as plt
        import networkx as nx
        
        g = nx.DiGraph()
        g.add_edges_from(self.model_.edges())
        plt.figure(figsize=(8,6))
        nx.draw_networkx(g, with_labels=True, arrows=True, node_size=1500, font_size=10)
        plt.title("Bayesian Network Structure")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(out_path)
        
        logger.info("Saved BN graph → %s", out_path)