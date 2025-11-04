docker build -t orchestrator:latest ./orchestrator
docker build -t lyrics-service:latest ./lyrics_service
docker build -t hotel-service:latest ./hotel_service
docker build -t car-service:latest ./car_service

# kubectl apply -f .\k8s.yaml
# kubectl get pods 
# kubectl get svc

# Exponer servicio para pruebas con Postman
# kubectl port-forward svc/lyrics-service 5001:5001
