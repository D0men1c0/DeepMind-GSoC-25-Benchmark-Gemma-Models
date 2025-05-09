from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class GeneralConfig(BaseModel):
    experiment_name: str = "Benchmark Experiment"
    output_dir: Path = Path("./benchmarks")
    random_seed: Optional[int] = 42

class ReportingConfig(BaseModel):
    enabled: bool = True
    format: str = "json"
    leaderboard_enabled: bool = False
    generate_visuals: Optional[Dict[str, bool]] = None
    output_dir: Path = Path("./reports")

class AdvancedConfig(BaseModel):
    enable_multi_gpu: bool = False
    use_tpu: bool = False
    distributed_training: bool = False
    batch_size: int = 32
    # Add other advanced params used in TaskHandler (e.g., generate_max_length etc.)
    truncation: bool = True
    padding: bool = True
    generate_max_length: int = 512
    skip_special_tokens: bool = True
    max_new_tokens: int = 50
    num_beams: int = 1
    do_sample: bool = False
    use_cache: bool = False
    clean_up_tokenization_spaces: bool = True

class DatasetConfig(BaseModel):
    name: str
    source_type: str = "hf_hub" # Added default
    config: Optional[str] = None
    split: str = "validation"
    data_dir: Optional[Path] = None
    streaming: bool = True
    loader_args: Dict[str, Any] = Field(default_factory=dict)

class MetricConfig(BaseModel):
    name: str
    options: Dict[str, Any] = Field(default_factory=dict)

class TaskConfig(BaseModel):
    name: str
    type: str # e.g., "classification", "generation"
    description: Optional[str] = None
    datasets: List[DatasetConfig]
    evaluation_metrics: List[MetricConfig]

class ModelConfig(BaseModel):
    name: str
    framework: str
    checkpoint: Optional[str] = None
    variant: Optional[str] = None
    size: Optional[str] = None
    quantization: Optional[str] = None
    offloading: Optional[bool] = None

class ModelParamsConfig(BaseModel):
    # Specific parameters for model loading or inference
    # E.g., generation parameters if not in AdvancedConfig
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    # Add others...

class BenchmarkConfig(BaseModel):
    general: GeneralConfig = Field(default_factory=GeneralConfig)
    tasks: List[TaskConfig]
    models: List[ModelConfig]
    model_parameters: ModelParamsConfig = Field(default_factory=ModelParamsConfig)
    evaluation: Optional[Dict[str, Any]] = None
    reporting: ReportingConfig = Field(default_factory=ReportingConfig)
    advanced: AdvancedConfig = Field(default_factory=AdvancedConfig)