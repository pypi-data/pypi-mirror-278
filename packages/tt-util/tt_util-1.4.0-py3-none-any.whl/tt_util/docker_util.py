import docker


class DockerController:
    def __init__(self, base_url: str):
        self.client = docker.DockerClient(base_url=base_url)

    def list_running_containers(self):
        """
        查询所有的容器
        """
        return self.client.containers.list()

    def list_running_object_containers(self):
        """
        查询所有的容器，已List返回
        """
        container_list = []
        for container in self.client.containers.list():
            container_list.append({
                'id': container.short_id,
                'name': container.name,
                'status': container.status,
                'image': container.image,
            })
        return container_list

    def get_container_detailed(self, container_id):
        """
        获取单个容器详细信息
        :param container_id:        容器id或者名称
        :return:                    信息
        """
        container = self.client.containers.get(container_id).attrs
        return {
            "create_time": container['Created'],                                                # 创建时间
            "setup_time": container['State']['StartedAt'],                                      # 启动时间
            "mount": str(container['Mounts']),                                                  # 挂载信息
            "restart_policy": str(container['HostConfig']['RestartPolicy']['Name']),            # 重启策略
            "setup_script": str(container['Args']),                                             # 启动脚本
            "log_conf": str(container['HostConfig']['LogConfig']),                              # 日志参数
            "network_conf": str(container['NetworkSettings']['Ports'])                          # 网卡参数
        }

    def inspect_container(self, container_id):
        """
        获取单个容器
        :param container_id:        容器id或者名称
        """
        return self.client.containers.get(container_id)

    def run_container(self, image, command=None, detach=True):
        """
        启动容器
        """
        return self.client.containers.run(image, command, detach=detach)

    def stop_container(self, container_id):
        """
        暂停容器
        :param container_id:        容器id或者名称
        """
        self.client.containers.get(container_id).stop()

    def remove_container(self, container_id):
        """
        删除容器
        :param container_id:        容器id或者名称
        """
        self.client.containers.get(container_id).remove()

    def close(self):
        """
        关闭当前连接
        """
        self.client.close()

    def test1(self, image):
        """
        关闭当前连接
        """
        return self.client.images.get(image)

    def prune_image(self):
        """
        关闭当前连接
        """
        return self.client.images.prune(filters={'dangling': True})

    def delete_build_cache(self):
        """
        删除构建缓存
        :return: 删除的缓存数量(字节)
        """
        delete_status = self.client.api.prune_builds()
        return delete_status['SpaceReclaimed']