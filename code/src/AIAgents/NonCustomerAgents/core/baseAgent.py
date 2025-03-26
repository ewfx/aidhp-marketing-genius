from abc import ABC, abstractmethod
import logging
from typing import Any, Dict
class BaseAgent(ABC):
    """
    Abstract base class for all AI agents
    Provides a standardized interface for agent operations
    """
    def init(self,name: str,logger: logging.Logger = None):
        """
        Initialize the base agent
        Args:
        name (str): Name of the agent
        logger (logging.Logger, optional): Logger instance
        """
        self.name = name
        self.logger = logger or self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """
        Set up a default logger for the agent
        
        Returns:
            logging.Logger: Configured logger
        """
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)
        
        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        ch.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(ch)
        
        return logger

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize agent resources, connections, etc.
        Must be implemented by subclasses
        """
        pass

    @abstractmethod
    def run(self, input_data: Any) -> Any:
        """
        Main method to execute the agent's primary task
        
        Args:
            input_data (Any): Input data for processing
        
        Returns:
            Any: Processing result
        """
        pass

    def log_action(self, 
                level: str, 
                message: str, 
                extra: Dict = None):
        """
        Log agent actions with optional extra details
        
        Args:
            level (str): Logging level (info, error, warning)
            message (str): Log message
            extra (Dict, optional): Additional context
        """
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        
        if extra:
            log_method(f"{message} - Context: {extra}")
        else:
            log_method(message)