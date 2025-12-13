import os
import sys
import logging
import grpc
from concurrent import futures
import signal

from server.validation import features_to_dict
from server.inference import ModelRunner

sys.path.insert(0, '/app/ml_grpc_service')
from protos import model_pb2, model_pb2_grpc

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class PredictionServiceServicer(model_pb2_grpc.PredictionServiceServicer):
    """
    gRPC service implementation for ML model predictions.
    """

    def __init__(self):
        """Initialize servicer with model runner."""
        self.model_version = os.getenv('MODEL_VERSION', 'v1.0.0')
        try:
            self.model_runner = ModelRunner()
            logger.info("ModelRunner initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ModelRunner: {e}")
            raise

    def Health(self, request, context):
        """
        Health check endpoint.

        Returns service status and model version.
        """
        logger.info("Health check called")
        return model_pb2.HealthResponse(
            status='ok',
            model_version=self.model_version
        )

    def Predict(self, request, context):
        """
        Prediction endpoint.

        Accepts feature inputs and returns prediction with confidence.
        """
        try:
            logger.info(f"Predict called with {len(request.features)} features")

            feature_dict = features_to_dict(request.features)
            logger.info(f"Features validated: {feature_dict}")

            prediction, confidence = self.model_runner.predict(feature_dict)
            logger.info(f"Prediction: {prediction}, Confidence: {confidence}")

            return model_pb2.PredictResponse(
                prediction=prediction,
                confidence=confidence,
                model_version=self.model_version
            )
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            logger.error(f"Validation error: {e}")
            return model_pb2.PredictResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logger.error(f"Internal error: {e}")
            return model_pb2.PredictResponse()

def serve():
    """Start gRPC server with configuration from environment variables."""
    port = int(os.getenv('PORT', '50051'))
    max_workers = int(os.getenv('MAX_WORKERS', '10'))

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))

    try:
        model_pb2_grpc.add_PredictionServiceServicer_to_server(
            PredictionServiceServicer(), server
        )
        server.add_insecure_port(f'0.0.0.0:{port}')
        logger.info(f"Starting gRPC server on port {port}")
        server.start()
        logger.info("gRPC server started successfully")

        def signal_handler(sig, frame):
            logger.info("Shutting down gRPC server")
            server.stop(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        server.wait_for_termination()
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise

if __name__ == '__main__':
    serve()
