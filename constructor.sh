docker build -t orchestrator:latest ./orchestrator
docker build -t lyrics-service:latest ./lyrics_service
docker build -t composition-service:latest ./composition_service  
docker build -t analytics-service:latest ./analytics_service
docker build -t delete-service:latest ./delete_service
docker build -t digital-delivery-service:latest ./digital_delivery_service
docker build -t vocal-recording-service:latest ./vocal_recording_service
docker build -t mastering-service:latest ./mastering_service
docker build -t emotional-refund-service:latest ./emotional_refund_service


# kubectl apply -f .\k8s.yaml
# kubectl get pods 
# kubectl get svc

# Exponer servicio para pruebas con Postman
# kubectl port-forward svc/lyrics-service 5001:5001
# kubectl port-forward svc/composition-service 5002:5002
# kubectl port-forward svc/mastering-service 5010:5010


# kubectl delete -f .\k8s.yaml
# kubectl get all

# Eliminar imagenes construidas
# docker rmi lyrics-service:latest
# docker rmi composition-service:latest
# docker rmi analytics-service:latest
# docker rmi orchestrator:latest
# docker rmi delete-service:latest
# docker rmi digital-delivery-service:latest
# docker rmi mastering-service:latest