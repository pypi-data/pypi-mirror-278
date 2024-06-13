# -*- coding: utf-8 -*-

OFF = False
ON = True

waf_rule_sets_name2id = {
    'robots': 1,
    'generic': 2,
    'inject': 3,
    'trojans': 4,
    'xss': 5,
    'scanner_detection': 6,
    'protocol_enforcement': 7,
    'protocol_attack': 8,
    'application_attack_lfi': 9,
    'application_attack_rfi': 10,
    'application_attack_rce': 11,
    'application_attack_php': 12,
    'application_attack_nodejs': 13,
    'application_attack_xss': 14,
    'application_attack_sqli': 15,
    'application_attack_session_fixation': 16,
    'application_attack_java': 17,
}

valid_waf_thresholds = {
    'high': True,
    'medium': True,
    'low': True,
    'none': True,
}

cross_req_waf_threshold_scores = {
    'high': 1000,
    'medium': 100,
    'low': 10,
}

waf_threshold_scores = {
    'high': 12,
    'medium': 6,
    'low': 3,
}
