from typing import Dict

def features_to_dict(features) -> Dict[str, float]:
    """
    Convert protobuf Feature objects to dictionary with validation.
    
    Validates:
    - No duplicate feature names
    - No empty feature names
    - Minimum one feature exists
    
    Raises:
    - ValueError for validation failures
    """
    if not features:
        raise ValueError("At least one feature is required")
    
    feature_dict = {}
    seen_names = set()
    
    for feature in features:
        if not feature.name or feature.name.strip() == "":
            raise ValueError("Feature names cannot be empty")
        
        if feature.name in seen_names:
            raise ValueError(f"Duplicate feature name: {feature.name}")
        
        seen_names.add(feature.name)
        feature_dict[feature.name] = feature.value
    
    return feature_dict