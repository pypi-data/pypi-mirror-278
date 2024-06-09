FROM python:3.10.12-slim
RUN mkdir /notebook
RUN apt-get update
RUN apt-get install -y graphviz
COPY ./docker/server.requirement.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt
WORKDIR /notebook
CMD jupyter kernelgateway --KernelGatewayApp.ip=0.0.0.0 \
    --KernelGatewayApp.port=8888 \
    --KernelGatewayApp.auth_token="${TOKEN}" \
    --JupyterApp.answer_yes=true \
    --JupyterWebsocketPersonality.list_kernels=true

EXPOSE 8888
