# -*- coding: utf-8 -*-            
# @Author : buyfakett
# @Time : 2024/6/7 上午11:54
import logging
from typing import Union

from confluent_kafka import Producer, Consumer, KafkaError


class KafkaManager:
    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers

    def produce(self, topic: str, value: Union[str, int, bytes], key: Union[str, int, bytes] = None):
        """
        生产消息到Kafka
        :param topic: topic
        :param value: value
        :param key: key
        """
        p = Producer({'bootstrap.servers': self.bootstrap_servers})

        def delivery_report(err, msg):
            """对生成的每个消息调用一次，以指示传递结果。"""
            if err is not None:
                logging.error(f'消息传递失败: {err}')
            else:
                logging.info(f'消息已送达 {msg.topic()} [{msg.partition()}]')

        p.produce(topic, key=key, value=value, callback=delivery_report)
        p.flush()

    def consume(self, topic: str, group_id: str, num_messages: int = 1, timeout: float = 1.0):
        """
        从Kafka消费指定数量的消息，并返回这些消息
        :param topic: topic
        :param group_id: 消费者
        :param num_messages: 消费几条数据
        :param timeout: 超时时间
        :return:
        """
        c = Consumer({
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })

        c.subscribe([topic])
        messages = []

        try:
            while len(messages) < num_messages:
                msg = c.poll(timeout)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logging.info('已到达分区的末尾')
                    else:
                        logging.error(f'消费错误: {msg.error()}')
                else:
                    messages.append(msg.value().decode('utf-8'))
                    if len(messages) >= num_messages:
                        break
        except Exception as e:
            print(f'消费错误: {e}')
        finally:
            c.close()

        return messages
