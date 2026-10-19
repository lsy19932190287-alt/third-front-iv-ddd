import numpy, pandas, scipy, statsmodels
print('numpy', numpy.__version__)
print('pandas', pandas.__version__)
print('scipy', scipy.__version__)
print('statsmodels', statsmodels.__version__)
try:
    import linearmodels
    print('linearmodels', linearmodels.__version__)
except ImportError:
    print('linearmodels NOT INSTALLED')