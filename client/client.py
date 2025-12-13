import grpc
import sys
import os
import logging

from protos import model_pb2, model_pb2_grpc

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

def call_health(host='localhost', port=50051, timeout=5):
    """
    Call Health endpoint.

    Returns HealthResponse or None on error.
    """
    try:
        channel = grpc.insecure_channel(f'{host}:{port}')
        stub = model_pb2_grpc.PredictionServiceStub(channel)
        response = stub.Health(model_pb2.HealthRequest(), timeout=timeout)
        logger.info(f"Health response: status={response.status}, version={response.model_version}")
        return response
    except Exception as e:
        logger.error(f"Health call failed: {e}")
        return None

def call_predict(features_dict=None, host='localhost', port=50051, timeout=5):
    """
    Call Predict endpoint with sample Iris features.

    Args:
        features_dict: Dict of feature_name -> value. If None, uses sample Iris data.

    Returns PredictResponse or None on error.
    """
    if features_dict is None:
        features_dict = {
            'sepal_length': 5.1,
            'sepal_width': 3.5,
            'petal_length': 1.4,
            'petal_width': 0.2
        }

    try:
        channel = grpc.insecure_channel(f'{host}:{port}')
        stub = model_pb2_grpc.PredictionServiceStub(channel)

        features = [model_pb2.Feature(name=k, value=v) for k, v in features_dict.items()]
        request = model_pb2.PredictRequest(features=features)

        response = stub.Predict(request, timeout=timeout)
        logger.info(f"Predict response: prediction={response.prediction}, confidence={response.confidence:.2%}")
        return response
    except Exception as e:
        logger.error(f"Predict call failed: {e}")
        return None

def main():
    """Main entry point - test both endpoints."""
    print("=" * 60)
    print("Testing gRPC ML Service")
    print("=" * 60)

    print("\n1. Testing Health endpoint...")
    health_resp = call_health()
    if health_resp:
        print(f"   Status: {health_resp.status}")
        print(f"   Model Version: {health_resp.model_version}")

    print("\n2. Testing Predict endpoint...")
    predict_resp = call_predict()
    if predict_resp:
        print(f"   Prediction: {predict_resp.prediction}")
        print(f"   Confidence: {predict_resp.confidence:.2%}")
        print(f"   Model Version: {predict_resp.model_version}")

    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
