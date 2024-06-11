# -*- coding: utf-8 -*-
# import io
import os
import random
import sdk_test
from edge2client.constants import OFF, ON

CURPATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class TestRule(sdk_test.TestSdk):
    def test_waf(self):
        condition = [{'var': 'uri', 'op': 'prefix', 'val': '/foo'}]
        waf_rule = {'rule_sets': [7,8,9,10,11,12,13,14,15,16,17],
                    'action': '403 Forbidden', 'threshold': 'low'}
        rule_id = self.client.new_rule(condition=condition,
                                       waf=waf_rule, last=True)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        waf_rule = {'rule_sets': [7,8,9,10,11,12,13,14,15,16,17],
                    'action': '403 Forbidden', 'threshold': 'high'}
        ok = self.client.put_rule(rule_id=rule_id, waf=waf_rule,
                                  condition=condition)
        self.assertTrue(ok)

        data = self.client.get_rule(rule_id)
        self.assertIn(7, data['waf']['rule_sets'])
        self.assertIn(8, data['waf']['rule_sets'])
        self.assertEqual(data['waf']['threshold_score'], 1000)

        waf_rule = {'rule_sets': [7,8,9,10,11,12,13,14,15,16,17],
                    'action': 'log'}
        ok = self.client.put_rule(rule_id=rule_id, waf=waf_rule,
                                  condition=condition)
        self.assertTrue(ok)

        waf_rule = {'rule_sets': [7,8,9,10,11,12,13,14,15,16,17],
                    'action': 'edge-captcha', 'threshold': 'low',
                    'clearance': 60}
        ok = self.client.put_rule(rule_id=rule_id, waf=waf_rule,
                                  condition=condition)
        self.assertTrue(ok)

        waf_rule = {'rule_sets': [7,8,9,10,11,12,13,14,15,16,17],
                    'action': 'redirect', 'threshold': 'medium',
                    'redirect_url': 'https://openrsty.org'}
        ok = self.client.put_rule(rule_id=rule_id, waf=waf_rule,
                                  condition=condition)
        self.assertTrue(ok)

        data = self.client.get_rule(rule_id)
        # None means true
        self.assertEqual(data['waf']['cross_requests'], True)
        self.assertEqual(data['waf']['threshold_score'], 100)

        # use sensitivity instead of threshold
        # cross_requests = False
        waf_rule = {'rule_sets': [7,8,9,10,11,12,13,14,15,16,17],
                    'action': 'redirect',
                    'sensitivity': 'high',
                    'cross_requests': False,
                    'redirect_url': 'https://openrsty.org'}
        ok = self.client.put_rule(rule_id=rule_id, waf=waf_rule,
                                  condition=condition)
        self.assertTrue(ok)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data['waf']['cross_requests'], False)
        # high sensitivity == low threshold
        self.assertEqual(data['waf']['threshold_score'], 3)

        # custom score
        waf_rule = {'rule_sets': [7,8,9,10],
                    'action': 'redirect',
                    'sensitivity': 'none',
                    'score': 1,
                    'cross_requests': False,
                    'redirect_url': 'https://openrsty.org'}
        ok = self.client.put_rule(rule_id=rule_id, waf=waf_rule,
                                  condition=condition)
        self.assertTrue(ok)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data['waf']['cross_requests'], False)
        self.assertEqual(data['waf']['threshold_score'], 1)
        self.assertEqual(data['waf']['rule_sets_threshold'], [-1, -1, -1, -1])

        # custom score
        waf_rule = {'rule_sets': [7,8,9,10],
                    'action': 'redirect',
                    'sensitivity': 'none',
                    'score': 1,
                    'cross_requests': False,
                    'rule_sets_threshold': [1,2,3,4],
                    'redirect_url': 'https://openrsty.org'}
        ok = self.client.put_rule(rule_id=rule_id, waf=waf_rule,
                                  condition=condition)
        self.assertTrue(ok)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data['waf']['cross_requests'], False)
        self.assertEqual(data['waf']['threshold_score'], 1)
        self.assertEqual(data['waf']['rule_sets_threshold'], [1,2,3,4])

        ok = self.client.del_rule(rule_id)
        self.assertTrue(ok)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data, {})

    def test_cache(self):
        condition = [{'var': 'client-country', 'op': 'eq', 'val': 'CN'}]
        cache_key = ['uri', 'query-string', 'client-city']
        cache_rule = {'cache_key': cache_key}
        rule_id = self.client.new_rule(condition=condition, cache=cache_rule)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        data = self.client.get_rule(rule_id)
        # default should be True
        self.assertEqual(data['enable_rule'], True)
        # default should be True
        self.assertEqual(data['last'], True)

        condition[0]['val'] = 'JP'
        cache_key = [
            {'name': "uri", },
            {'name': "client-city"},
            {'name': "client-continent", 'args': 'first-x-forwarded-addr'},
            {'name': "query-string"}
        ]
        default_ttls= [{
            'ttl_unit': "min", 'status': 200, 'ttl': 2
        }, {
            'ttl_unit': "min", 'status': 301, 'ttl': 1
        }]
        cache_rule = {
            'cache_key': cache_key,
            'default_ttls': default_ttls,
            'browser_ttl': 2,
            'browser_ttl_unit': 'min',
            'disable_convert_head': True,
            'enforce_cache': True,
            'cluster_hash': True,
            'enable_global': ON,
        }
        ok = self.client.put_rule(rule_id=rule_id, condition=condition,
                                  cache=cache_rule)
        self.assertTrue(ok)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data['cache']['cache_key'][0]['name'], 'uri')
        self.assertEqual(data['cache']['cache_key'][1]['name'], 'client-city')
        self.assertEqual(data['cache']['cache_key'][2]['args'], 'first-x-forwarded-addr')
        self.assertEqual(len(data['cache']['cache_key']), 4)
        self.assertEqual(data['cache']['cluster_hash'], True)
        self.assertEqual(data['cache']['disable_convert_head'], True)
        self.assertEqual(data['cache']['enforce_cache'], True)
        self.assertEqual(data['cache']['enable_global'], ON)
        self.assertEqual(data['cache']['browser_ttl'], 2)
        self.assertEqual(data['cache']['browser_ttl_unit'], 'min')
        self.assertEqual(type(data['cache']['default_ttls']), type(list()))
        self.assertEqual(data['conditions'][0]['values'][0]['val'], 'JP')

        # disable default cache
        # disable browser cache
        cache_rule = {
            'cache_key': cache_key,
            'default_ttls': OFF,
            'browser_ttl': OFF,
            'browser_ttl_unit': 'min',
            'disable_convert_head': False,
            'enforce_cache': False,
            'cluster_hash': False,
            'enable_global': OFF,
        }
        ok = self.client.put_rule(rule_id=rule_id, condition=condition,
                                  cache=cache_rule)
        self.assertTrue(ok)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data['cache'].get('default_ttls',None), None)
        self.assertEqual(data['cache']['cluster_hash'], False)
        self.assertEqual(data['cache']['enforce_cache'], False)
        self.assertEqual(data['cache'].get('browser_ttl',None), None)
        self.assertEqual(data['cache'].get('browser_ttl_unit',None), None)
        self.assertEqual(data['cache']['disable_convert_head'], False)
        self.assertEqual(data['cache']['enable_global'], OFF)

        ok = self.client.del_rule(rule_id)
        self.assertTrue(ok)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data, {})

    def test_content(self):
        condition = [{'var': 'uri', 'op': 'eq', 'val': '/favicon.ico'}]
        file_id = self.client.upload_favicon(name='test',
                                             favicon_content='content')
        self.assertIs(type(file_id), int)
        self.assertGreater(file_id, 0)

        rule_id = self.client.new_rule(condition=condition,
                                       content={'favicon': file_id})
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        new_file_id = self.client.upload_favicon(
            name='test',
            favicon_content='new_content')
        self.assertIs(type(new_file_id), int)
        self.assertGreater(new_file_id, 0)

        ok = self.client.put_rule(rule_id=rule_id,
                                  content={'favicon': new_file_id})
        self.assertTrue(ok)

        data = self.client.get_rule(rule_id)

        self.assertEqual(data['content']['file'], new_file_id)
        self.assertEqual(data['conditions'][0]['values'][0]['val'],
                         '/favicon.ico')

        ok = self.client.del_rule(rule_id)
        self.assertTrue(ok)

        ok = self.client.del_favicon(file_id)
        ok = self.client.del_favicon(new_file_id)
        self.assertTrue(ok)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data, {})

    def test_empty_gif(self):
        condition = [{'var': 'uri', 'op': 'eq', 'val': '/'}]
        rule_id = self.client.new_rule(condition=condition,
                                       content={'empty_gif': True})
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        data = self.client.get_rule(rule_id)
        self.assertTrue(data['content']['empty_gif'])

        ok = self.client.del_rule(rule_id)
        self.assertTrue(ok)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data, {})

    def test_get_all_rules(self):
        condition = [{'var': 'client-country', 'op': 'eq', 'val': 'CN'}]
        cache_key = ['uri', 'query-string', 'client-city']
        cache_rule = {'cache_key': cache_key}
        rule_id = self.client.new_rule(condition=condition, cache=cache_rule,
                                       top=1)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        condition = [
            {'var': 'host', 'val': 'con.' + self.apex},
            {'var': ['req-header', 'Referer'],
             'vals': [[r'foo\d+', 'rx'], 'foo.com']}
        ]
        conseq = {
            'enable-websocket': {},
            'redirect': {'url': '/cn/2017/', 'code': 302},
            'user-code': {'el': 'true => say(\"hello\");'}
        }
        rule_id = self.client.new_rule(condition=condition, conseq=conseq,
                                       last=True)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        data = self.client.get_all_rules()
        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]['top'], 1)
        self.assertTrue(data[1]['last'])

        data = self.client.get_all_rules_by_app_domain(self.apex)
        self.assertEqual(len(data), 2)

    def test_el(self):
        code = "true => print('hello, {}');".format(self.apex)
        ok = self.client.new_el(phase='req-rewrite', code=code, pre=True)
        self.assertTrue(ok)

    def test_cert(self):
        domain = str(random.randint(1, 10000)) + '.foo.com'
        ok = self.client.put_app(app_id=self.app_id, domains=[domain],
                                 label='foo.com')
        self.assertTrue(ok)

        self.client.new_release()

        key_file = os.path.join(CURPATH, 'tests', 'key.pem')
        cert_file = os.path.join(CURPATH, 'tests', 'cert.pem')
        with open(key_file) as f:
            key = f.read()
        with open(cert_file) as f:
            cert = f.read()

        cert_id = self.client.set_cert_key(key=key, cert=cert)
        self.assertIs(type(cert_id), int)
        self.assertGreater(cert_id, 0)

        data = self.client.get_cert_key(cert_id)
        self.assertEqual(data['domains'][0], '*.foo.com')

        data = self.client.get_all_cert_keys()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['domains'], ['*.foo.com'])

        ok = self.client.del_cert_key(cert_id)
        self.assertTrue(ok)

        data = self.client.get_cert_key(cert_id)
        self.assertEqual(data, {})

    def test_req_rewrite_3(self):
        condition = [
            {'var': 'host', 'val': 'con.' + self.apex},
            {'var': 'server-port', 'op': 'is-empty'},
        ]
        conseq = {
            'enable-websocket': {},
            'redirect': {'url': '/cn/2017/', 'code': 302}
        }
        rule_id = self.client.new_rule(condition=condition, conseq=conseq)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data['conditions'][0]['variable']['name'], 'host')
        self.assertEqual(data['conditions'][1]['variable']['name'],
                         'server-port')
        self.assertEqual(data['conditions'][1]['operator']['name'], 'is-empty')

        ok = self.client.del_rule(rule_id)
        self.assertTrue(ok)
        data = self.client.get_rule(rule_id)
        self.assertEqual(data, {})

    def test_rule_order(self):
        condition = [{'var': 'uri', 'op': 'eq', 'val': '/favicon.ico'}]
        file_id = self.client.upload_favicon(name='test',
                                             favicon_content='content')
        self.assertIs(type(file_id), int)
        self.assertGreater(file_id, 0)

        rule_id = self.client.new_rule(condition=condition,
                                       content={'favicon': file_id})
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        new_file_id = self.client.upload_favicon(
            name='test',
            favicon_content='new_content')
        self.assertIs(type(new_file_id), int)
        self.assertGreater(new_file_id, 0)

        ok = self.client.put_rule(rule_id=rule_id,
                                  content={'favicon': new_file_id},
                                  order=1)
        self.assertTrue(ok)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data['order'], 1)

        ok = self.client.del_rule(rule_id)
        self.assertTrue(ok)

        ok = self.client.del_favicon(file_id)
        ok = self.client.del_favicon(new_file_id)
        self.assertTrue(ok)

    def test_disable_rule(self):
        conseq = {
            'enable-websocket': {},
            'redirect': {'url': '/cn/2017/', 'code': 302}
        }
        rule_id = self.client.new_rule(conseq=conseq)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        data = self.client.get_rule(rule_id)
        # default should be True
        self.assertEqual(data['enable_rule'], True)
        # default should be False
        self.assertEqual(data['last'], False)

        rule_id = self.client.new_rule(conseq=conseq, enable=False)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data['enable_rule'], False)

        ok = self.client.put_rule(rule_id, conseq=conseq, enable=True)
        self.assertEqual(ok, True)
        data = self.client.get_rule(rule_id)
        self.assertEqual(data['enable_rule'], True)

        ok = self.client.put_rule(rule_id, conseq=conseq, enable=False)
        self.assertEqual(ok, True)
        data = self.client.get_rule(rule_id)
        self.assertEqual(data['enable_rule'], False)


    def test_disable_sections(self):
        condition = [{'var': 'client-country', 'op': 'eq', 'val': 'CN'}]
        waf_rule = {'rule_sets': [7,8,9,10,11,12,13,14,15,16,17],
                    'action': '403 Forbidden', 'threshold': 'low'}
        conseq = {
            'enable-websocket': {},
            'redirect': {'url': '/cn/2017/', 'code': 302},
        }
        cache_key = ['uri', 'query-string', 'client-city']
        cache_rule = {'cache_key': cache_key}

        condition = [{'var': 'uri', 'op': 'eq', 'val': '/favicon.ico'}]
        file_id = self.client.upload_favicon(name='test2', favicon_content='content')
        self.assertIs(type(file_id), int)
        self.assertGreater(file_id, 0)

        up_id = self.client.new_upstream(
            name='origin-upstream',
            servers=[
                {'domain': 'test.com', 'port': 80},
                {'ip': '172.22.31.2', 'port': 80, 'weight': 2}
            ])
        self.assertIs(type(up_id), int)
        self.assertGreater(up_id, 0)

        backup_up_id = self.client.new_upstream(
            name='backup-upstream',
            servers=[
                {'ip': '172.22.31.3', 'port': 80},
                {'ip': '172.22.31.4', 'port': 80, 'weight': 3}
            ])
        self.assertIs(type(backup_up_id), int)
        self.assertGreater(backup_up_id, up_id)

        proxy_rule = {
            'upstreams': [{'upstream': up_id, 'weight': 2}],
            'backup_upstreams': [{'upstream': backup_up_id}],
            'retries': 2,
            "retry_condition": ["invalid_header", "http_500"],
            "balancer_algorithm": "hash",
            "balancer_vars": [
                {"name": "uri"},
                {
                    "name": "uri-arg",
                    "args": "foo"
                }
            ]
        }

        rule_id = self.client.new_rule(condition=condition,
                                       conseq=conseq,
                                       waf=waf_rule,
                                       cache=cache_rule,
                                       proxy=proxy_rule,
                                       content={'favicon': file_id})

        data = self.client.get_rule(rule_id)
        self.assertEqual(data['enable_rule'], True)
        self.assertEqual(len(data['conditions']), 1)
        self.assertEqual(len(data['actions']), 2)
        self.assertGreater(len(data['cache']), 1)
        self.assertGreater(len(data['content']), 1)
        self.assertGreater(len(data['proxy']), 1)
        self.assertEqual(len(data['proxy']['backup_upstream']), 1)
        self.assertEqual(len(data['proxy']['upstream']), 1)
        self.assertGreater(len(data['waf']), 1)

        proxy_rule['backup_upstreams'] = None

        ok = self.client.put_rule(rule_id, proxy=proxy_rule)
        self.assertEqual(ok, True)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data['enable_rule'], True)
        self.assertEqual(len(data['conditions']), 1)
        self.assertEqual(len(data['actions']), 2)
        self.assertGreater(len(data['cache']), 1)
        self.assertGreater(len(data['content']), 1)
        self.assertGreater(len(data['proxy']), 1)
        self.assertEqual(data['proxy'].get('backup_upstream'), None)
        self.assertEqual(len(data['proxy']['upstream']), 1)
        self.assertGreater(len(data['waf']), 1)

        ok = self.client.put_rule(rule_id, condition=OFF,
                                       conseq=conseq,
                                       waf=OFF,
                                       cache=OFF,
                                       proxy=OFF,
                                       content=OFF)

        self.assertEqual(ok, True)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data['enable_rule'], True)
        self.assertEqual(data.get('conditions', None), None)
        self.assertEqual(len(data['actions']), 2)
        self.assertEqual(data.get('cache', None), None)
        self.assertEqual(data.get('content', None), None)
        self.assertEqual(data.get('proxy', None), None)
        self.assertEqual(data.get('waf', None), None)

        ok = self.client.put_rule(rule_id, conseq=OFF,
                                       waf=waf_rule)

        self.assertEqual(ok, True)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data['enable_rule'], True)
        self.assertEqual(data.get('conditions', None), None)
        self.assertEqual(data.get('actions', None), None)
        self.assertEqual(data.get('cache', None), None)
        self.assertEqual(data.get('content', None), None)
        self.assertEqual(data.get('proxy', None), None)
        self.assertGreater(len(data['waf']), 1)


    def test_rule_last(self):
        conseq = {
            'enable-websocket': {},
            'redirect': {'url': '/cn/2017/', 'code': 302}
        }
        rule_id = self.client.new_rule(conseq=conseq)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        conseq = {
            'redirect': {'url': '/cn/2018/', 'code': 301}
        }
        rule_id2 = self.client.new_rule(conseq=conseq)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        rules = self.client.get_all_rules()
        self.assertEqual(len(rules), 2)
        self.assertGreater(rules[0]['id'], rules[1]['id'])

        ok = self.client.put_rule(rule_id2, conseq=conseq, last=True)
        self.assertEqual(ok, True)
        data = self.client.get_rule(rule_id2)
        self.assertEqual(data['last'], True)

        # the "last" tag is unrelated to sequence,
        # it is just a switch in the page rules.
        self.assertGreater(rules[0]['id'], rules[1]['id'])

    def test_rule_order2(self):
        conseq = {
            'enable-websocket': {},
            'redirect': {'url': '/cn/2017/', 'code': 302}
        }
        rule_id = self.client.new_rule(conseq=conseq)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        conseq = {
            'redirect': {'url': '/cn/2018/', 'code': 301}
        }
        rule_id2 = self.client.new_rule(conseq=conseq)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        rules = self.client.get_all_rules()
        self.assertEqual(len(rules), 2)
        # rule_id == rules[1]['id']
        # rule_id2 == rules[0]['id']
        self.assertGreater(rules[0]['id'], rules[1]['id'])

        ok = self.client.put_rule(rule_id2, conseq=conseq, order=1)
        self.assertEqual(ok, True)
        data = self.client.get_rule(rule_id2)
        self.assertEqual(data['order'], 1)

        rules = self.client.get_all_rules()
        self.assertGreater(rules[1]['id'], rules[0]['id'])

        # reset to 0
        ok = self.client.put_rule(rule_id2, conseq=conseq, order=0)
        self.assertEqual(ok, True)
        data = self.client.get_rule(rule_id2)
        self.assertEqual(data['order'], 0)

        rules = self.client.get_all_rules()
        self.assertGreater(rules[0]['id'], rules[1]['id'])


    def test_rule_comment(self):
        conseq = {
            'enable-websocket': {},
            'redirect': {'url': '/cn/2017/', 'code': 302}
        }
        rule_id = self.client.new_rule(conseq=conseq)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data.get('comment', None), None)

        rule_id = self.client.new_rule(conseq=conseq, comment="test")
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data.get('comment', None), "test")

        ok = self.client.put_rule(rule_id, conseq=conseq, comment="test2")
        self.assertEqual(ok, True)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data.get('comment', None), "test2")

        ok = self.client.put_rule(rule_id, conseq=conseq, comment="")
        self.assertEqual(ok, True)

        data = self.client.get_rule(rule_id)
        self.assertEqual(data.get('comment', None), None)

    def test_waf_rule_set_name(self):
        condition = [{'var': 'uri', 'op': 'prefix', 'val': '/foo'}]
        waf_rule = {'rule_sets': ["protocol_enforcement", "protocol_attack"],
                    'action': '403 Forbidden', 'threshold': 'high'}
        rule_id = self.client.new_rule(condition=condition,
                                       waf=waf_rule, last=True)
        self.assertIs(type(rule_id), int)
        self.assertGreater(rule_id, 0)

        data = self.client.get_rule(rule_id)
        self.assertIn(7, data['waf']['rule_sets'])
        self.assertIn(8, data['waf']['rule_sets'])
        self.assertEqual(data['waf']['threshold_score'], 1000)
