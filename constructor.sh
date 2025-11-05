docker build -t orchestrator:latest ./orchestrator
docker build -t lyrics-service:latest ./lyrics_service
docker build -t hotel-service:latest ./hotel_service
docker build -t car-service:latest ./car_service
docker build -t mastering-service:latest ./mastering_service


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
# docker rmi mastering-service:latest
# docker rmi hotel-service:latest
# docker rmi car-service:latest
# docker rmi orchestrator:latest