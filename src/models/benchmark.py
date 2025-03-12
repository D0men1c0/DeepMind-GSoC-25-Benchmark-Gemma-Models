import time
import torch
from models.model_loader import ModelLoader
from evaluation.evaluator import Evaluator
from utils.file_manager import save_results
from utils.logger import setup_logger

logger = setup_logger()

class BenchmarkRunner:
    """
    Class to run benchmarking tasks across multiple models and datasets using configurations.
    
    :param config: Dictionary containing configuration for models, tasks, metrics, etc.
    """
    
    def __init__(self, config):
        self.config = config
        self.models = config["models"]
        self.tasks = config["tasks"]
        self.evaluation_metrics = config["evaluation_metrics"]
        self.model_params = config["model_parameters"]
        self.evaluation_params = config["evaluation"]
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.results = {}
    
    def run(self):
        """
        Runs the benchmark across all models and tasks.
        
        :return: Dictionary containing the results for each model/task combination.
        """
        for model_config in self.models:
            model_name = model_config["name"]
            logger.info(f"Running benchmark for model: {model_name}")
            model_loader = ModelLoader(model_name)
            model, tokenizer = model_loader.load()

            for task_config in self.tasks:
                task_name = task_config["name"]
                logger.info(f"Running task {task_name} for model {model_name}...")
                
                # Extract task-specific evaluation metrics
                task_metrics = task_config["evaluation_metrics"]
                
                # Run the task and get predictions and labels (mock in this case)
                predictions, labels = self._run_task(model, tokenizer, task_config)
                
                for metric in task_metrics:
                    evaluator = Evaluator(metric=metric)
                    evaluation_result = evaluator.evaluate(predictions, labels)
                    
                    if model_name not in self.results:
                        self.results[model_name] = {}
                    if task_name not in self.results[model_name]:
                        self.results[model_name][task_name] = {}
                    
                    self.results[model_name][task_name][metric] = evaluation_result

        # Save results and generate reports
        save_results(self.results, self.config["general"]["output_dir"])
        
        return self.results
    
    def _run_task(self, model, tokenizer, task_config):
        """
        Run a specific task (mock implementation for now).
        
        :param model: The loaded model.
        :param tokenizer: The tokenizer for the model.
        :param task_config: Configuration for the task to run (e.g., MMLU, GSM8K).
        :return: Tuple of predictions and labels.
        """
        # Placeholder logic, replace with actual task execution.
        predictions = ["dummy_prediction"] * 10
        labels = ["dummy_label"] * 10
        return predictions, labels