
import numpy as np
import scipy.stats as stats

class SESD_tres:
    def __init__(self, data=None, alpha=0.01, maxr=10):
        self.mean = 0
        self.sqsum = 0
        self.alpha = alpha
        self.maxr = maxr
        self.data = data
        self.size = len(data)
        self.mean = np.mean(data)
        self.sqsum = np.sum(np.square(data))

    def test(self, on):
        out = self.data[0]
        self.data = np.append(self.data[1:], on)
        self.mean += -(out - on) / self.size
        self.sqsum += (-out ** 2) + (on ** 2)
        mean_ = self.mean
        sqsum_ = self.sqsum
        size_ = self.size
        data_ = self.data
        sd_ = np.sqrt((sqsum_ - size_ * (mean_ ** 2) + 1e-8) / (size_ - 1))
        ares = np.abs((data_ - mean_) / sd_)
        esd_index = np.argmax(ares)
        esd = ares[esd_index]
        try:
            if esd > self.get_lambda(self.alpha, size_):
                if esd_index == size_ - 1:
                    return True
            else:
                return False
        except:
            return False

        for i in range(2, self.maxr + 1):
            size_ -= 1
            mean_ = ((size_ + 1) * mean_ - data_[esd_index]) / size_
            sqsum_ -= data_[esd_index] ** 2
            sd_ = np.sqrt((sqsum_ - size_ * mean_ ** 2 + 1e-8) / (size_ - 1))

            data_ = np.delete(data_, esd_index)
            ares = np.abs((data_ - mean_) / sd_)
            esd_index = np.argmax(ares)
            esd = ares[esd_index]
            try:
                if esd > self.get_lambda(self.alpha, size_):
                    if esd_index == size_ - 1:
                        return True
                else:
                    return False
            except:
                return False
        return False

    def get_lambda(self, alpha, size):
        t = stats.t.ppf(1 - alpha / (2 * size), size - 2)
        lmbda = t * (size - 1) / np.sqrt((size + t ** 2) * size)
        return lmbda


class SESD_tcha:
    def __init__(self, data=None, alpha=0.01, maxr=10):
        self.mean = 0
        self.sqsum = 0
        self.alpha = alpha
        self.maxr = maxr
        self.data = data
        self.size = len(data)
        self.mean = np.mean(data)
        self.sqsum = np.sum(np.square(data))

    def test(self, on):
        out = self.data[0]
        self.data = np.append(self.data[1:], on)
        self.mean += -(out - on) / self.size
        self.sqsum += (-out**2) + (on**2)
        mean_ = self.mean
        sqsum_ = self.sqsum
        size_ = self.size
        data_ = self.data
        sd_ = np.sqrt((sqsum_ - size_ * (mean_**2) + 1e-8)/(size_-1))
        ares = np.abs((data_-mean_)/sd_)
        esd_index = np.argmax(ares)
        esd = ares[esd_index]
        try:
            if esd > self.get_lambda(self.alpha, size_):
                if esd_index == size_ - 1:
                    return True
            else:
                return False
        except:
            return False
        
        for i in range(2, self.maxr+1):
            size_ -= 1
            mean_ = ((size_+1)*mean_ - data_[esd_index])/size_
            sqsum_ -= data_[esd_index]**2
            sd_ = np.sqrt((sqsum_ - size_ * mean_**2 + 1e-8)/(size_-1))
            data_ = np.delete(data_, esd_index)
            ares = np.abs((data_-mean_)/sd_)
            esd_index = np.argmax(ares)
            esd = ares[esd_index]
            try:
                if esd > self.get_lambda(self.alpha, size_):
                    if esd_index == size_ - 1:
                        return True
                else:
                    return False
            except:
                return False
        return False

    def get_lambda(self, alpha, size):
        t = stats.t.ppf(1 - alpha / (2 * size), size - 2)
        lmbda = t * (size - 1) / np.sqrt((size + t ** 2) * size)
        return lmbda

