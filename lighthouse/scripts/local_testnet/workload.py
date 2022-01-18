import requests, time

beacon_nodes = [
    ('beacon2', 'http://10.0.20.6:8002'),
    ('beacon3', 'http://10.0.20.8:8003'),
    ('beacon4', 'http://10.0.20.10:8004'),
    ('beacon5', 'http://10.0.20.12:8005'),
    ('beacon6', 'http://10.0.20.14:8006'),
    ('beacon7', 'http://10.0.20.16:8007'),
    ('beacon8', 'http://10.0.20.18:8008'),
    ('beacon9', 'http://10.0.20.20:8009'),
    ('beacon10','http://10.0.20.22:8010'),
    ('beacon11','http://10.0.20.24:8011'),
    ('beacon12','http://10.0.20.26:8012'),
    ('beacon13','http://10.0.20.28:8013'),
    ('beacon14','http://10.0.20.30:8014'),
    ('beacon15','http://10.0.20.32:8015'),
    ('beacon16','http://10.0.20.34:8016'),
    ('beacon17','http://10.0.20.36:8017'),
    ('beacon18','http://10.0.20.38:8018'),
    ('beacon19','http://10.0.20.40:8019'),
    ('beacon20','http://10.0.20.42:8020')
]

baseline_node = ('beacon1', 'http://10.0.20.4:8000')

queryPaths = ['/eth/v1/beacon/headers',
              '/eth/v1/beacon/pool/attestations',
              '/eth/v1/beacon/pool/attester_slashings',
              '/eth/v1/beacon/pool/proposer_slashings',
              '/eth/v1/beacon/pool/voluntary_exits',
              '/eth/v1/debug/beacon/heads',
              '/eth/v1/node/syncing']

states = ['head', 'justified', 'finalized']

statePaths = ['/committees', '/validator_balances', '/root', '/fork', '/finality_checkpoints']

headQueryPaths = ['/eth/v1/beacon/states/']

slotQueryPaths = ['/eth/v1/beacon/blocks/']

def find_head_slot(node):
    response = requests.get(node[1] + '/eth/v1/node/syncing')
    return response.json()['data']['head_slot']

def api_baseline_compare(baseline_node, nodes, api_uri, api_call_interval=0.5):
    print(f"Comparing responses on {api_uri}")
    baseline_response = requests.get(baseline_node[1]+api_uri)
    print(f"Baseline response: {baseline_response.content}")
    divergent_responses = []
    for node in nodes:
        response = requests.get(node[1]+api_uri)
        if response.content != baseline_response.content:
            divergent_responses.append((node[0], response.content))        
        time.sleep(api_call_interval)
    if(len(divergent_responses) > 0):
        responses = [f"{{'node': {d[0]}, 'node_response': {d[1]} }}" for d in divergent_responses]
        print(f"FAILED! {{'api': {api_uri}, 'baseline_response': {baseline_response.content}, 'responses': [{','.join(responses)}] }}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(f"antithesis: start_faults")
    time.sleep(5)    
    print ("antithesis: start_timer")
    index = 0
    while (index < 3):
        print(f"Starting sequence: {index} ")
        headSlot = find_head_slot(baseline_node)

        
        for p in queryPaths:
            api_baseline_compare(baseline_node, beacon_nodes, p)

        for p in slotQueryPaths:
            api_baseline_compare(baseline_node, beacon_nodes, p+headSlot)

        for p in statePaths:
            for s in states:
                api_baseline_compare(baseline_node, beacon_nodes, '/eth/v1/beacon/states/' + s + p)

        print(f"Sequence completed: {index} ")
        index = index + 1
        time.sleep(10)
    print ("Workload Done.")
    print ("antithesis: terminate")    