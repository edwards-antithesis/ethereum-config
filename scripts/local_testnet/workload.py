import requests, time

beaconNodeIPs = ['http://10.0.20.4:8000','http://10.0.20.6:8002','http://10.0.20.8:8003','http://10.0.20.10:8004','http://10.0.20.12:8005','http://10.0.20.14:8006','http://10.0.20.16:8007','http://10.0.20.18:8008','http://10.0.20.20:8009','http://10.0.20.22:8010','http://10.0.20.24:8011','http://10.0.20.26:8012','http://10.0.20.28:8013','http://10.0.20.30:8014','http://10.0.20.32:8015','http://10.0.20.34:8016']

#,'http://10.0.20.36:8017','http://10.0.20.38:8018','http://10.0.20.40:8019','http://10.0.20.42:8020']

queryPaths = ['/eth/v1/beacon/headers',
              '/eth/v1/beacon/pool/attestations', '/eth/v1/beacon/pool/attester_slashings',
              '/eth/v1/beacon/pool/proposer_slashings', '/eth/v1/beacon/pool/voluntary_exits',
              '/eth/v1/debug/beacon/heads',
              '/eth/v1/node/syncing']

states = ['head', 'justified', 'finalized']

statePaths = ['/committees', '/validator_balances', '/root', '/fork', '/finality_checkpoints']

headQueryPaths = ['/eth/v1/beacon/states/']

slotQueryPaths = ['/eth/v1/beacon/blocks/']

def find_head_slot():
    response = requests.get(beaconNodeIPs[0] + '/eth/v1/node/syncing')
    return response.json()['data']['head_slot']

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print("Waiting for faults to start")
    time.sleep(10)
    print ("Faults Started, Starting execution of tests...")
    print ("antithesis: start_timer")
    index = 0
    while (index <3):
        print("Sequence Starting, "+str(index)+" .")
        headSlot = find_head_slot()

        
        for j in range(len(queryPaths)):
            baseline_response = requests.get(beaconNodeIPs[0]+queryPaths[j])
            for i in range(len(beaconNodeIPs)):
                print(beaconNodeIPs[i]+queryPaths[j])
                response = requests.get(beaconNodeIPs[i]+queryPaths[j])
                print(response.content)

                if response.content != baseline_response.content:
                    print("FAILED!")
                    print(baseline_response.content)
                    print(response.content)
                time.sleep(0.5)

        for k in range(len(slotQueryPaths)):
            baseline_response = requests.get(beaconNodeIPs[0]+slotQueryPaths[k]+headSlot)
            for i in range(len(beaconNodeIPs)):
                print(beaconNodeIPs[i]+slotQueryPaths[k]+headSlot)
                response = requests.get(beaconNodeIPs[i]+slotQueryPaths[k]+headSlot)
                print(response.content)
                
                if response.content != baseline_response.content:
                    print("FAILED!")
                    print(baseline_response.content)
                    print(response.content)
                time.sleep(0.5)

        for l in range(len(statePaths)):
            for m in range(len(states)):
                baseline_response = requests.get(beaconNodeIPs[0] + '/eth/v1/beacon/states/' + states[m] + statePaths[l])
                for i in range(len(beaconNodeIPs)):
                    print(beaconNodeIPs[i]+'/eth/v1/beacon/states/'+states[m]+statePaths[l])
                    response = requests.get(beaconNodeIPs[i]+'/eth/v1/beacon/states/'+states[m]+statePaths[l])
                    print(response.content)

                    if response.content != baseline_response.content:
                        print("FAILED!")
                        print(baseline_response.content)
                        print(response.content)
                    time.sleep(0.5)

        print("Sequence Ended, Sleeping, Loop "+str(index)+" .")
        index = index + 1
        time.sleep(10)
    print ("Workload Done.")    