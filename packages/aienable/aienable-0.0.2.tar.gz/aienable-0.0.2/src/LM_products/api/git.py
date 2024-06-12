# -*- coding: utf-8 -*-
# Author: Lin WeiCheng
# Description: This is a snippet of the git api for the project.
# Created: 2024-06-03
# Last Modified: 2024-06-03
# version: 1.0


import requests
import base64


class Git_Api:
    def __init__(self, token_url='https://iam-cache-proxy.in-baocloud.cn:26335/v3/auth/tokens'):
        self.token_url = token_url
        self.headers = {'X-Auth-Token': self.get_token(),  # 不需要鉴权可以注释调
                        'Content-type': 'application/json'}

    def get_token(self):
        url = self.token_url  # 初始化为你的认证地址
        data = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "name": "hw_linweichen",  # 最终用户名
                            "password": "eedosgyhlw@123",  # 最终用户登录密码
                            "domain": {
                                "name": "baowugroup"  # 租户名称
                            }
                        }
                    }
                },
                "scope": {
                    "project": {
                        "name": "cn-sh_git"  # 资源集名称
                    }
                }
            }
        }

        response = requests.post(url, json=data, verify=False)

        token = response.headers.get('X-Subject-Token')

        return token

    @staticmethod
    def get_b64_from_image(image_path):
        with open(image_path, 'rb') as f:
            b64_code = base64.b64encode(f.read())
        return b64_code.decode('utf-8')

    def get_dataset(self):
        url = 'https://git.cn-sh.baocloud-ai.cn/v1/da8aedec57cc45aeab440de62c55e122/v-share/iit-ivp/datasets'

        response = requests.get(url=url, headers=self.headers, verify=False)

        return response.json()

    def get_dataset_info(self, dataset_id):
        url = f'https://git.cn-sh.baocloud-ai.cn/v1/da8aedec57cc45aeab440de62c55e122/v-share/iit-ivp/datasets/{dataset_id}'

        response = requests.get(url=url, headers=self.headers, verify=False)

        return response.json()

    def post_sample_data(self, image_path):
        url = 'https://git.cn-sh.baocloud-ai.cn/v1/da8aedec57cc45aeab440de62c55e122/v-share/iit-ivp/sample-data'
        data = {
            "device_id": "123456",  # 设备ID
            "service_id": "e5b4d445-7491-4903-9b5d-7e3c5178ecc6",  # 服务ID同模型id
            "sample_data": "data:image/jpg;base64," + Git_Api.get_b64_from_image(image_path),
            # data:image/jpg;base64,图片base64
            "sample_tips": "test",  # 样本描述
            "annotation": "",  # 标注信息
            "sample_type": "IMAGE_DATA",  # 样本类型，缺省值为IMAGE_DATA，
            "sample_file_name": "test"  # 样本文件名
        }

        response = requests.get(url=url, headers=data, verify=False)

        return response.json()

    def get_models(self):
        url = 'https://git.cn-sh.baocloud-ai.cn/v1/da8aedec57cc45aeab440de62c55e122/v-share/iit-ivp/models?offset=0&limit=10'

        response = requests.get(url=url, headers=self.headers, verify=False)

        return response.json()

    def update_services(self, service_id):
        url = f'https://git.cn-sh.baocloud-ai.cn/v1/da8aedec57cc45aeab440de62c55e122/v-share/iit-ivp/services/{service_id}'
        data = {
            "description": "test",  # 非必选，string, 服务描述
            "env": "",  # 非必选， 键值对， 环境变量
            "ak": "",  # 用户AK
            "sk": "",  # 用户SK
            "port": "",  # 必选， Integer， 服务端口 30000~65000
            "service_status": "RUNNING",
            # 非必选， String， 服务状态 ● running ● stopped ● stopping ● deploying ● failed ● deleting ● deleted ● concerning ● finished ● terminating ● freeze ● succeeded ● unknown ● wait_child ● child_failed
            "service_spec_value": "1",  # 非必选， Integer， 部署的规格数量
            "mount_local_path": "",  # 非必选， String， 边缘部署时的本地存储挂在路径
            "custom_spec": "",  # 非必选， String， 自定义部署规格
        }

        response = requests.get(url=url, headers=data, verify=False)

        return response.json()

    def get_edge_nodes(self):
        url = 'https://git.cn-sh.baocloud-ai.cn/v1/da8aedec57cc45aeab440de62c55e122/v-share/iit-ivp/services/edge-nodes?offset=0&limit=1'

        response = requests.get(url=url, headers=self.headers, verify=False)

        return response.json()

    def get_edge_node_pods(self, node_id):
        url = f'https://git.cn-sh.baocloud-ai.cn/v1/da8aedec57cc45aeab440de62c55e122/v-share/iit-ivp/services/edge-nodes/{node_id}/pods?offset=0&limit=10'

        response = requests.get(url=url, headers=self.headers, verify=False)

        return response.json()

    def deploy_application_version(self, asset_suite_id, application_id, version_id):
        # todo 未完成
        """调用接口部署模型服务
        :param asset_suite_id: 套件ID
        :param application_id: 应用ID
        :param version_id: 版本ID
        :return:
        """
        url = f'https://git.cn-sh.baocloud-ai.cn/v1/da8aedec57cc45aeab440de62c55e122/v-share/iit-ivp/asset-suites/{asset_suite_id}/applications/{application_id}/versions/{version_id}/deploy'
        data = {
            # "service_id": "123456",  # 非必选, String, 服务ID
            "service_name": "test",  # 必选, String, 服务名称
            # "description": "",  # 非必选, String, 服务描述
            "infer_type": "",  # 必选, String, 推理类型
            # "env": "",  # 非必选, 键值对, 环境变量
            # "nodes":"",  # 非必选, Array of strings, 边缘部署方式对应部署节点列表
            "ak": "",  # 用户AK
            "sk": "",  # 用户SK
            # "asset_resource": "",  # 非必选, Object, 资源限制
            "port": "",  # 必选, Integer, 服务端口 30000~65000
            # "cpu_arch": "String",  # 非必选, String, cpu架构
            # "source": "",  # 非必选, String, 指定部署方式
            # "service_spec_value": "",  # 非必选, Integer, 部署的规格数量
            # "mount_local_path": "",  # 非必选, String, 边缘部署时的本地存储挂在路径
            # "request_mode": "",  # 非必选, String, 请求模式
            # "asset_id": "",  # 非必选, String, 资产ID
            # "custom_spec": "",  # 非必选, String, 自定义部署规格
            # "deploy_request": "",  # 非必选, String, 服务部署请求体
            # "python-env": ""  # 非必选, String, python环境
            # "key_type": "aksk"  # 必选, String, 密钥类型  FIX, TEMP
        }
        response = requests.get(url=url, headers=self.headers, verify=False)

        return response.json()


if __name__ == "__main__":
    GA = Git_Api()
    rsp = GA.get_models()
    print(rsp)
