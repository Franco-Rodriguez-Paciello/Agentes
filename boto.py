import boto3

client = boto3.client("bedrock", region_name="us-east-2")

respuesta = client.list_inference_profiles(typeEquals="SYSTEM_DEFINED")

for perfil in respuesta["inferenceProfileSummaries"]:
    pid = perfil["inferenceProfileId"]
    if "anthropic" in pid:                      
        print(pid, "|", perfil["status"])