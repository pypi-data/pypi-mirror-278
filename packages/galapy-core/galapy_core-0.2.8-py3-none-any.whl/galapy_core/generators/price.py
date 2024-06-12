import random
from datetime import datetime

import numpy as np
import pandas as pd
import pendulum as pen
from pydantic import BaseModel
from rich import print
# from stochastic.processes.continuous import FractionalBrownianMotion
# import numpy as np
from scipy.linalg import cholesky

class FractionalBrownianMotion:
    def __init__(self, hurst, t=1, num_samples=1000):
        self.hurst = hurst
        self.t = t
        self.num_samples = num_samples
    
    def _autocorrelation(self, k):
        return 0.5 * (abs(k - 1) ** (2 * self.hurst) - 2 * abs(k) ** (2 * self.hurst) + abs(k + 1) ** (2 * self.hurst))
    
    def _covariance_matrix(self):
        cov_matrix = np.zeros((self.num_samples, self.num_samples))
        for i in range(self.num_samples):
            for j in range(i + 1):
                cov_matrix[i, j] = self._autocorrelation(i - j)
                cov_matrix[j, i] = cov_matrix[i, j]
        return cov_matrix
    
    def sample(self):
        cov_matrix = self._covariance_matrix()
        chol_matrix = cholesky(cov_matrix, lower=True)
        normal_samples = np.random.normal(size=self.num_samples)
        fbm_samples = np.dot(chol_matrix, normal_samples)
        return fbm_samples


class PriceGenerator(BaseModel):
    start_time: datetime = pen.now("utc").subtract(years=2)
    end_time: datetime = pen.now("utc")
    num_samples: int = 1000
    hurst: float = 0.7
    mu: float = 1000
    sigma: float = 100
    vol_mu: float = 100000
    vol_sigma: float = 100

    def generate(self):
        timestamps = pd.date_range(
            start=self.start_time, end=self.end_time, periods=self.num_samples
        )
        fbm = FractionalBrownianMotion(hurst=self.hurst, t=1, num_samples=self.num_samples)
        # fbm = FractionalBrownianMotion(hurst=self.hurst, t=1)
        price = fbm.sample()
        price = price * random.gauss(self.mu, self.sigma)
        price = np.abs(price)

        volume = fbm.sample()
        volume = volume * random.gauss(self.vol_mu, self.vol_sigma)
        volume = np.abs(volume)

        return timestamps, price, volume

    def generate_df(self):
        timestamps, s, volume = self.generate()
        frame = pd.DataFrame({"timestamp": timestamps, "price": s, "volume": volume})
        frame = frame.set_index("timestamp")
        frame["timestamp"] = frame.index.copy()
        frame["timestamp"] = pd.to_datetime(frame["timestamp"])
        frame["timestamp"] = frame["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S%z")
        return frame


if __name__ == "__main__":
    price_generator = PriceGenerator()
    df = price_generator.generate_df()

    print(df)
