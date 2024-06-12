from .optimizer import Optimizer
from .cross_validation import CrossValidationEstimator
from .ensemble_optimizer import EnsembleOptimizer
from .fit_methods import fit, available_fit_methods
from .oi import read_summary


__all__ = [
    'fit',
    'read_summary',
    'available_fit_methods',
    'Optimizer',
    'EnsembleOptimizer',
    'CrossValidationEstimator',
]

__project__ = 'trainstation'
__description__ = 'Convenient training of linear models'
__copyright__ = '2024'
__license__ = 'MIT'
__version__ = '1.1'
__maintainer__ = 'trainstation developers group'
__url__ = 'http://trainstation.materialsmodeling.org/'
__status__ = 'Stable'
