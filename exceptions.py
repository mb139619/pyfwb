

class InvalidPeriodError(Exception):
    
    
    """Exception raised in case of invalid period of scraping."""
    
    
    def __init__(self, period, valid_periods):
        self.period = period
        self.valid_periods = valid_periods
        message = f"Invalid period: '{period}'. You can choose from: {', '.join(valid_periods)}"
        super().__init__(message)