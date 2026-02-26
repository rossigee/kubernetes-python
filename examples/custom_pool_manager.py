# Copyright 2023 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Example demonstrating the use of a custom pool manager with ApiClient.
This allows advanced configuration of HTTP connections, such as custom SSL settings,
connection pooling, retries, etc.
"""

import urllib3

from kubernetes import client, config


def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()

    # Create a custom pool manager with specific settings
    pool_manager = urllib3.PoolManager(
        num_pools=10,
        maxsize=10,
        retries=urllib3.Retry(total=3, backoff_factor=0.3),
        # Add other custom settings as needed, e.g., SSL certificates
    )

    # Pass the custom pool_manager to ApiClient
    api_client = client.ApiClient(pool_manager=pool_manager)
    k8s_core_v1 = client.CoreV1Api(api_client)

    print("Listing pods with custom pool manager:")
    ret = k8s_core_v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


if __name__ == '__main__':
    main()