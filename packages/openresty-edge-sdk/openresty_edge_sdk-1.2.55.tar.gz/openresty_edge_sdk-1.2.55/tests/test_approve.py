# -*- coding: utf-8 -*-
# import io
import sdk_test
import time

def first_address(addrs):
    return addrs.split(' ')[0]

class TestApprove(sdk_test.TestSdk):
    def test_list_candidate_node(self):
        gateway_name = "test-edge-sdk"
        # get gateway clusters
        gateways = self.client.get_all_gateway()
        for gateway in gateways:
            # check if the cluster with test-sdk name exists
            if gateway['name'] == gateway_name:
                # delete if exists
                self.client.del_gateway(gateway['id'])

        # sleep to wait node to appear in the candidate list
        time.sleep(5)

        # get candidate node
        data = self.client.get_all_candidate_node()
        self.assertEqual(type(data), type(list()))

        if len(data) > 0:
            candidate_node = data[0]
            self.assertRegex(candidate_node['mac_address'], '^\w+:\w+:\w+:\w+:\w+:\w+.*$')
            self.assertRegex(candidate_node['hardware_id'], '^\w+$')
            self.assertRegex(candidate_node['internal_ip'], '^\d+\.\d+\.\d+\.\d+.*$')
            self.assertRegex(candidate_node['priv_hash'], '^\w+$')

            # get partitions
            partitions = self.client.get_all_cluster_groups()
            self.assertGreater(len(partitions), 0)
            for partition in partitions:
                self.assertIs(type(partition['id']), type(0))

            # new cluster
            partition_id = partitions[0]['id']
            gateway_id = self.client.add_gateway(gateway_name, partition_id)
            self.assertIs(type(gateway_id), type(0))

            # approve
            ok = self.client.approve_candidate_node(gateway_id, first_address(candidate_node['mac_address']))
            self.assertTrue(ok)

            # delete node
            node = self.client.get_node_by_mac_address(first_address(candidate_node['mac_address']))
            self.assertIs(type(node['id']), type(0))
            ok = self.client.del_node(node['id'])
            self.assertTrue(ok)

            # delete cluster
            ok = self.client.del_gateway(gateway_id)
            self.assertTrue(ok)
