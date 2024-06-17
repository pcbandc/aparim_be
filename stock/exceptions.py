class NotEnoughStock(Exception):
    """Raised when stock current balance is less than quantity ordered
    Attributes:
        good - good which caused the error
        warehouse - current warehouse
        time - time as of which the goods sell
        deficiency - current stock deficiency
    """
    def __init__(self, good, warehouse, time, deficiency):
        self.good = good.short_name
        self.deficiency = deficiency
        self.message = f'Ordered amount of {self.good} exceeds current stock in ' \
                       f'{warehouse} warehouse as of {time} by ' \
                       f'{self.deficiency} units'
        super().__init__(self.message)

