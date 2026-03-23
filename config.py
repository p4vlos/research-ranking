"""
Configuration for Research Area Ranking Tool.
Defines the 10 candidate research directions with keyword queries.
"""

# OpenAlex polite pool email (gets higher rate limits)
MAILTO = "nicolaou.pavlos@ucy.ac.cy"

# Year range
YEARS = [2024, 2025]

# Paper types to include (journals + conference proceedings)
WORK_TYPES = ["article", "proceedings-article"]

# Composite score weights (balanced across all three)
WEIGHTS = {
    "paper_count": 0.33,
    "mean_citations": 0.33,
    "growth_rate": 0.34,
}

# Maximum pages to fetch per query (each page = 200 results)
# Set high for "all available" mode
MAX_PAGES_PER_QUERY = 50  # up to 10,000 per query

# Research area definitions
# Each area has a short name, display name, and 2-3 keyword queries
RESEARCH_AREAS = [
    {
        "id": "foundation_models_ts",
        "name": "Foundation Models for Time Series",
        "short": "Foundation TS",
        "queries": [
            "foundation model time series",
            "pre-trained model time series forecasting",
            "zero-shot time series forecasting",
        ],
    },
    {
        "id": "federated_learning_health",
        "name": "Federated Learning for Wearable Health",
        "short": "FL Wearable",
        "queries": [
            "federated learning wearable health",
            "federated learning health monitoring",
            "privacy-preserving wearable learning",
        ],
    },
    {
        "id": "disease_wearable",
        "name": "Disease-Specific Wearable Forecasting",
        "short": "Disease Wearable",
        "queries": [
            "wearable depression detection",
            "wearable mental health monitoring",
            "wearable cardiovascular monitoring machine learning",
        ],
    },
    {
        "id": "tinyml_ondevice",
        "name": "TinyML / On-Device Learning for Health",
        "short": "TinyML Health",
        "queries": [
            "TinyML health wearable",
            "on-device learning wearable",
            "edge AI wearable health monitoring",
        ],
    },
    {
        "id": "multimodal_health",
        "name": "Multi-Modal Health Fusion",
        "short": "Multimodal Health",
        "queries": [
            "multimodal health sensor fusion wearable",
            "wearable environmental data fusion health",
            "multi-modal wearable health monitoring",
        ],
    },
    {
        "id": "continual_learning",
        "name": "Continual / Lifelong Learning for Wearables",
        "short": "Continual Learn",
        "queries": [
            "continual learning wearable sensor",
            "concept drift health monitoring wearable",
            "online learning wearable health",
        ],
    },
    {
        "id": "heat_health_wearable",
        "name": "Heat & Health from Wearables",
        "short": "Heat Health",
        "queries": [
            "heat stress wearable monitoring",
            "heatwave health wearable",
            "thermal stress health wearable sensor",
        ],
    },
    {
        "id": "signal_accuracy",
        "name": "Improving HR / Physiological Signal Accuracy",
        "short": "Signal Accuracy",
        "queries": [
            "PPG motion artifact removal deep learning",
            "heart rate estimation wearable machine learning",
            "wearable sensor calibration machine learning",
        ],
    },
    {
        "id": "air_pollution_wearable",
        "name": "Air Pollution + Wearable Health",
        "short": "Air Pollution",
        "queries": [
            "air pollution wearable health monitoring",
            "personal air pollution exposure wearable",
            "air quality health wearable sensor",
        ],
    },
    {
        "id": "wearable_data_harmonisation",
        "name": "Consumer Wearable Data Harmonisation",
        "short": "Data Harmonise",
        "queries": [
            "wearable dataset benchmark health",
            "consumer wearable data harmonisation",
            "smartwatch health data pipeline",
        ],
    },
]
