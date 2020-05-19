import string
import sys
import random
import logging
from kubernetes import client, config, utils
import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import client, config
from flask import Flask, app, json, request, Response
from kubernetes.client.models.v1_resource_requirements import V1ResourceRequirements
app = Flask(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
config.load_kube_config()
configuration = kubernetes.client.Configuration()

v1 = kubernetes.client.BatchV1Api(kubernetes.client.ApiClient(configuration))

def kube_create_job_object_free(name, container_image, namespace, container_name, env_vars={},resources='None'):
    # Body is the object Body
    body = client.V1Job(api_version="batch/v1", kind="Job")
    # Body needs Metadata
    # Attention: Each JOB must have a different name!
    body.metadata = client.V1ObjectMeta(namespace=namespace, name=name)
    # And a Status
    body.status = client.V1JobStatus()
     # Now we start with the Template...

    resources = client.V1ResourceRequirements(limits={'cpu':'.9'})

    template = client.V1PodTemplate()
    template.template = client.V1PodTemplateSpec()
    # Passing Arguments in Env:
    env_list = []
    for env_name, env_value in env_vars.items():
        env_list.append( client.V1EnvVar(name=env_name, value=env_value) )
    container = client.V1Container(name=container_name, image=container_image, env=env_list,resources=resources)
    template.template.spec = client.V1PodSpec(containers=[container], restart_policy='Never')
    # And finaly we can create our V1JobSpec!
    body.spec = client.V1JobSpec(ttl_seconds_after_finished=600, template=template.template)
    return body

def kube_create_job_free(dataset, namespace, container_name):
    # Create the job definition
    container_image = "prasadi2/mp3:latest"
    name = 'aws-node-' + id_generator()
    body = kube_create_job_object_free(name, container_image, namespace, container_name, env_vars={"DATASET": dataset, "TYPE":'cnn'})
    try:
        api_response = v1.create_namespaced_job(namespace, body, pretty=True)
        print(api_response)
    except ApiException as e:
        print("Exception when calling BatchV1Api->create_namespaced_job: %s\n" % e)
    return

def kube_create_job_object_premium(name, container_image, namespace, container_name, env_vars={}):
    # Body is the object Body
    body = client.V1Job(api_version="batch/v1", kind="Job")
    # Body needs Metadata
    # Attention: Each JOB must have a different name!
    body.metadata = client.V1ObjectMeta(namespace=namespace, name=name)
    # And a Status
    body.status = client.V1JobStatus()
     # Now we start with the Template...

    template = client.V1PodTemplate()
    template.template = client.V1PodTemplateSpec()
    # Passing Arguments in Env:
    env_list = []
    for env_name, env_value in env_vars.items():
        env_list.append( client.V1EnvVar(name=env_name, value=env_value) )
    container = client.V1Container(name=container_name, image=container_image, env=env_list)
    template.template.spec = client.V1PodSpec(containers=[container], restart_policy='Never')
    # And finaly we can create our V1JobSpec!
    body.spec = client.V1JobSpec(ttl_seconds_after_finished=600, template=template.template)
    return body

def kube_create_job_premium(dataset, namespace, container_name):
    # Create the job definition
    container_image = "prasadi2/mp3:latest"
    name = 'aws-node-' + id_generator()
    body = kube_create_job_object_premium(name, container_image, namespace, container_name, env_vars={"DATASET": dataset, "TYPE":'cnn'})
    try:
        api_response = v1.create_namespaced_job(namespace, body, pretty=True)
        print(api_response)
    except ApiException as e:
        print("Exception when calling BatchV1Api->create_namespaced_job: %s\n" % e)
    return

def id_generator(size=12, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/')
def hello_world():
  return 'Hello from Flask!'

@app.route('/img-classification/free', methods=['POST'])
def free():
  print('free method')
  Dict = eval(request.data)
  kube_create_job_free('mnist', 'free-service',"mpthree-container")
  return 'mnist', 200

@app.route('/img-classification/premium', methods=['POST'])
def premium():
  Dict = eval(request.data)
  kube_create_job_premium('kmnist', 'default','premium-container')
  return 'kmnist', 200

@app.route('/config', methods=['GET'])
def config():
    try:

      corev1 = client.CoreV1Api()

      ret = corev1.list_pod_for_all_namespaces(watch=False)
      node_list = []

      for i in ret.items:
          node = {'node':i.spec.node_name,'ip':i.status.pod_ip,'namespace':i.metadata.namespace,'name':i.metadata.name,'status':i.status.phase}
          node_list.append(node)

      result = {"pods":node_list}
      return app.response_class(response = json.dumps(result),status=200, content_type='application/json')
    except Exception as e:
        return("Error" + str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)