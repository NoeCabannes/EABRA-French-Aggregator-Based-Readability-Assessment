import numpy as np
from scipy.stats import skew, kurtosis

def compute_aggregators(values):
    """
    Given a list or array of numerical values, computes the 18 aggregators 
    defined by the FABRA architecture.
    """
    if not values:
        # Return a dictionary of NaNs or zeros if there are no values
        keys = ['sum', 'min', 'max', 'len', 'median', 'Q1', 'Q3', '80P', '90P',
                'avg', 'mode', 'var', 'std', 'RSD', 'IQR', 'Dolch', 'skewness', 'kurtosis']
        return {k: 0.0 for k in keys}
    
    arr = np.array(values, dtype=float)
    n = len(arr)
    
    if n == 0:
        return {}

    # Measures of range
    res_sum = np.sum(arr)
    res_min = np.min(arr)
    res_max = np.max(arr)
    res_len = n

    # Measures of separation
    res_median = np.median(arr)
    res_q1 = np.percentile(arr, 25)
    res_q3 = np.percentile(arr, 75)
    res_80p = np.percentile(arr, 80)
    res_90p = np.percentile(arr, 90)

    # Measures of central tendency
    res_avg = np.mean(arr)
    # Numpy doesn't have a mode function, using a simple binning or unique count for mode
    vals, counts = np.unique(arr, return_counts=True)
    res_mode = vals[np.argmax(counts)]

    # Measures of dispersion
    if n > 1:
        res_var = np.var(arr, ddof=1)
        res_std = np.std(arr, ddof=1)
    else:
        res_var = 0.0
        res_std = 0.0

    res_rsd = (res_std / res_avg) if res_avg != 0 else 0.0
    res_iqr = res_q3 - res_q1
    res_dolch = res_90p - res_median

    # Measures of description of the curve
    if n > 2:
        try:
            res_skew = skew(arr, bias=False)
            # if array is constant, skewness might be nan or 0
            if np.isnan(res_skew):
                res_skew = 0.0
        except Exception:
            res_skew = 0.0
            
        try:
            res_kurt = kurtosis(arr, bias=False)
            if np.isnan(res_kurt):
                res_kurt = 0.0
        except Exception:
            res_kurt = 0.0
    else:
        res_skew = 0.0
        res_kurt = 0.0

    return {
        'sum': float(res_sum),
        'min': float(res_min),
        'max': float(res_max),
        'len': float(res_len),
        'median': float(res_median),
        'Q1': float(res_q1),
        'Q3': float(res_q3),
        '80P': float(res_80p),
        '90P': float(res_90p),
        'avg': float(res_avg),
        'mode': float(res_mode),
        'var': float(res_var),
        'std': float(res_std),
        'RSD': float(res_rsd),
        'IQR': float(res_iqr),
        'Dolch': float(res_dolch),
        'skewness': float(res_skew),
        'kurtosis': float(res_kurt)
    }

def aggregate_feature_dict(feature_name, values):
    """
    Applies the aggregators and prefixes the keys with the feature name.
    """
    aggs = compute_aggregators(values)
    return {f"{feature_name}_{k}": v for k, v in aggs.items()}
